# bili-mindmap

`bili-mindmap` 是一个面向 OpenClaw / Codex 工作流的 Bilibili 视频知识整理项目：输入一个 B 站视频链接或 `BV` 号，自动抓取视频信息、字幕、AI 总结、热门评论，在字幕缺失时自动回退到音频转写，最后输出 `outline.md` 和可直接在 XMind 中打开的 `.xmind` 思维导图文件。

这个仓库当前采用 **workspace / monorepo** 形式组织：`bili-mindmap` 作为主 skill 负责编排流程，同时集成 `bilibili-cli`、`aliyun-asr`、`parakeet-local-asr`、`xmind-generator` 等 companion skills 或本地副本，方便直接联调和复现。

## 功能特性

- 输入 Bilibili 视频链接或 `BV` 号，自动生成思维导图
- 自动检查 `bili` 登录状态，必要时引导扫码登录
- 自动抓取视频详情、字幕、AI 总结、热门评论
- 字幕不可用时自动提取音频并执行 ASR 回退
- Windows 优先使用 `aliyun-asr`
- Linux / macOS 优先使用 `parakeet-local-asr`，失败时回退到 `aliyun-asr`
- 自动生成结构化 `outline.md`
- 自动导出 `.xmind` 文件，默认使用视频标题命名
- 对评论、AI 总结、视频简介等补充来源添加来源标记

## 适用场景

- 把 B 站视频整理成知识导图
- 快速梳理长视频结构与核心观点
- 为课程、访谈、纪录片、知识区内容生成复盘材料
- 作为 OpenClaw 的一个可复用 skill 工作流

## 仓库结构

- `SKILL.md`：主 skill 入口，面向 OpenClaw / Codex 的使用说明
- `agents/openai.yaml`：主 agent 配置
- `references/`：导图大纲参考模板等资料
- `scripts/prepare_bili_context.py`：采集视频上下文、登录状态和 ASR 回退
- `scripts/generate_outline.py`：从上下文生成 Markdown 导图大纲
- `scripts/render_xmind.py`：把 Markdown 大纲转换为 `.xmind`
- `scripts/run_bili_mindmap.py`：一键跑完整流程
- `bilibili-cli/`：Bilibili CLI 相关能力
- `aliyun-asr/`：阿里云文件音频转写能力，Windows 推荐
- `parakeet-local-asr/`：本地 Parakeet ASR 能力，Linux / macOS 推荐
- `xmind-generator/`：XMind 文件生成器
- `RELEASE_CHECKLIST.md`：GitHub 发布前自检清单

## 架构说明

这个项目推荐作为 **主 skill + companion skills** 来理解，而不是把所有能力硬塞进一个单体 skill：

- `bili-mindmap`：主流程编排层
- `bilibili-cli`：视频详情、字幕、评论、音频提取
- `aliyun-asr`：云端文件音频转写回退
- `parakeet-local-asr`：本地 ASR 服务
- `xmind-generator`：导图文件导出

这样做的好处是：

- 结构清晰，边界明确
- 易于替换某个依赖能力
- 更方便持续维护和后续拆分
- 方便先在一个仓库内联调，再逐步模块化发布

## 工作流程

完整流程如下：

1. 使用 `bili status` 检查 Bilibili 登录状态
2. 如果未登录，则使用 `bili login` 引导扫码登录
3. 使用 `bili video` 获取：
   - 视频详情
   - 字幕
   - AI 总结
   - 热门评论
4. 如果字幕不可用，则使用 `bili audio` 提取音频
5. 根据当前操作系统选择 ASR：
   - Windows：优先 `aliyun-asr`
   - Linux / macOS：优先 `parakeet-local-asr`，失败后回退到 `aliyun-asr`
6. 将采集结果整理为 `context.md` 与中间文件
7. 使用 `generate_outline.py` 生成 `outline.md`
8. 使用 `render_xmind.py` 输出 `.xmind`

## 平台策略

### Windows

