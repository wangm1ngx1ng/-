#!/usr/bin/env python3
"""Extract a video into a dense, zero-gap contact sheet.

The strict mode intentionally refuses impossible layouts instead of adding
padding, cropping, or distorting frames.
"""
from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--frames", type=int, default=24)
    ap.add_argument("--interval", type=float, default=None,
                    help="按固定秒数抽帧，例如 --interval 1 表示每秒一帧")
    ap.add_argument("--columns", type=int, default=4)
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--every-frame", action="store_true",
                    help="读取视频流中的每一帧；忽略 --frames")
    ap.add_argument("--approximate", action="store_true",
                    help="允许输出最接近的自然比例；仍不留白、不裁切、不变形")
    args = ap.parse_args()
    if args.frames < 1 or args.columns < 1 or args.width < 1:
        raise SystemExit("frames、columns、width 必须为正整数")
    if not args.video.is_file():
        raise SystemExit(f"找不到视频：{args.video}")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("未找到 ffmpeg，请先安装并确保它在 PATH 中")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="video-contact-sheet-") as td:
        frame_dir = Path(td)
        if args.every_frame:
            run(["ffmpeg", "-y", "-i", str(args.video), "-vsync", "0",
                 str(frame_dir / "frame_%05d.png")])
        else:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(args.video)],
                check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            duration = max(float(probe.stdout.strip()), 0.001)
            sample_fps = (1 / args.interval) if args.interval else max(args.frames / duration, 0.001)
            cmd = ["ffmpeg", "-y", "-i", str(args.video), "-vf", f"fps={sample_fps:.8f}"]
            if args.interval is None:
                cmd += ["-frames:v", str(args.frames)]
            cmd += [str(frame_dir / "frame_%05d.png")]
            run(cmd)
        frames = sorted(frame_dir.glob("frame_*.png"))
        if not frames:
            raise SystemExit("视频没有可读取的抽帧结果")
        if not args.every_frame and args.interval is None:
            frames = frames[:args.frames]

        with Image.open(frames[0]) as first:
            src_w, src_h = first.size
        ratio = src_w / src_h
        cols = min(args.columns, len(frames))
        rows = math.ceil(len(frames) / cols)
        tile_w = args.width / cols
        tile_h = tile_w / ratio
        natural_h = tile_h * rows
        target_h = args.width * 4 / 3
        if not args.approximate and abs(natural_h - target_h) > 0.5:
            raise SystemExit(
                "当前抽帧数/列数无法同时满足严格3:4与全局同尺寸。"
                f"自然比例为 {args.width:.0f}:{natural_h:.0f}。"
                "请调整 --frames 或 --columns；不要用留白、裁切或变形补齐。"
            )

        out_h = round(natural_h)
        sheet = Image.new("RGB", (args.width, out_h))
        for index, path in enumerate(frames):
            with Image.open(path) as image:
                image = image.convert("RGB")
                resized = image.resize((round(tile_w), round(tile_h)), Image.Resampling.LANCZOS)
            row, col = divmod(index, cols)
            x = round(col * tile_w)
            y = round(row * tile_h)
            sheet.paste(resized, (x, y))
        sheet.save(args.output, "PNG", optimize=True)
        actual = sheet.width / sheet.height
        print(f"输出：{args.output}")
        mode = "逐帧" if args.every_frame else "均匀抽样"
        print(f"抽帧：{len(frames)}（{mode}），布局：{rows}行×{cols}列，比例：{actual:.6f}")


if __name__ == "__main__":
    main()
