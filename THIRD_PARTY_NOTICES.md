# Third-Party Notices

This repository is organized as a workspace / monorepo. It contains original `bili-mindmap` orchestration files together with companion skills or local copies of upstream projects.

## Scope

- Top-level orchestration files such as `README.md`, `SKILL.md`, `agents/`, `references/`, and `scripts/` are the `bili-mindmap` project itself.
- Some subdirectories may come from upstream projects, or may be adapted local copies used for integration and testing.

## Included Components

### `bilibili-cli/`

- Role: Bilibili login, metadata retrieval, subtitles, comments, audio extraction
- Local status: bundled as a source directory inside this workspace
- License status: contains `bilibili-cli/LICENSE`
- Observed license: Apache License 2.0

### `aliyun-asr/`

- Role: cloud-based audio file transcription fallback, especially for Windows
- Local status: bundled as a source directory inside this workspace
- License status: no separate top-level `LICENSE` file found in the current bundled snapshot
- Recommendation: verify upstream repository ownership and intended license before wider redistribution or commercial use

### `parakeet-local-asr/`

- Role: local ASR workflow for Linux / macOS
- Local status: bundled as a source directory inside this workspace
- License status: no separate top-level `LICENSE` file found in the current bundled snapshot
- Recommendation: verify upstream repository ownership and intended license before wider redistribution or commercial use

### `xmind-generator/`

- Role: export Markdown outline to `.xmind`
- Local status: bundled as a source directory inside this workspace
- License status: no separate top-level `LICENSE` file found in the current bundled snapshot
- Recommendation: verify upstream repository ownership and intended license before wider redistribution or commercial use

## Publication Notes

- If you continue to publish this repository publicly, keep this file updated when companion components change.
- If you later split the repository into multiple standalone projects, add a dedicated `LICENSE` to each independently maintained project.
- If any bundled component has an upstream `NOTICE`, attribution requirement, or trademark restriction, preserve it in future releases.