- 推荐优先配置 `aliyun-asr`
- 不依赖本地 Parakeet 服务也可以完成字幕缺失回退

### Linux / macOS

- 推荐优先使用 `parakeet-local-asr`
- 如果 Parakeet 本地服务不可达、返回空结果或执行失败，自动回退到 `aliyun-asr`

## 环境要求

至少需要以下运行环境：

- Python 3.10+
- Node.js 18+
- `bili` 命令可用

如果需要音频回退，还需要：

- `bilibili-cli[audio]`
- 对应的音频依赖链路可用
- 至少准备一个可用的 ASR 提供方：
  - Windows：推荐 `aliyun-asr`
  - Linux / macOS：推荐 `parakeet-local-asr`，并准备 `aliyun-asr` 作为兜底

## 安装说明

### 1. 安装 `bilibili-cli`

推荐使用：

```bash
pipx install "bilibili-cli[audio]"
```

或者：

```bash
uv tool install "bilibili-cli[audio]"
```

安装后确认：

```bash
bili --help
```

### 2. 安装 XMind 生成依赖

在 `xmind-generator` 目录执行：

```bash
cd xmind-generator
npm install
```

### 3. 准备 ASR

#### 方案 A：阿里云 ASR

默认读取以下配置文件：

- Windows：`%USERPROFILE%\.openclaw\aliyun-asr-config.json`
- Linux / macOS：`~/.openclaw/aliyun-asr-config.json`

也可以通过环境变量覆盖：

```bash
ALIYUN_ASR_CONFIG=/path/to/aliyun-asr-config.json
```

配置示例：

```json
{
  "access_key_id": "your-access-key-id",
  "access_key_secret": "your-access-key-secret",
  "app_key": "your-app-key",
  "region": "cn-shanghai"
}
```

#### 方案 B：Parakeet 本地 ASR

参考 `parakeet-local-asr/SKILL.md` 启动本地服务。默认约定：

- URL：`http://localhost:9001`
- 端点：`/v1/audio/transcriptions`

## 快速开始

### 一键运行完整流程

```bash
python scripts/run_bili_mindmap.py \
  --source "https://www.bilibili.com/video/BV1ABcsztEcY" \
  --output-dir output/BV1ABcsztEcY \
  --login-if-needed \
  --transcribe-if-needed
```

如果不显式指定 `.xmind` 输出文件名，程序会默认使用 **视频标题** 作为文件名。

### 指定 ASR 提供方

```bash
python scripts/run_bili_mindmap.py \
  --source "BV1ABcsztEcY" \
  --output-dir output/BV1ABcsztEcY \
  --transcribe-if-needed \
  --asr-provider aliyun
```

可选值：

- `auto`
- `parakeet`
- `aliyun`

## 分步运行

### 1. 采集视频上下文

```bash
python scripts/prepare_bili_context.py \
  --source "BV1ABcsztEcY" \
  --output output/BV1ABcsztEcY \
  --login-if-needed \
  --transcribe-if-needed
```

### 2. 生成思维导图大纲

```bash
python scripts/generate_outline.py \
  --context-dir output/BV1ABcsztEcY
```

### 3. 导出 XMind 文件

```bash
python scripts/render_xmind.py \
  --outline output/BV1ABcsztEcY/outline.md \
  --output output/BV1ABcsztEcY/result.xmind
```

## 输出内容

每次运行通常会生成：

- `manifest.json`：记录登录检查、采集结果、ASR 回退状态
- `context.md`：汇总上下文，方便人工排查
- `outline.md`：自动生成的导图大纲
- `video_details.txt` / `video_details.json`
- `subtitles.txt`
- `ai_summary.txt`
- `comments.txt`
- `transcript.txt`：仅在字幕缺失且 ASR 成功时生成
- `*.xmind`

## 大纲结构约定

自动生成的大纲会尽量包含以下分支：

- `视频概览`
- `内容脉络`
- `核心内容`
- `关键细节`
- `评论反馈`
- `总结 / 行动项`

说明：

