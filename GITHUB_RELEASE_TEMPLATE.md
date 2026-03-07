# GitHub Release Template

This file contains suggested metadata for the GitHub repository homepage and the first public release.

## Suggested Repository Description

Generate XMind mind maps from Bilibili videos with subtitle retrieval and ASR fallback for OpenClaw.

## Suggested Topics

- `bilibili`
- `mindmap`
- `xmind`
- `openclaw`
- `asr`
- `python`
- `workflow`
- `knowledge-management`

## Suggested Website

- Leave empty for now, or point to the repository itself

## Suggested First Release Title

`v0.1.0 - Initial public workspace release`

## Suggested First Release Notes

```md
## Highlights

- Add end-to-end Bilibili video to XMind workflow
- Support login check and QR-code login via `bilibili-cli`
- Collect video details, subtitles, AI summary, and hot comments
- Add subtitle-missing fallback with audio extraction and ASR transcription
- Prefer `aliyun-asr` on Windows
- Prefer `parakeet-local-asr` on Linux / macOS, with automatic fallback to `aliyun-asr`
- Generate `outline.md` and export `.xmind` mind maps
- Default `.xmind` filename now follows the video title

## Repository Structure

This release is published as a workspace / monorepo:

- `bili-mindmap` is the orchestration layer
- companion directories are included for integration and local reproduction

## Notes

- Review `RELEASE_CHECKLIST.md` before packaging future releases
- Review `THIRD_PARTY_NOTICES.md` before wider redistribution or commercial use
```
