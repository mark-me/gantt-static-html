# Gantt Chart Generator

A Python-based static HTML Gantt chart generator that creates self-contained, email-friendly project roadmaps with collapsible epics, status filtering, and dark mode support.

## ✨ Features

* ✨ Collapsible Epic/Feature Hierarchies - Organize tasks by epic categories
* 🎨 Dark Mode Toggle - Persists across sessions with localStorage
* 🔍 Status Filtering - Filter by Completed, In Progress, or Pending
* 📱 Single Static HTML File - Works without servers, perfect for email distribution
* 🌐 Responsive Design - Works on desktop and mobile browsers
* 💾 Offline Ready - All scripts embedded in generated HTML (no CDN dependency)
* 🖨️ Print Support - Clean print layout via browser print dialog

## 🚀 Quick Start

### Installation

You can use either pip (traditional) or uv (modern, fast package manager):

#### Using uv (Recommended)

```bash
# Install uv (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip:
pip install uv

# Then install this project
uv sync

# Or if you cloned the repo:
git clone https://github.com/yourusername/gantt-static-html.git
cd gantt-static-html
uv sync
```

> 💡 Tip: uv is 10-100x faster than pip and handles lock files automatically. See Installation Guide for more details.

## Generate Your Gantt Chart

1. **Edit your data**: Modify project_data.json with your epic/feature information
2. **Generate HTML**:

   ```bash
   # Using uv
    uv run python main.py

    # Using pip
    python main.py
    ```

3. **Output**: Find `output/project_gantt.html` - ready to share!

## Project Structure

```bash
gantt-static-html/
├── main.py                     # Entry point
├── pyproject.toml             # Project metadata (uv/pip compatible)
├── uv.lock                    # Locked dependencies (uv only)
├── README.md                  # This file
├── LICENSE                    # MIT license
├── .gitignore               # Git ignore patterns
├── output/                   # Generated HTML output
│   └── project_gantt.html    # (created on build)
├── src/                      # Application source
│   ├── __init__.py
│   ├── config.py            # Configuration settings
│   ├── data_loader.py       # JSON data loading/validation
│   ├── template_generator.py # HTML rendering logic
│   ├── bundle.py            # CSS/JS bundling for offline use
│   └── templates/
│       ├── base.html        # Base template (theme/toggle)
│       └── gantt_content.html
├── assets/                   # Source assets (bundled at build)
│   ├── css/
│   │   ├── variables.css    # CSS variables & theming
│   │   ├── layout.css       # Layout components
│   │   └── components.css   # Buttons, badges, etc.
│   └── js/
│       ├── theme.js         # Dark mode functionality
│       ├── filters.js       # Status filtering logic
│       └── gantt-init.js    # Gantt initialization
└── docs/                     # Detailed documentation
    ├── index.md             # Documentation home
    ├── installation.md      # pip/uv installation guide
    ├── data-schema.md       # JSON data reference
    ├── customization.md     # Theme & behavior customization
    ├── troubleshooting.md   # Common issues
    └── api.md               # Advanced configuration API
```

## Requirements

* Python 3.11+
* One of the following:
  * pip (standard) + requirements.txt
  * uv (recommended) + pyproject.toml + uv.lock

## Configuration

### Basic Configuration

Edit `src/config.py` for common settings:

```python
class Config:
    # Input/Output paths
    DATA_FILE = "project_data.json"
    OUTPUT_DIR = BASE_DIR / "output"
    OUTPUT_FILE = "project_gantt.html"

    # View mode (day, week, month, quarter)
    DEFAULT_VIEW_MODE = "month"

    # Color palette for epics
    EPIC_COLORS = ["#6d4aff", "#4CAF50", "#FF9800", "#E91E63"]

    # Enable/disable script bundling
    ENABLE_BUNDLING = True
```

### Advanced Configuration

* Custom CSS theming
* Adding new task statuses
* Modifying JavaScript behavior
* Disabling CDN embedding
* Performance tuning

## Data Format

Your `project_data.json` should follow this schema:

```json
{
  "project_title": "Q3 2026 Product Roadmap",
  "epics": [
    {
      "id": "EPIC-1",
      "name": "🚀 Mobile App Launch",
      "description": "Cross-platform mobile application",
      "features": [
        {
          "id": "FEATURE-1",
          "name": "User Authentication",
          "start_date": "2026-07-01",
          "end_date": "2026-07-10",
          "progress": 100,
          "status": "completed"
        },
        {
          "id": "FEATURE-2",
          "name": "Push Notifications",
          "start_date": "2026-07-08",
          "end_date": "2026-07-20",
          "progress": 60,
          "status": "in_progress"
        }
      ]
    }
  ]
}
```

> **Full schema reference**: docs/data-schema.md

## Troubleshooting

Common issues and solutions:

| Problem                 | Solution                                               |
|-------------------------|--------------------------------------------------------|
| Gantt not displaying    | Check browser console (F12) for errors                 |
| Scripts not loading     | Use HTTP server or enable `embed_cdn=True`             |
| Dark mode not persisting| Verify `localStorage` is enabled                       |
| UV sync fails           | Delete `uv.lock` and run `uv sync --reinstall`         |
| `pip install` fails     | Use `pip install -r requirements.txt`                  |

## Development

Setting Up Development Environment

### Using uv

```bash
uv venv
source .venv/bin/activate
uv sync
```
