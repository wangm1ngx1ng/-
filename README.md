# Video Replication Breakdown

一个用于 ChatGPT / Codex 的视频一比一复刻拆解 Skill。它会基于完整视频证据，输出可直接使用的中文复刻方案，包括固定 15 秒分段、逐 0.5 秒视觉时间轴、独立真实人声 SRT、负面提示词、资产要求与验收结果。

## 核心特点

- 先核对完整视频、真实画面和音频，再生成提示词。
- 固定按 `ceil(视频总时长 / 15秒)` 分段，每段本地时间从 `00:00.0` 开始。
- 每个片段独立完整，不依赖“上一段”“参考视频”等外部措辞。
- 逐 0.5 秒描述动作、机位、运镜、道具和连续性。
- 口播仅来自真实可听人声，并以独立 SRT 交付。

## 目录结构

```text
video-replication-breakdown/
├── SKILL.md
├── README.md
└── agents/
    └── openai.yaml
```

`SKILL.md` 是必需的工作流说明；`agents/openai.yaml` 提供 ChatGPT / Codex 中的展示名称、简介和默认提示词。

## 安装

将整个 `video-replication-breakdown` 文件夹放入 Codex 可扫描的 Skill 目录，确保 `SKILL.md` 与 `agents/openai.yaml` 的相对位置保持不变。也可以使用支持从 Git 仓库安装 Skill 的安装器指向本仓库。

安装后可显式调用：

```text
$video-replication-breakdown 请拆解我上传的视频，并给出可直接投喂的复刻提示词。
```

## 使用边界

仅用于用户拥有或已获授权使用的视频。无法由真实画面或音频确认的内容不得凭空补写。

## 授权状态

本项目采用 [MIT License](./LICENSE) 开源。
