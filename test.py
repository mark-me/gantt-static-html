
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))
# Add to main.py before generating HTML
print("\n🔍 Verifying asset files:")
from pathlib import Path
from config import Config

assets_dir = Path(Config.ASSETS_DIR)
print(f"Assets directory: {assets_dir}")
print(f"Exists: {assets_dir.exists()}")

for subdir in ["css", "js"]:
    subpath = assets_dir / subdir
    print(f"\n  {subdir}/:")
    print(f"    Exists: {subpath.exists()}")
    if subpath.exists():
        for f in subpath.glob("*.css" if subdir == "css" else "*.js"):
            print(f"    ✓ {f.name}")
    else:
        print(f"    ⚠ Create this folder with the expected files!")