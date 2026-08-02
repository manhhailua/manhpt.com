#!/usr/bin/env python3
"""Validate repository-specific structure for a Docusaurus blog post."""

from __future__ import annotations

import argparse
import re
import struct
import sys
from pathlib import Path


REQUIRED_FIELDS = {"title", "authors", "tags", "date", "description"}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
POST_DIR_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-zA-Z0-9-]+$")
SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".svg", ".webp"}
TARGET_COVER_RATIO = 16 / 9
MIN_COVER_WIDTH = 1200
MIN_COVER_HEIGHT = 675
MAX_COVER_BYTES = 2 * 1024 * 1024


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_list(value: str, block_items: list[str]) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [
            unquote(item.strip())
            for item in value[1:-1].split(",")
            if item.strip()
        ]
    return [unquote(item) for item in block_items]


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], dict[str, list[str]], int]:
    if not lines or lines[0].strip() != "---":
        raise ValueError("File must start with YAML frontmatter delimited by '---'.")

    try:
        end = next(
            index for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ValueError("Frontmatter is missing its closing '---'.") from exc

    scalars: dict[str, str] = {}
    blocks: dict[str, list[str]] = {}
    current_key: str | None = None
    block_scalar_key: str | None = None

    for line in lines[1:end]:
        field = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s*(.*))?$", line)
        if field:
            current_key = field.group(1)
            value = (field.group(2) or "").strip()
            block_scalar_key = current_key if value in {">", ">-", "|", "|-", "|+"} else None
            scalars[current_key] = "" if block_scalar_key else value
            blocks.setdefault(current_key, [])
            continue

        item = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item and current_key:
            blocks[current_key].append(item.group(1))
            continue

        if block_scalar_key and line.startswith((" ", "\t")):
            continuation = line.strip()
            if continuation:
                scalars[block_scalar_key] = " ".join(
                    part for part in (scalars[block_scalar_key], continuation) if part
                )

    return scalars, blocks, end


def load_declared_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        match.group(1).strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := re.match(r"^([^\s][^:]*):\s*$", line))
    }


def find_repo_root(post: Path) -> Path:
    for parent in [post.parent, *post.parents]:
        if (parent / "blog" / "tags.yml").exists():
            return parent
    return Path.cwd()


def prose_lines(lines: list[str]) -> list[str]:
    """Return lines outside fenced code blocks."""
    result: list[str] = []
    active_fence: str | None = None

    for line in lines:
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)[0]
            active_fence = None if active_fence == marker else marker
            continue
        if active_fence is None:
            result.append(line)

    return result


def svg_dimensions(data: bytes) -> tuple[int, int] | None:
    text = data.decode("utf-8", errors="ignore")
    root = re.search(r"<svg\b[^>]*>", text, flags=re.IGNORECASE | re.DOTALL)
    if not root:
        return None

    tag = root.group(0)

    def numeric_attribute(name: str) -> float | None:
        match = re.search(
            rf"\b{name}\s*=\s*['\"]\s*([0-9]+(?:\.[0-9]+)?)\s*(?:px)?\s*['\"]",
            tag,
            flags=re.IGNORECASE,
        )
        return float(match.group(1)) if match else None

    width = numeric_attribute("width")
    height = numeric_attribute("height")
    if width and height:
        return round(width), round(height)

    viewbox = re.search(
        r"\bviewBox\s*=\s*['\"]\s*[-0-9.]+[ ,]+[-0-9.]+[ ,]+([0-9.]+)[ ,]+([0-9.]+)\s*['\"]",
        tag,
        flags=re.IGNORECASE,
    )
    if viewbox:
        return round(float(viewbox.group(1))), round(float(viewbox.group(2)))
    return None


