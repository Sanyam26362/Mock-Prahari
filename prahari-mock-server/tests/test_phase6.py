import json
import os
import subprocess
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_radar_sources_config():
    config_file = PROJECT_ROOT / "config" / "radar_sources.json"
    assert config_file.is_file(), "config/radar_sources.json does not exist"

    with open(config_file, "r", encoding="utf-8") as f:
        sources = json.load(f)

    assert isinstance(sources, list)
    assert len(sources) >= 2

    stations_file = PROJECT_ROOT / "data" / "radar" / "stations.json"
    with open(stations_file, "r", encoding="utf-8") as f:
        stations = json.load(f)
    valid_station_ids = {s["id"].lower() for s in stations}

    for src in sources:
        assert src["stationId"].lower() in valid_station_ids, f"Invalid stationId in config: {src['stationId']}"
        assert src["product"].lower() in {"reflectivity", "velocity"}, f"Invalid product: {src['product']}"
        assert "sourceUrl" in src
        assert "enabled" in src
    print("PASS: config/radar_sources.json is valid and aligned with stations.json")


def test_capture_radar_and_dynamic_discovery():
    script_path = PROJECT_ROOT / "scripts" / "capture_radar.py"
    assert script_path.is_file(), "scripts/capture_radar.py does not exist"

    # Run capture_radar.py --once --simulate
    cmd = [sys.executable, str(script_path), "--once", "--simulate"]
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True)
    assert result.returncode == 0, f"capture_radar failed with output: {result.stderr}"
    assert "Captured" in result.stdout

    # Query frames endpoint via TestClient to verify dynamic hot discovery
    res = client.get("/api/radar/kolkata/frames?product=reflectivity")
    assert res.status_code == 200
    frames = res.json()["frames"]
    assert len(frames) >= 4, f"Expected at least 4 frames after capture, got {len(frames)}"

    # Ensure timestamps are strictly sorted ascending
    timestamps = [f["timestamp"] for f in frames]
    assert timestamps == sorted(timestamps)

    # Verify latest frame endpoint points to the newest frame
    latest_res = client.get("/api/radar/kolkata/latest?product=reflectivity")
    assert latest_res.status_code == 200
    latest_frame = latest_res.json()
    assert latest_frame["timestamp"] == timestamps[-1]
    print(f"PASS: Dynamic frame discovery verified ({len(frames)} frames sorted, latest: {latest_frame['timestamp']})")


def test_readme_coverage():
    readme_path = PROJECT_ROOT / "README.md"
    assert readme_path.is_file(), "README.md does not exist"
    content = readme_path.read_text(encoding="utf-8")

    assert "Prahari" in content, "Missing project title in README"
    assert "26078" in content, "Missing SIH problem statement ID in README"
    assert "GNN" in content or "Diffusion" in content, "Missing AI architecture in README"
    assert "Post-Hackathon" in content or "Migration" in content or "Roadmap" in content, "Missing migration roadmap in README"
    assert "uvicorn" in content, "Missing uvicorn run instructions in README"
    print("PASS: README.md exists and covers all required operational and architectural sections")


if __name__ == "__main__":
    test_radar_sources_config()
    test_capture_radar_and_dynamic_discovery()
    test_readme_coverage()
    print("\nALL PHASE 6 TESTS PASSED SUCCESSFULLY!")
