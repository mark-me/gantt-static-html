"""Configuration settings for the Gantt generator."""

from pathlib import Path


class Config:
    """Central configuration for Gantt chart generation. Defines file paths, asset locations, and default display options.

    This class groups constants used throughout the application to control how
    data is loaded, where output is written, and how the Gantt chart appears.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    # Input/Output paths (relative to project root)
    DATA_FILE = "project_data.json"
    OUTPUT_DIR = BASE_DIR / "output"
    OUTPUT_FILE = "project_gantt.html"

    # Template settings
    TEMPLATES_DIR = BASE_DIR / "src" / "templates"

    # Asset paths for bundling
    ASSETS_DIR = BASE_DIR / "assets"

    # Use Frappe Gantt URLs
    SCRIPT_URL = "https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.min.js"
    STYLES_URL = "https://cdn.jsdelivr.net/npm/frappe-gantt@0.6.1/dist/frappe-gantt.css"

    # Bundling settings
    ENABLE_BUNDLING = True  # Set False for dev testing

    # Gantt defaults
    DEFAULT_VIEW_MODE = "month"  # day, week, month
    DATE_FORMAT = "%Y-%m-%d"

    # Color scheme for epics
    EPIC_COLORS = [
        "#6d4aff",  # Purple
        "#4CAF50",  # Green
        "#FF9800",  # Orange
        "#E91E63",  # Pink
        "#2196F3",  # Blue
        "#9C27B0",  # Deep Purple
        "#00BCD4",  # Cyan
        "#795548",  # Brown
    ]