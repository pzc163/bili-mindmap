#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Markdown outline into an XMind file.")
    parser.add_argument("--outline", required=True, help="Markdown outline file")
    parser.add_argument("--output", required=True, help="Target .xmind file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    outline = Path(args.outline).resolve()
    output = Path(args.output).resolve()
    generator_dir = root / "xmind-generator"
    generator_script = generator_dir / "scripts" / "generate_xmind.js"

    if not outline.exists():
        raise SystemExit(f"Outline file not found: {outline}")
    if not generator_script.exists():
        raise SystemExit(f"Generator script not found: {generator_script}")
    if not shutil.which("node"):
        raise SystemExit("Missing required command: node")

    output.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["node", str(generator_script), "--input", str(outline), "--output", str(output)],
        cwd=generator_dir,
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
