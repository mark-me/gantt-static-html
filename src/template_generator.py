"""Generate static HTML from Jinja templates with embedded CDN scripts."""

import json
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from config import Config
from bundle import bundle_css, bundle_js
import urllib.request
import sys


def download_script(url: str, timeout: int = 10) -> str:
    """Download script content from URL."""
    try:
        print(f"  Downloading: {url.split('/')[-1]}")
        response = urllib.request.urlopen(url, timeout=timeout)
        return response.read().decode('utf-8')
    except Exception as e:
        print(f"  ✗ Failed: {e}", file=sys.stderr)
        return ""


def generate_html(data: dict, enable_bundling: bool = True,
                  embed_cdn: bool = True) -> str:
    import urllib.request
    import sys

    env = Environment(loader=FileSystemLoader(Config.TEMPLATES_DIR), autoescape=True)
    template = env.get_template("gantt_content.html")
    tasks = _flatten_tasks(data["epics"])
    tasks_json = json.dumps(tasks, ensure_ascii=False)

    print(f"\n📦 embed_cdn={embed_cdn}, SCRIPT_URL={Config.SCRIPT_URL[:50]}...")

    moment_js = ""
    frappe_js = ""

    if embed_cdn:
        print("  Attempting to download Moment.js...")
        moment_url = "https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"
        try:
            moment_response = urllib.request.urlopen(moment_url, timeout=30)
            moment_js = moment_response.read().decode('utf-8')
            print(f"  ✓ Moment.js downloaded: {len(moment_js)} bytes")
        except Exception as e:
            print(f"  ✗ Moment.js download FAILED: {e}", file=sys.stderr)
            moment_js = ""

        print("  Attempting to download Frappe Gantt...")
        try:
            frappe_response = urllib.request.urlopen(Config.SCRIPT_URL, timeout=30)
            frappe_js = frappe_response.read().decode('utf-8')
            print(f"  ✓ Frappe Gantt downloaded: {len(frappe_js)} bytes")
        except Exception as e:
            print(f"  ✗ Frappe Gantt download FAILED: {e}", file=sys.stderr)
            frappe_js = ""
    else:
        print("  ⚠ embed_cdn=False, using CDN references")

    print(f"  Final moment_js: {'present' if moment_js else 'EMPTY'} ({len(moment_js)} chars)")
    print(f"  Final frappe_js: {'present' if frappe_js else 'EMPTY'} ({len(frappe_js)} chars)")

    # Get bundled custom CSS/JS
    bundled_css_content = ""
    bundled_js_content = ""

    if enable_bundling:
        css_files, js_files = get_bundled_resources()
        bundled_css_content = bundle_css(css_files)
        bundled_js_content = bundle_js(js_files)

    html = template.render(
        title=data.get("project_title", "Project Gantt"),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        tasks_json=tasks_json,
        total_epics=data.get("_metadata", {}).get("total_epics", 0),
        total_features=data.get("_metadata", {}).get("total_features", 0),
        cdn_script=Config.SCRIPT_URL,
        cdn_styles=Config.STYLES_URL,
        view_mode=Config.DEFAULT_VIEW_MODE,
        enable_bundling=enable_bundling,
        bundled_css=bundled_css_content,
        bundled_js=bundled_js_content,
        moment_inline=moment_js,
        frappe_inline=frappe_js,
        embed_cdn=embed_cdn
    )

    return html


def _flatten_tasks(epics: list) -> list:
    # Same as before...
    tasks = []
    for epic_idx, epic in enumerate(epics):
        feature_dates = [(f["start_date"], f["end_date"]) for f in epic.get("features", [])
                        if f.get("start_date") and f.get("end_date")]

        if feature_dates:
            sorted_dates = sorted(feature_dates, key=lambda x: x[0])
            epic_start = sorted_dates[0][0]
            epic_end = sorted(sorted_dates, key=lambda x: x[1])[-1][1]
        else:
            epic_start = epic.get("start_date", datetime.now().strftime("%Y-%m-%d"))
            epic_end = epic.get("end_date", epic_start)

        tasks.append({
            "id": epic["id"],
            "text": f"▶ {epic['name']}",
            "start_date": epic_start,
            "end_date": epic_end,
            "progress": epic.get("avg_progress", 0) / 100,
            "open": True,
            "color": epic["color"],
            "is_epic": True,
            "parent": None
        })

        for feature in epic.get("features", []):
            if feature.get("start_date") and feature.get("end_date"):
                tasks.append({
                    "id": feature["id"],
                    "text": feature["name"],
                    "start_date": feature["start_date"],
                    "end_date": feature["end_date"],
                    "progress": feature.get("progress", 0) / 100,
                    "open": True,
                    "color": None,
                    "is_epic": False,
                    "parent": epic["id"],
                    "status": feature.get("status", "pending")
                })

    return tasks


def get_bundled_resources():
    assets_dir = Path(Config.ASSETS_DIR)

    css_files = [
        str(assets_dir / "css" / "variables.css"),
        str(assets_dir / "css" / "layout.css"),
        str(assets_dir / "css" / "components.css"),
    ]

    js_files = [
        str(assets_dir / "js" / "theme.js"),
        str(assets_dir / "js" / "filters.js"),
        str(assets_dir / "js" / "gantt-init.js"),
    ]

    css_files = [f for f in css_files if Path(f).exists()]
    js_files = [f for f in js_files if Path(f).exists()]

    return css_files, js_files