---
name: aliyun-asr
description: "Pure Aliyun ASR skill for speech-to-text from local audio files or voice messages. Use when OpenClaw or another skill needs to transcribe WAV, MP3, OGG, FLAC, AMR, or OPUS audio into text, especially on Windows where local Parakeet ASR may not be available."
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "requires": { "bins": ["python3"] },
        "install": [],
      },
  }
---

# Aliyun ASR

纯语音转文字 skill，不做 TTS，不做 OSS，只负责把音频内容转成文本。

它既可以处理 OpenClaw 渠道里的语音消息，也可以直接处理本地音频文件。

## 核心能力

- 语音转文本，不生成语音回复
- 支持本地音频文件输入
- 支持 OpenClaw 渠道中的语音消息输入
- 适合作为 Windows 环境下的 ASR 回退方案

## 快速配置

### 1. 准备阿里云账号

- 开通阿里云智能语音交互 NLS 服务
- 创建具备 NLS 权限的 AccessKey
- 获取应用 `AppKey`

### 2. 配置文件位置

默认配置文件位置：

- Windows: `%USERPROFILE%\.openclaw\aliyun-asr-config.json`
- Linux/macOS: `~/.openclaw/aliyun-asr-config.json`

也可以通过环境变量覆盖：

```bash
ALIYUN_ASR_CONFIG=/path/to/aliyun-asr-config.json
```

配置文件示例：

```json
{
  "access_key_id": "your-access-key-id",
  "access_key_secret": "your-access-key-secret",
  "app_key": "your-app-key",
  "region": "cn-shanghai"
}
```

### 3. 安全设置

Linux/macOS 可选：

```bash
chmod 600 ~/.openclaw/aliyun-asr-config.json
```

## 使用方式

### OpenClaw 语音消息模式

1. 用户发送语音消息
2. OpenClaw 调用该 skill
3. skill 返回文本给上层流程

### 本地音频文件模式

直接传入音频文件路径：

```bash
python main.py /path/to/audio.wav
python handle_media.py /path/to/audio.mp3
python aliyun_pure_asr.py /path/to/audio.ogg
```

这正适合 `bili-mindmap` 这种“先提取音频文件，再做转写”的场景。

## 技术细节

- 依赖：`requests`
- 支持格式：MP3, WAV, OGG, FLAC, AMR, OPUS
- 输入模式：本地音频文件路径
- 输出模式：纯文本

## 注意事项

- 当前实现最适合短音频或已经切分好的音频段
- 对长音频，建议像 `bili-mindmap` 一样先切分再逐段转写
- Windows 环境下它适合作为 Parakeet 不可用时的回退方案
