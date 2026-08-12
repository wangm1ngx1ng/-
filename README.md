# AI 视频生产 Skills 合集

一套面向 ChatGPT / Codex 的中文 AI 视频生产工作流，覆盖视频复刻拆解、专业短视频剪辑、场景锚定九宫格和真实视频抽帧。

## 已收录 Skills

### 1. Video Replication Breakdown

仓库根目录中的 `SKILL.md`。基于完整视频证据输出固定 15 秒分段、逐 0.5 秒视觉时间轴、独立真实人声 SRT、负面提示词、资产要求与验收结果。

显式调用：

```text
$video-replication-breakdown 请拆解我上传的视频，并给出可直接投喂的复刻提示词。
```

### 2. Professional Video Editor

目录：`skills/professional-video-editor/`

根据参考视频拆解最终视觉风格，联网寻找与口播内容匹配的真实素材，建立素材与台词时间码表，并完成剪辑、混剪、调色、字幕和最终视频输出。

显式调用：

```text
$professional-video-editor 按参考视频风格为我的素材匹配真实素材并输出最终成片。
```

### 3. Scene Anchor Nine Grid

目录：`skills/scene-anchor-nine-grid/`

将剧本段落、场景描述或参考图转换为 16:9 横屏 3×3 Next Scene 场景调度板、人物站位连续性图、动作道具连续性图和关键帧投喂表。

显式调用：

```text
$scene-anchor-nine-grid 把我的场景段落整理成16:9横屏3×3 Next Scene场景锚定分镜提示词。
```

### 4. Frame Grab Sheet

目录：`skills/frame-grab-sheet/`

从真实视频按时间顺序抽帧，生成严格 3:4、无间距、保持原比例的高密度分镜总览图，并包含可复现的抽帧脚本。

显式调用：

```text
$frame-grab-sheet 请把这个视频制作成真实抽帧、无裁切无变形的3:4密集分镜总览图。
```

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
└── skills/
    ├── professional-video-editor/
    │   ├── SKILL.md
    │   └── agents/openai.yaml
    ├── scene-anchor-nine-grid/
    │   ├── SKILL.md
    │   └── agents/openai.yaml
    └── frame-grab-sheet/
        ├── SKILL.md
        ├── agents/openai.yaml
        └── scripts/make_contact_sheet.py
```

每个 Skill 的 `SKILL.md` 是工作流入口，`agents/openai.yaml` 提供 ChatGPT / Codex 中的展示名称、简介与默认提示词。

## 安装

安装单个 Skill 时，将对应 Skill 目录完整复制到 Codex 可扫描的 Skill 目录，并保持内部相对路径不变。仓库根目录本身对应 `video-replication-breakdown`；其余三个 Skill 位于 `skills/` 下。

`frame-grab-sheet` 运行时需要 Python、Pillow、ffmpeg 和 ffprobe。

## 使用边界

- 只复刻、处理或发布用户拥有或已获授权使用的素材。
- 网络素材必须保留来源和授权记录；授权无法确认时不得用于最终成片。
- 无法由真实画面或音频确认的内容不得凭空补写。

## License

本项目采用 [MIT License](./LICENSE) 开源。
