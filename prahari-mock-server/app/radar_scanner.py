import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from app.loader import load_json, BASE_DATA_DIR

RADAR_FILENAME_REGEX = re.compile(
    r"^(?P<station>[a-zA-Z0-9_-]+)_(?P<product>[a-zA-Z0-9_-]+)_(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})T(?P<hour>\d{2})(?P<minute>\d{2})Z\.(?:png|jpg|jpeg)$",
    re.IGNORECASE,
)


def get_stations() -> List[Dict[str, Any]]:
    """Loads and returns the list of radar stations from data/radar/stations.json."""
    return load_json("radar/stations.json")


def parse_frame_filename(station_id: str, product: str, filename: str) -> Optional[Dict[str, Any]]:
    """
    Parses a radar image filename against the standard pattern:
    <stationId>_<product>_<YYYYMMDDTHHMMZ>.<ext>
    Returns metadata dict or None if filename does not match.
    """
    match = RADAR_FILENAME_REGEX.match(filename)
    if not match:
        return None

    year = match.group("year")
    month = match.group("month")
    day = match.group("day")
    hour = match.group("hour")
    minute = match.group("minute")

    timestamp_slug = f"{year}{month}{day}T{hour}{minute}Z"
    iso_timestamp = f"{year}-{month}-{day}T{hour}:{minute}:00Z"
    image_url = f"/static/radar/{station_id}/{product}/{filename}"

    return {
        "id": f"{station_id}_{product}_{timestamp_slug}",
        "timestamp": iso_timestamp,
        "imageUrl": image_url,
    }


def scan_radar_frames(
    station_id: str,
    product: str,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Scans radar image files for the given station and product,
    sorts them chronologically (oldest to newest), and applies optional time range and limit filters.
    """
    station_dir = BASE_DATA_DIR / "radar" / station_id.lower() / product.lower()
    if not station_dir.is_dir():
        return []

    frames: List[Dict[str, Any]] = []
    for file_path in station_dir.iterdir():
        if file_path.is_file():
            parsed = parse_frame_filename(station_id.lower(), product.lower(), file_path.name)
            if parsed:
                frames.append(parsed)

    # Sort chronologically (oldest to newest)
    frames.sort(key=lambda x: x["timestamp"])

    # Filter by from_time
    if from_time:
        frames = [f for f in frames if f["timestamp"] >= from_time]

    # Filter by to_time
    if to_time:
        frames = [f for f in frames if f["timestamp"] <= to_time]

    # Slice limit (most recent frames)
    if limit is not None and limit > 0:
        frames = frames[-limit:]

    return frames
