import json
from pathlib import Path
from fastapi import HTTPException

BASE_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_json(relative_file_path: str):
    """
    Safely resolves and loads JSON fixtures from the data directory.
    Guards against directory traversal, missing files, and corrupted JSON.
    """
    resolved_base = BASE_DATA_DIR.resolve()
    target_path = (BASE_DATA_DIR / relative_file_path).resolve()

    # Guard against directory traversal
    try:
        target_path.relative_to(resolved_base)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Directory traversal attempt detected",
        )

    # Check if file exists
    if not target_path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Resource file not found: {relative_file_path}",
        )

    # Parse JSON
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Corrupted JSON fixture",
        )


def load_keyed_json(relative_file_path: str, event_id: str):
    """Loads a JSON file and returns the nested object keyed by event_id case-insensitively.

    Raises HTTP 404 if file does not exist or if event_id is not present.
    """
    data = load_json(relative_file_path)

    if isinstance(data, dict):
        norm_id = event_id.strip().lower()
        for k, v in data.items():
            if str(k).strip().lower() == norm_id:
                return v
        raise HTTPException(
            status_code=404,
            detail=(
                f"Event '{event_id}' not found in fixture"
                f" '{relative_file_path}'"
            ),
        )

    # If top-level is a list of objects with an 'id' or 'eventId' key
    if isinstance(data, list):
        norm_id = event_id.strip().lower()
        for item in data:
            if isinstance(item, dict):
                item_id = str(item.get("id") or item.get("eventId", "")).lower()
                if item_id == norm_id:
                    return item
        raise HTTPException(
            status_code=404,
            detail=(
                f"Event '{event_id}' not found in fixture list"
                f" '{relative_file_path}'"
            ),
        )

    raise HTTPException(
        status_code=500,
        detail=f"Fixture '{relative_file_path}' is not a keyed object or list",
    )
