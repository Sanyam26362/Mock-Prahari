import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.loader import load_json, BASE_DATA_DIR
from fastapi import HTTPException

client = TestClient(app)


def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
    print("PASS: /api/health")


def test_system_status():
    res = client.get("/api/system-status")
    assert res.status_code == 200
    expected = json.loads((BASE_DATA_DIR / "shared/systemStatus.json").read_text(encoding="utf-8"))
    assert res.json() == expected
    assert "data" not in res.json()
    assert "result" not in res.json()
    print("PASS: /api/system-status")


def test_dashboard_endpoints():
    endpoints = [
        ("/api/dashboard/overview", "dashboard/overview.json"),
        ("/api/dashboard/kpis", "dashboard/kpis.json"),
        ("/api/dashboard/anomaly-overview", "dashboard/anomalyOverview.json"),
        ("/api/dashboard/active-anomalies", "dashboard/activeAnomalies.json"),
        ("/api/dashboard/forecast-timeline", "dashboard/forecastTimeline.json"),
        ("/api/dashboard/processing-pipeline", "dashboard/processingPipeline.json"),
    ]

    for endpoint, file_rel in endpoints:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Failed on {endpoint}: {res.status_code}"
        expected = json.loads((BASE_DATA_DIR / file_rel).read_text(encoding="utf-8"))
        body = res.json()
        assert body == expected, f"Mismatch on {endpoint}"
        if isinstance(body, dict):
            assert "data" not in body, f"Envelope detected in {endpoint}"
            assert "result" not in body, f"Envelope detected in {endpoint}"
        print(f"PASS: {endpoint} -> {file_rel} (Raw JSON, 200 OK)")


def test_missing_file_handling():
    try:
        load_json("dashboard/missingFile.json")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Resource file not found: dashboard/missingFile.json"
        print("PASS: load_json 404 on missing file")


def test_path_traversal_guard():
    try:
        load_json("../requirements.txt")
        assert False, "Should have raised HTTPException"
    except HTTPException as e:
        assert e.status_code == 400
        assert "Directory traversal" in e.detail
        print("PASS: load_json 400 on directory traversal")


def test_unknown_endpoint():
    res = client.get("/api/dashboard/unknown-endpoint")
    assert res.status_code == 404
    print("PASS: /api/dashboard/unknown-endpoint -> 404")


def test_cors():
    res = client.get("/api/dashboard/kpis", headers={"Origin": "http://localhost:5173"})
    assert res.status_code == 200
    assert res.headers.get("access-control-allow-origin") == "http://localhost:5173"
    print("PASS: CORS header access-control-allow-origin present")


def test_openapi_tags():
    res = client.get("/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    paths = schema.get("paths", {})
    for p in ["/api/dashboard/overview", "/api/dashboard/kpis", "/api/dashboard/anomaly-overview",
              "/api/dashboard/active-anomalies", "/api/dashboard/forecast-timeline", "/api/dashboard/processing-pipeline"]:
        assert p in paths, f"{p} missing from openapi schema"
        assert "Dashboard" in paths[p]["get"]["tags"], f"Tag 'Dashboard' missing from {p}"
    print("PASS: OpenAPI schema tags verified for Dashboard")


if __name__ == "__main__":
    test_health()
    test_system_status()
    test_dashboard_endpoints()
    test_missing_file_handling()
    test_path_traversal_guard()
    test_unknown_endpoint()
    test_cors()
    test_openapi_tags()
    print("\nALL PHASE 2 TESTS PASSED SUCCESSFULLY!")
