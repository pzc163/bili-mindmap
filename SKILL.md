---
name: bili-mindmap
description: Turn a Bilibili video link or BV number into a summarized XMind mind map for OpenClaw. Use when the user provides a Bilibili URL/BV and wants a summary, transcript-based outline, structured notes, 内容梳理, or 思维导图. The skill checks `bili` login state, guides QR login when needed, collects video details, subtitles, AI summary, and hot comments with `bilibili-cli`, falls back to audio extraction plus local OpenAI-compatible ASR when subtitles are unavailable, and exports a `.xmind` file.
homepage: https://github.com/pzc163/bili-mindmap
metadata:
  clawdbot:
    emoji: "🧠"
    files:
      - "scripts/*"
      - "references/*"
      - "agents/*"
---

# Bili Mindmap

把 B 站视频链接变成可以在 XMind 中打开的思维导图。

## 先决条件

- 确认 `bili` 已安装且可用。
- 确认 `xmind-generator` 目录已经完成依赖安装，可运行 `node scripts/generate_xmind.js`。
- 需要音频回退时，确认 `bilibili-cli[audio]` 已安装。
- 需要本地转写时，确认本地已有 OpenAI 兼容的转写接口。
- 优先复用仓库内现有目录：`bilibili-cli`、`xmind-generator`、`parakeet-local-asr`。

## 关键限制

- 先尝试字幕；只有拿不到字幕时才走音频转写。
- 登录是强依赖检查项：先运行 `bili status`，需要时再运行 `bili login`。
- 转写时先判断当前操作系统：Windows 优先走 `aliyun-asr`；Linux/macOS 优先走 `parakeet-local-asr`，如果本地 ASR 不可用或返回空结果，再切到 `aliyun-asr`。
- `aliyun-asr` 依赖阿里云配置；如果未配置，则要明确提示用户补齐配置文件。
- 不要臆造视频内容；缺失信息时要明确说明来源是字幕、评论、AI 总结还是 ASR 转写。

## 标准流程

1. 解析用户输入，接受完整 Bilibili 视频链接或 `BV` 号。
2. 运行 `bili status` 检查登录状态。
3. 如果未登录或需要凭证的命令失败，运行 `bili login`，等待用户扫码完成。
4. 运行 `python scripts/prepare_bili_context.py --source <视频链接或BV号> --login-if-needed --transcribe-if-needed` 收集上下文。
5. 阅读输出目录中的 `context.md`、`manifest.json` 和相关文本文件。
6. 按 `references/mindmap-outline-template.md` 的结构整理成 Markdown 大纲。
7. 把大纲保存为 `.md` 文件。
8. 运行 `python scripts/render_xmind.py --outline <大纲文件> --output <输出.xmind>` 生成思维导图。
9. 向用户说明思维导图路径，并标明主要内容来源。

## 一键流水线

如果要减少人工整理步骤，优先直接运行总控脚本：

```bash
python scripts/run_bili_mindmap.py \
  --source "BV1ABcsztEcY" \
  --output-dir output/BV1ABcsztEcY \
  --login-if-needed \
  --transcribe-if-needed
```

该脚本会依次执行：

1. 采集上下文
2. 自动生成 `outline.md`
3. 导出 `.xmind`，未显式指定输出路径时默认使用视频标题命名文件

## 采集策略

按下面顺序尽量完整收集信息：

1. `bili video <source>`：拿视频详情。
2. `bili video <source> --subtitle`：优先拿字幕。
3. `bili video <source> --ai`：拿站内 AI 总结。
4. `bili video <source> --comments`：拿热门评论。
5. 若字幕不可用：
   - 运行 `bili audio <source> -o <输出目录/audio>` 提取音频。
   - 根据当前操作系统选择 ASR：
     - Windows：优先 `aliyun-asr`
     - Linux/macOS：优先 `parakeet-local-asr`
   - Linux/macOS 下如果 `parakeet-local-asr` 接口不可达、调用报错或返回空文本，则自动切到 `aliyun-asr`。
   - 合并多个分段转写结果为单个全文。