def webp_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 20 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None

    cursor = 12
    while cursor + 8 <= len(data):
        chunk_type = data[cursor:cursor + 4]
        chunk_size = int.from_bytes(data[cursor + 4:cursor + 8], "little")
        start = cursor + 8
        payload = data[start:start + chunk_size]

        if chunk_type == b"VP8X" and len(payload) >= 10:
            width = int.from_bytes(payload[4:7], "little") + 1
            height = int.from_bytes(payload[7:10], "little") + 1
            return width, height
        if chunk_type == b"VP8L" and len(payload) >= 5 and payload[0] == 0x2F:
            bits = int.from_bytes(payload[1:5], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if chunk_type == b"VP8 " and len(payload) >= 10:
            signature = payload.find(b"\x9d\x01\x2a", 0, 10)
            if signature >= 0 and signature + 7 <= len(payload):
                width = int.from_bytes(payload[signature + 3:signature + 5], "little") & 0x3FFF
                height = int.from_bytes(payload[signature + 5:signature + 7], "little") & 0x3FFF
                return width, height

        cursor = start + chunk_size + (chunk_size % 2)
    return None


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    if not data.startswith(b"\xff\xd8"):
        return None

    start_of_frame = {
        0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
    }
    cursor = 2
    while cursor < len(data):
        if data[cursor] != 0xFF:
            cursor += 1
            continue
        while cursor < len(data) and data[cursor] == 0xFF:
            cursor += 1
        if cursor >= len(data):
            break

        marker = data[cursor]
        cursor += 1
        if marker in {0xD8, 0xD9}:
            continue
        if cursor + 2 > len(data):
            break

        segment_length = int.from_bytes(data[cursor:cursor + 2], "big")
        if segment_length < 2 or cursor + segment_length > len(data):
            break
        if marker in start_of_frame and segment_length >= 7:
            height = int.from_bytes(data[cursor + 3:cursor + 5], "big")
            width = int.from_bytes(data[cursor + 5:cursor + 7], "big")
            return width, height
        cursor += segment_length
    return None


def image_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None

    suffix = path.suffix.lower()
    if suffix == ".png" and len(data) >= 24 and data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_dimensions(data)
    if suffix == ".webp":
        return webp_dimensions(data)
    if suffix == ".svg":
        return svg_dimensions(data)
    return None


def validate(post: Path, repo_root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        text = post.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read {post}: {exc}"], warnings

    lines = text.splitlines()
    try:
        fields, blocks, frontmatter_end = parse_frontmatter(lines)
    except ValueError as exc:
        return [str(exc)], warnings

    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        errors.append(f"Missing frontmatter fields: {', '.join(missing)}.")

    for key in ("title", "date", "description"):
        if key in fields and not unquote(fields[key]):
            errors.append(f"Frontmatter field '{key}' must not be empty.")

    date = unquote(fields.get("date", ""))
    if date and not DATE_PATTERN.fullmatch(date):
        errors.append("Date must use YYYY-MM-DD.")

    directory_match = POST_DIR_PATTERN.fullmatch(post.parent.name)
    if post.name != "index.md":
        warnings.append("Project convention uses index.md inside a dated post directory.")
    if not directory_match:
        warnings.append("Post directory should use YYYY-MM-DD-slug.")
    elif date and directory_match.group(1) != date:
        errors.append(
            f"Frontmatter date {date} does not match directory date "
            f"{directory_match.group(1)}."
        )

    slug = unquote(fields.get("slug", ""))
    if slug and not SLUG_PATTERN.fullmatch(slug):
        errors.append("Slug must be lowercase ASCII kebab-case.")

    authors = parse_list(fields.get("authors", ""), blocks.get("authors", []))
    declared_authors = load_declared_keys(repo_root / "blog" / "authors.yml")
    if not authors:
        errors.append("At least one author is required.")
    for author in authors:
        if declared_authors and author not in declared_authors:
            errors.append(f"Unknown author '{author}' in blog/authors.yml.")

    tags = parse_list(fields.get("tags", ""), blocks.get("tags", []))
    declared_tags = load_declared_keys(repo_root / "blog" / "tags.yml")
    if not tags:
        errors.append("At least one tag is required.")
    for tag in tags:
        if declared_tags and tag not in declared_tags:
            errors.append(f"Unknown tag '{tag}' in blog/tags.yml.")

    body_lines = lines[frontmatter_end + 1:]
    body = "\n".join(body_lines)
    prose = prose_lines(body_lines)
    prose_body = "\n".join(prose)
    truncate_count = body.count("<!-- truncate -->")
    if truncate_count != 1:
        errors.append(
            f"Expected exactly one '<!-- truncate -->' marker; found {truncate_count}."
        )
    else:
        truncate_line = next(
            index for index, line in enumerate(body_lines)
            if "<!-- truncate -->" in line
        )
        first_h2 = next(
            (index for index, line in enumerate(body_lines) if line.startswith("## ")),
            None,
        )
        if first_h2 is not None and truncate_line > first_h2:
            errors.append("The truncate marker must appear before the first H2.")

    if any(line.startswith("# ") for line in prose):
        errors.append("Do not use an H1 in the post body; the title comes from frontmatter.")

    if not any(line.startswith("## ") for line in prose):
        warnings.append("The post has no H2 sections.")

    fence_count = sum(
        1 for line in body_lines if re.match(r"^\s*(?:`{3,}|~{3,})", line)
    )
    if fence_count % 2:
        errors.append("Code fences appear to be unbalanced.")

    description = unquote(fields.get("description", ""))
    if description and not 100 <= len(description) <= 180:
        warnings.append(
            f"Description is {len(description)} characters; aim for roughly 100–180."
        )

    if re.search(r"\b(?:TODO|TBD|FIXME)\b", prose_body, flags=re.IGNORECASE):
        errors.append("Remove TODO, TBD, or FIXME placeholders before publishing.")

    image = unquote(fields.get("image", ""))
    image_path: Path | None = None
    if not image:
        errors.append("Frontmatter field 'image' is required for the cover image.")
    elif image.startswith("./"):
        image_path = post.parent / image[2:]
        if not image_path.exists():
            errors.append(f"Relative image does not exist: {image}.")
    elif image.startswith("/"):
        image_path = repo_root / "static" / image.lstrip("/")
        if not image_path.exists():
            errors.append(f"Static image does not exist: {image}.")
    else:
        errors.append(
            "Cover image must be a repository-local './...' or '/img/...' path."
        )

    if image_path and image_path.exists():
        suffix = image_path.suffix.lower()
        if suffix not in SUPPORTED_IMAGE_SUFFIXES:
            errors.append(
                f"Unsupported cover format '{suffix or '(none)'}'; use WebP, PNG, JPEG, or SVG."
            )
        else:
            dimensions = image_dimensions(image_path)
            if dimensions:
                width, height = dimensions
                ratio_error = abs((width / height) - TARGET_COVER_RATIO) / TARGET_COVER_RATIO
                if ratio_error > 0.03:
                    warnings.append(
                        f"Cover is {width}x{height}; use a 16:9 aspect ratio."
                    )
                if width < MIN_COVER_WIDTH or height < MIN_COVER_HEIGHT:
                    warnings.append(
                        f"Cover is {width}x{height}; use at least "
                        f"{MIN_COVER_WIDTH}x{MIN_COVER_HEIGHT}."
                    )
            else:
                warnings.append(f"Could not determine cover dimensions: {image}.")

            if image_path.stat().st_size > MAX_COVER_BYTES:
                warnings.append("Cover exceeds 2 MB; optimize it before publishing.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a manhpt.com Docusaurus blog post."
    )
    parser.add_argument("post", type=Path, help="Path to blog post index.md")
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root; auto-detected when omitted.",
    )
    args = parser.parse_args()

    post = args.post.resolve()
    repo_root = (
        args.repo_root.resolve() if args.repo_root else find_repo_root(post).resolve()
    )
    errors, warnings = validate(post, repo_root)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"OK: {post} ({len(warnings)} warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
