"""Bundle external CSS/JS files into inline content for static HTML output."""

import sys
from pathlib import Path


def read_file(file_path: str) -> str:
    """Read file contents with UTF-8 encoding and error handling."""
    path = Path(file_path)
    if not path.exists():
        print(f"WARNING: File not found: {file_path}", file=sys.stderr)
        return ""

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"WARNING: Error reading {file_path}: {e}", file=sys.stderr)
        return ""


def bundle_css(css_files: list) -> str:
    """Combine multiple CSS files into one string."""
    combined = []

    for css_file in css_files:
        content = read_file(css_file).strip()
        if content:
            combined.append(f"/* {Path(css_file).name} */\n{content}\n")

    result = "\n".join(combined) if combined else ""
    if not result:
        print("WARNING: No CSS files were bundled!", file=sys.stderr)
    return result


def bundle_js(js_files: list) -> str:
    """Combine multiple JS files into one string."""
    combined = []

    for js_file in js_files:
        content = read_file(js_file).strip()
        if content:
            combined.append(f"// {Path(js_file).name}\n{content}\n")

    result = "\n".join(combined) if combined else ""
    if not result:
        print("WARNING: No JS files were bundled!", file=sys.stderr)
    return result