- `内容脉络` 会尽量根据字幕或 ASR 文本自动提炼
- 来自 AI 总结、评论、简介的内容会附加来源标记
- 来自字幕 / ASR 主干内容默认不加标记

## 在 OpenClaw 中使用

如果你是把这个仓库作为 OpenClaw skill 工程使用，主入口是根目录的 `SKILL.md`。

典型触发方式示例：

- “把这个 B 站视频整理成思维导图：`https://www.bilibili.com/video/...`”
- “总结这个 BV 视频并输出 XMind 文件：`BV...`”
- “根据这个 B 站视频自动生成知识梳理导图”

## GitHub 发布建议

这个仓库更适合作为一个 **可运行的工作区项目** 发布，而不是立即强行拆成多个独立仓库。这样可以保留已经验证通过的联调结构，降低复现成本。

发布时建议：

- 保留主流程代码和 companion 目录
- 在仓库首页说明这是 workspace / monorepo 结构
- 对外说明哪些目录是主 skill，哪些是集成依赖
- 检查依赖目录的原始来源和许可证要求

发布前请先查看：`RELEASE_CHECKLIST.md`

建议一并维护这些发布相关文件：

- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `GITHUB_RELEASE_TEMPLATE.md`

## 安全与隐私

请不要把以下内容提交到 GitHub：

- 阿里云密钥配置
- Bilibili 登录 Cookie / 凭证
- 本地 `output/` 运行结果
- 真实音频文件、临时切片、日志文件
- 本地缓存、虚拟环境、`node_modules/`

仓库已经通过 `.gitignore` 对这些内容做了默认忽略，但发布前仍建议手动检查一次。

## 常见问题

### 1. `bili` 命令不存在

请先安装 `bilibili-cli`，并确认：

```bash
bili --help
```

### 2. 提示未登录或无法获取字幕

先手动检查：

```bash
bili status
bili login
```

### 3. XMind 导出失败

通常是 `xmind-generator` 依赖未安装：

```bash
cd xmind-generator
npm install
```

### 4. Windows 上 ASR 不工作

优先检查：

- 阿里云配置文件是否存在
- `ALIYUN_ASR_CONFIG` 是否指向正确路径
- 配置中的 `access_key_id`、`access_key_secret`、`app_key` 是否有效

### 5. Linux / macOS 上 Parakeet 失败

主流程会自动回退到阿里云 ASR。如果回退也失败，检查：

- Parakeet 服务是否已启动
- 阿里云配置是否已准备
- 音频提取链路是否正常

## 当前状态

当前版本已经完成以下能力验证：

- 登录检查与扫码登录引导
- 视频详情 / 字幕 / AI 总结 / 评论抓取
- Windows / Linux / macOS 差异化 ASR 策略
- 字幕缺失时的音频回退与转写
- 自动生成 `outline.md`
- 自动导出 `.xmind`
- 视频标题命名输出文件

后续可以继续完善的方向包括：

- 更高质量的 ASR 去噪与摘要抽象
- 更多真实样例与回归测试
- 更稳定的章节标题抽取
- 更清晰的 OpenClaw 安装说明

## 致谢

这个项目的完整工作流建立在几个已有 skill / 工具之上，感谢它们提供的能力基础与启发：

- `bilibili-cli`：提供 Bilibili 登录、详情抓取、字幕、评论和音频提取能力
- `aliyun-asr`：提供云端音频文件转写能力，尤其适合 Windows 场景
- `parakeet-local-asr`：提供本地 ASR 能力，适合 Linux / macOS 优先使用
- `xmind-generator`：提供 `.xmind` 文件导出能力

`bili-mindmap` 的定位不是替代这些项目，而是把它们编排成一个可实际运行的 Bilibili 视频知识梳理工作流。

## 说明

如果这个仓库中包含来自其他技能或项目的目录，请在正式公开发布前，补充它们的原始来源、修改说明以及许可证信息。详见：`THIRD_PARTY_NOTICES.md`
