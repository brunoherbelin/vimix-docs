#!/usr/bin/env python3
"""Validate documentation pages: front matter, image references, alt texts, image size (oversized images only warn: they are optimized after merge).

Usage: python3 scripts/check_pages.py   (run from the repository root)
"""
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ("title", "summary", "author", "vimix_version", "date")
MAX_BYTES = 300 * 1024  # soft limits: larger images are resized by scripts/optimize_images.py
MAX_WIDTH = 1600
HARD_MAX_BYTES = 10 * 1024 * 1024  # hard limits: rejected
HARD_MAX_WIDTH = 5000
IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)\)")


def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip().strip('"')
    return meta


def png_width(path):
    with open(path, "rb") as f:
        header = f.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">I", header[16:20])[0]


def check_page(page):
    errors = []
    text = page.read_text(encoding="utf-8")
    meta = front_matter(text)
    if meta is None:
        return [f"{page}: missing front matter"]
    for key in REQUIRED:
        if not meta.get(key):
            errors.append(f"{page}: front matter '{key}' is missing or empty")
    if meta.get("date") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["date"]):
        errors.append(f"{page}: 'date' must be YYYY-MM-DD")
    for heading in ("## What it does", "## How to", "## Specific information"):
        if heading not in text:
            errors.append(f"{page}: missing section '{heading}'")
    for m in IMAGE_RE.finditer(text):
        if not m.group("alt").strip():
            errors.append(f"{page}: image {m.group('src')} has no alt text")
        if not m.group("src").startswith("http") and not (page.parent / m.group("src")).is_file():
            errors.append(f"{page}: image {m.group('src')} not found")
    return errors


def check_image(img):
    """Return (errors, warnings) for one image."""
    errors, warnings = [], []
    if img.suffix.lower() != ".png":
        return [f"{img}: only PNG images are accepted"], warnings
    size = img.stat().st_size
    width = png_width(img)
    if width is None:
        return [f"{img}: not a valid PNG file"], warnings
    if size > HARD_MAX_BYTES:
        errors.append(f"{img}: {size // 1024} KB exceeds {HARD_MAX_BYTES // 1024} KB")
    elif size > MAX_BYTES:
        warnings.append(f"{img}: {size // 1024} KB exceeds {MAX_BYTES // 1024} KB (will be optimized after merge)")
    if width > HARD_MAX_WIDTH:
        errors.append(f"{img}: width {width} px exceeds {HARD_MAX_WIDTH} px")
    elif width > MAX_WIDTH:
        warnings.append(f"{img}: width {width} px exceeds {MAX_WIDTH} px (will be resized after merge)")
    return errors, warnings


def main():
    errors, warnings = [], []
    pages = sorted((ROOT / "pages").rglob("index.md"))
    for page in pages:
        errors += check_page(page)
    for img in sorted((ROOT / "pages").rglob("img/*")):
        if img.is_file() and img.name != ".gitkeep":
            e, w = check_image(img)
            errors += e
            warnings += w
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(pages)} page(s) checked, {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
