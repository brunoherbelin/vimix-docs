#!/usr/bin/env python3
"""Resize and compress documentation screenshots to the size limits of check_pages.py.

Usage: python3 scripts/optimize_images.py   (run from the repository root; needs Pillow)
Only images over the limits are modified, so running it twice changes nothing.
"""
import sys
from pathlib import Path

from PIL import Image

from check_pages import MAX_BYTES, MAX_WIDTH, ROOT


def optimize(path):
    """Shrink one PNG in place. Return True if the file was modified."""
    if path.stat().st_size <= MAX_BYTES:
        with Image.open(path) as probe:
            if probe.width <= MAX_WIDTH:
                return False
    with Image.open(path) as img:
        img.load()
        if img.width > MAX_WIDTH:
            height = round(img.height * MAX_WIDTH / img.width)
            img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB").resize(
                (MAX_WIDTH, height), Image.LANCZOS)
        img.save(path, optimize=True)
        if path.stat().st_size > MAX_BYTES:
            # screenshots have few colours: a 256-colour palette is nearly lossless
            img.convert("RGBA" if "A" in img.getbands() else "RGB").quantize(256).save(path, optimize=True)
    return True


def main():
    status = 0
    for path in sorted((ROOT / "pages").rglob("img/*.png")):
        before = path.stat().st_size
        if optimize(path):
            after = path.stat().st_size
            print(f"optimized {path.relative_to(ROOT)}: {before // 1024} KB -> {after // 1024} KB")
            if after > MAX_BYTES:
                print(f"WARNING {path.relative_to(ROOT)} is still above {MAX_BYTES // 1024} KB")
    return status


if __name__ == "__main__":
    sys.exit(main())
