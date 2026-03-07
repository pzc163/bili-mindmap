"""Aliyun ASR package entrypoints for file-based transcription."""

from .handle_media import handle_media

process_media = handle_media

__all__ = ["handle_media", "process_media"]
