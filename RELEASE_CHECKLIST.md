# 发布前清单

适用于把当前 `bili-mindmap` 工作区上传到 GitHub 前的自检。

## 1. 敏感信息检查

- 确认没有提交任何真实密钥、令牌、Cookie、账号信息。
- 不要提交本机配置文件，例如：
  - `~/.openclaw/aliyun-asr-config.json`
  - `%USERPROFILE%\.openclaw\aliyun-asr-config.json`
  - `~/.bilibili-cli/credential.json`
  - `%USERPROFILE%\.bilibili-cli\credential.json`
- 仓库内如果手动复制过配置文件，只保留示例文件，例如 `aliyun-asr/example-config.json`。

## 2. 生成产物检查

- 不要提交 `output/` 下的测试结果。
- 不要提交本地导出的 `.xmind`、音频切片、转写文本、日志文件。
- 不要提交临时调试目录，例如 `tmp-outline-sample/`、`tmp-outline-sample2/`、`tmp/`。

## 3. 依赖与缓存检查

- 不要提交 `node_modules/`。
- 不要提交 Python 缓存，例如 `__pycache__/`、`.pytest_cache/`、`.mypy_cache/`、`.ruff_cache/`。
- 不要提交本地虚拟环境，例如 `.venv/`、`venv/`、`env/`。

## 4. 仓库说明检查

- 在 `README.md` 中明确说明这是一个 `workspace / monorepo` 风格项目。
- 写清楚各目录职责：
  - `SKILL.md`、`agents/`、`scripts/`、`references/`：`bili-mindmap` 主体
  - `bilibili-cli/`、`aliyun-asr/`、`parakeet-local-asr/`、`xmind-generator/`：集成依赖或 companion skills
- 如果依赖目录来自其他仓库，补充原始来源和许可证说明。

## 5. 发布前本地检查

- 新建 Git 仓库后先执行：`git status --short`
- 再执行：`git add .`
- 然后执行：`git status --short`
- 重点确认以下内容没有进入暂存区：
  - `output/`
  - `node_modules/`
  - 任意 `.xmind`、音频、日志、凭证文件

## 6. 建议的首发内容

- 建议首发只包含：
  - 源码
  - `SKILL.md`
  - `README.md`
  - 示例配置模板
  - 必要的说明文档
- 建议不要首发提交真实测试输出，避免仓库体积过大，也避免泄露账号和使用痕迹。
