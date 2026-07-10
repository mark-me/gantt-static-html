"""Load and validate epic data from JSON files."""

import json
from pathlib import Path
from typing import Any

from config import Config


def load_epic_data(file_path: str) -> dict[str, Any]:
    """
    Load epic data from JSON file and return validated structure.

    Expected JSON format:
    {
        "project_title": "My Project",
        "epics": [
            {
                "id": "EPIC-1",
                "name": "Mobile App Launch",
                "color": "#6d4aff",
                "features": [
                    {
                        "id": "FEATURE-1",
                        "name": "User Authentication",
                        "start_date": "2026-07-01",
                        "end_date": "2026-07-10",
                        "progress": 80,
                        "status": "completed"
                    }
                ]
            }
        ]
    }
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # Validate and normalize structure
    data = _normalize_data(raw_data)

    # Assign colors if not specified
    _assign_colors(data)

    return data


def _normalize_data(raw_data: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize raw epic JSON data into a consistent internal structure. Derive
    default values and aggregate metadata for epics and features.

    This function ensures all epics and features have required fields, filters
    out features without complete date ranges, and calculates epic-level
    progress metrics.

    Args:
        raw_data: Raw data loaded from the epic JSON file.

    Returns:
        A normalized data structure with epics, features, and metadata.
    """
    normalized = {
        "project_title": raw_data.get("project_title", "Project Gantt Chart"),
        "epics": [],
        "_metadata": {
            "generated_date": None,  # Will be set in template
            "total_epics": 0,
            "total_features": 0,
        },
    }

    for epic in raw_data.get("epics", []):
        normalized_epic = {
            "id": epic.get("id", f"EPIC-{len(normalized['epics']) + 1}"),
            "name": epic.get("name", "Untitled Epic"),
            "color": epic.get("color"),
            "description": epic.get("description", ""),
            "url": epic.get("url"),
            "features": [],
        }

        total_progress = 0
        feature_count = 0

        for feature in epic.get("features", []):
            normalized_feature = {
                "id": feature.get("id", f"F-{len(normalized_epic['features']) + 1}"),
                "name": feature.get("name", "Untitled Feature"),
                "start_date": feature.get("start_date"),
                "end_date": feature.get("end_date"),
                "progress": feature.get("progress", 0),
                "status": feature.get("status", "pending"),
                "description": feature.get("description", ""),
                "url": feature.get("url"),
            }

            if normalized_feature["start_date"] and normalized_feature["end_date"]:
                normalized_epic["features"].append(normalized_feature)
                total_progress += normalized_feature.get("progress", 0)
                feature_count += 1

        # Calculate epic-level metrics
        if feature_count > 0:
            normalized_epic["avg_progress"] = round(total_progress / feature_count)
        else:
            normalized_epic["avg_progress"] = 0

        normalized["epics"].append(normalized_epic)
        normalized["_metadata"]["total_epics"] += 1
        normalized["_metadata"]["total_features"] += feature_count

    return normalized


def _assign_colors(data: dict[str, Any]) -> None:
    """
    Assign default colors to epics that do not specify their own color. Ensure
    each epic receives a visually distinct color by cycling through a preset list.

    This function updates the input data structure in place and leaves existing
    epic color values unchanged.

    Args:
        data: Normalized epic data containing an "epics" list to be updated.
    """

    for idx, epic in enumerate(data.get("epics", [])):
        if not epic.get("color"):
            epic["color"] = Config.EPIC_COLORS[idx % len(Config.EPIC_COLORS)]


    for idx, epic in enumerate(data.get("epics", [])):
        if not epic.get("color"):
            epic["color"] = Config.EPIC_COLORS[idx % len(Config.EPIC_COLORS)]


def save_sample_data(file_path: str) -> None:
    """Save a sample JSON file for testing."""
    sample_data = {
        "project_title": "Sample Product Roadmap",
        "epics": [
            {
                "id": "EPIC-1",
                "name": "🚀 Mobile App Launch",
                "description": "Launch cross-platform mobile application",
                "features": [
                    {
                        "id": "FEATURE-1",
                        "name": "User Authentication",
                        "start_date": "2026-07-01",
                        "end_date": "2026-07-10",
                        "progress": 100,
                        "status": "completed",
                    },
                    {
                        "id": "FEATURE-2",
                        "name": "Push Notifications",
                        "start_date": "2026-07-08",
                        "end_date": "2026-07-20",
                        "progress": 60,
                        "status": "in_progress",
                    },
                    {
                        "id": "FEATURE-3",
                        "name": "Payment Integration",
                        "start_date": "2026-07-15",
                        "end_date": "2026-08-05",
                        "progress": 30,
                        "status": "in_progress",
                    },
                ],
            },
            {
                "id": "EPIC-2",
                "name": "📊 Analytics Dashboard",
                "description": "Build real-time analytics platform",
                "features": [
                    {
                        "id": "FEATURE-4",
                        "name": "Data Pipeline",
                        "start_date": "2026-07-10",
                        "end_date": "2026-07-25",
                        "progress": 80,
                        "status": "in_progress",
                    },
                    {
                        "id": "FEATURE-5",
                        "name": "Visualization Components",
                        "start_date": "2026-07-20",
                        "end_date": "2026-08-10",
                        "progress": 40,
                        "status": "in_progress",
                    },
                ],
            },
        ],
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2)

    print(f"✅ Sample data saved to: {file_path}")
