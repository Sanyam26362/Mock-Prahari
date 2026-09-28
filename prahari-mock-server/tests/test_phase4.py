import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_radar_stations():
    res = client.get("/api/radar/stations")
    assert res.status_code == 200
    stations = res.json()
    assert isinstance(stations, list)
    assert len(stations) >= 3

    ids = [s["id"] for s in stations]
    assert "kolkata" in ids
    assert "paradip" in ids
    assert "agartala" in ids

    kolkata = next(s for s in stations if s["id"] == "kolkata")
    assert "latitude" in kolkata
    assert "longitude" in kolkata
    assert "rangeKm" in kolkata
    assert "reflectivity" in kolkata["products"]
    print("PASS: /api/radar/stations lists valid stations")


def test_radar_frames_sorting_and_urls():
    res = client.get("/api/radar/kolkata/frames?product=reflectivity")
    assert res.status_code == 200
    data = res.json()
    assert data["stationId"] == "kolkata"
    assert data["product"] == "reflectivity"
    assert data["source"] == "IMD Doppler Weather Radar"

    frames = data["frames"]
    assert len(frames) >= 3

    # Check sorting: oldest to newest
    timestamps = [f["timestamp"] for f in frames]
    assert timestamps == sorted(timestamps)
    assert timestamps[0] == "2026-09-28T12:00:00Z"
    assert timestamps[1] == "2026-09-28T12:30:00Z"
    assert timestamps[2] == "2026-09-28T13:00:00Z"

    # Check URL format
    for f in frames:
        assert f["imageUrl"].startswith("/static/radar/kolkata/reflectivity/")
        assert f["imageUrl"].endswith(".png")
        assert "\\" not in f["imageUrl"]  # ensure forward slashes
    print("PASS: /api/radar/kolkata/frames sorted chronologically with forward-slash URLs")


def test_time_filtering_and_limit():
    # Filter 'from'
    res_from = client.get("/api/radar/kolkata/frames?product=reflectivity&from=2026-09-28T12:30:00Z")
    assert res_from.status_code == 200
    frames_from = res_from.json()["frames"]
    assert len(frames_from) >= 2
    for f in frames_from:
        assert f["timestamp"] >= "2026-09-28T12:30:00Z"
    print("PASS: from filter works correctly")

    # Filter 'to'
    res_to = client.get("/api/radar/kolkata/frames?product=reflectivity&to=2026-09-28T12:30:00Z")
    assert res_to.status_code == 200
    frames_to = res_to.json()["frames"]
    assert len(frames_to) == 2
    assert frames_to[0]["timestamp"] == "2026-09-28T12:00:00Z"
    assert frames_to[1]["timestamp"] == "2026-09-28T12:30:00Z"
    print("PASS: to filter works correctly")

    # Limit
    res_all = client.get("/api/radar/kolkata/frames?product=reflectivity")
    all_timestamps = [f["timestamp"] for f in res_all.json()["frames"]]

    res_limit = client.get("/api/radar/kolkata/frames?product=reflectivity&limit=1")
    assert res_limit.status_code == 200
    frames_limit = res_limit.json()["frames"]
    assert len(frames_limit) == 1
    assert frames_limit[0]["timestamp"] == all_timestamps[-1]
    print("PASS: limit parameter returns newest slice")


def test_radar_latest_frame():
    res_all = client.get("/api/radar/kolkata/frames?product=reflectivity")
    all_timestamps = [f["timestamp"] for f in res_all.json()["frames"]]

    res = client.get("/api/radar/kolkata/latest?product=reflectivity")
    assert res.status_code == 200
    latest = res.json()
    assert latest["timestamp"] == all_timestamps[-1]
    assert latest["imageUrl"].startswith("/static/radar/kolkata/reflectivity/")
    print(f"PASS: /api/radar/kolkata/latest returns newest frame ({latest['timestamp']})")


def test_static_png_serving():
    res = client.get("/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png")
    assert res.status_code == 200
    assert "image/png" in res.headers.get("content-type", "")
    assert len(res.content) > 0
    print("PASS: Static PNG file served with image/png MIME type")


def test_unknown_station_404():
    res = client.get("/api/radar/mumbai/frames")
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()
    print("PASS: Unknown station cleanly returns 404")


def test_unknown_product_404():
    # Agartala only supports reflectivity, not velocity
    res = client.get("/api/radar/agartala/frames?product=velocity")
    assert res.status_code == 404
    assert "not supported" in res.json()["detail"].lower()
    print("PASS: Unsupported product cleanly returns 404")


def test_station_with_no_images():
    res = client.get("/api/radar/agartala/frames?product=reflectivity")
    assert res.status_code == 200
    assert res.json()["frames"] == []
    print("PASS: Station with no images returns 200 with empty frames array")

    res_latest = client.get("/api/radar/agartala/latest?product=reflectivity")
    assert res_latest.status_code == 404
    print("PASS: /latest on station with no images returns 404")


if __name__ == "__main__":
    test_radar_stations()
    test_radar_frames_sorting_and_urls()
    test_time_filtering_and_limit()
    test_radar_latest_frame()
    test_static_png_serving()
    test_unknown_station_404()
    test_unknown_product_404()
    test_station_with_no_images()
    print("\nALL PHASE 4 TESTS PASSED SUCCESSFULLY!")
