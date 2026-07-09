#!/usr/bin/env python3
"""
Main entry point for generating static Gantt chart HTML.
Loads epic data from JSON and outputs a self-contained HTML file.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config import Config
from data_loader import load_epic_data
from template_generator import generate_html


def main():
    """Main execution flow."""
    print("=" * 60)
    print("Gantt Chart Generator")
    print("=" * 60)

    # Validate input file exists
    if not Path(Config.DATA_FILE).exists():
        print(f"❌ Error: Data file not found at '{Config.DATA_FILE}'")
        sys.exit(1)

    # Load and validate epic data
    print(f"\n📥 Loading data from: {Config.DATA_FILE}")
    try:
        data = load_epic_data(Config.DATA_FILE)
        print(f"   ✓ Loaded {len(data.get('epics', []))} epic(s)")

        total_features = sum(len(epic.get('features', [])) for epic in data.get('epics', []))
        print(f"   ✓ Found {total_features} feature(s) total")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)

    # Create output directory if needed
    output_dir = Path(Config.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 Output directory: {output_dir}")

    # Generate HTML (with CDN scripts embedded for offline use)
    print("\n🎨 Generating HTML (embedding CDN scripts)...")
    try:
        html_output = generate_html(data, enable_bundling=True, embed_cdn=True)
    except Exception as e:
        print(f"❌ Error generating HTML: {e}")
        sys.exit(1)

    # Write to file
    output_path = output_dir / Config.OUTPUT_FILE
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"\n✅ Success! Generated: {output_path.resolve()}")
    print("   📤 Share this file via email (opens in any browser)")
    print("=" * 60)


if __name__ == "__main__":
    main()