## 推荐命令

```bash
# 只做上下文采集
python scripts/prepare_bili_context.py --source "https://www.bilibili.com/video/BV1ABcsztEcY"

# 自动在需要时登录并在无字幕时执行 ASR 回退
python scripts/prepare_bili_context.py \
  --source "BV1ABcsztEcY" \
  --login-if-needed \
  --transcribe-if-needed

# 手动指定只用阿里云 ASR
python scripts/prepare_bili_context.py \
  --source "BV1ABcsztEcY" \
  --transcribe-if-needed \
  --asr-provider aliyun

# 根据整理好的 Markdown 大纲生成 XMind
python scripts/render_xmind.py \
  --outline output/outline.md \
  --output output/video-mindmap.xmind

# 一条命令跑完整链路
python scripts/run_bili_mindmap.py \
  --source "BV1ABcsztEcY" \
  --output-dir output/BV1ABcsztEcY \
  --login-if-needed \
  --transcribe-if-needed
```

## 大纲整理要求

- 用视频标题作为中心主题。
- 一级分支优先包含：`视频概览`、`核心内容`、`关键细节`、`评论反馈`、`总结/行动项`。
- 长视频场景下，允许自动生成 `内容脉络` 分支，用于体现章节/片段结构。
- 如果来源是字幕或 ASR，按内容逻辑合并，而不是逐句复制。
- 如果来源是评论，只保留高价值观点、争议点、补充信息，不要把水评塞进思维导图。
- 如果 `AI 总结` 与字幕冲突，优先以字幕/ASR 为准，并在导图中保留“AI 总结补充”而非覆盖正文。
- `outline.md` 中允许对补充来源打标记：`（AI补充）`、`（评论补充）`、`（简介补充）`；逐字稿主干内容默认不加标记。

## 输出物

至少生成以下文件：

- `manifest.json`：记录采集与回退情况。
- `context.md`：供后续总结整理使用的完整上下文。
- `outline.md`：自动生成的 Markdown 思维导图大纲，可继续人工微调，并会对非逐字稿补充内容附加来源标记。
- `*.xmind`：可在 XMind 中直接打开的文件。

## 故障处理

- 如果 `bili` 不存在：提示先安装 `bilibili-cli`。
- 如果 `bili status` 失败：提示用户执行登录或检查本地凭证。
- 如果 `--subtitle` 没内容：继续走音频提取 + ASR。
- 如果音频提取失败：提示安装 `bilibili-cli[audio]` 或检查 FFmpeg/PyAV 依赖。
- 如果 Linux/macOS 上本地 Parakeet ASR 不可达：自动尝试 `aliyun-asr`，并在 `manifest.json` 中记录回退。
- 如果阿里云 ASR 也不可达或未配置：保留已采集的详情、AI 总结、评论，并明确说明缺少逐字稿。
- 如果 `node` 或 `xmind` 依赖缺失：提示先在 `xmind-generator` 目录执行依赖安装。

## 资源定位

- `scripts/prepare_bili_context.py`：统一检查登录、抓取内容、按操作系统选择 ASR 并执行回退。
- `scripts/generate_outline.py`：根据采集结果自动生成 `outline.md` 草稿。
- `scripts/run_bili_mindmap.py`：串起采集、生成大纲、导出 XMind 的总控脚本。
- `scripts/render_xmind.py`：包装调用 `xmind-generator/scripts/generate_xmind.js`。
- `references/mindmap-outline-template.md`：导图大纲模板。
- `bilibili-cli/README.md`：B 站命令参考。
- `parakeet-local-asr/SKILL.md`：本地转写服务约定。
- `aliyun-asr/SKILL.md`：云端转写服务约定。
- `xmind-generator/SKILL.md`：XMind 生成器约定。
