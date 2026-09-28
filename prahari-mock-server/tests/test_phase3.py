import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.loader import BASE_DATA_DIR

client = TestClient(app)


def test_model_analysis_routes():
    endpoints = [
        ("/api/model-analysis/overview", "modelAnalysis/overview.json"),
        ("/api/model-analysis/models", "modelAnalysis/models.json"),
        ("/api/model-analysis/pipeline", "modelAnalysis/pipeline.json"),
        ("/api/model-analysis/configuration", "modelAnalysis/configuration.json"),
        ("/api/model-analysis/metrics", "modelAnalysis/metrics.json"),
        ("/api/model-analysis/verification", "modelAnalysis/verification.json"),
        ("/api/model-analysis/track-error-chart", "modelAnalysis/trackErrorChart.json"),
        ("/api/model-analysis/baseline-comparison", "modelAnalysis/baselineComparison.json"),
    ]

    for endpoint, file_rel in endpoints:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Failed on {endpoint}: {res.status_code}"
        expected = json.loads((BASE_DATA_DIR / file_rel).read_text(encoding="utf-8"))
        assert res.json() == expected, f"Mismatch on {endpoint}"
        print(f"PASS: {endpoint} -> {file_rel} (200 OK)")


def test_route_precedence():
    # 1. /api/historical-events/comparison-modes vs /{eventId}
    res_modes = client.get("/api/historical-events/comparison-modes")
    assert res_modes.status_code == 200
    assert isinstance(res_modes.json(), list)
    assert len(res_modes.json()) > 0
    assert "gnn-vs-numerical" in [m["id"] for m in res_modes.json()]
    print("PASS: Route precedence - /api/historical-events/comparison-modes returned array, not eventId lookup")

    # 2. /api/event-detail/events vs /{eventId}
    res_events = client.get("/api/event-detail/events")
    assert res_events.status_code == 200
    assert isinstance(res_events.json(), list)
    assert len(res_events.json()) > 0
    assert "BOB-02" in [e["id"] for e in res_events.json()]
    print("PASS: Route precedence - /api/event-detail/events returned array, not eventId lookup")

    # 3. /api/events/ vs /{eventId}
    res_opts = client.get("/api/events/")
    assert res_opts.status_code == 200
    assert isinstance(res_opts.json(), list)
    print("PASS: Route precedence - /api/events/ returned array, not eventId lookup")


def test_case_insensitivity():
    # Event monitor case insensitivity
    res_upper = client.get("/api/events/BOB-02")
    res_lower = client.get("/api/events/bob-02")
    res_mixed = client.get("/api/events/BoB-02")
    assert res_upper.status_code == 200
    assert res_lower.status_code == 200
    assert res_mixed.status_code == 200
    assert res_upper.json() == res_lower.json() == res_mixed.json()
    print("PASS: Case insensitivity - /api/events/BOB-02 == /api/events/bob-02 == /api/events/BoB-02")

    # Historical replay case insensitivity
    res_hist_upper = client.get("/api/historical-events/AMPHAN-2020")
    res_hist_lower = client.get("/api/historical-events/amphan-2020")
    assert res_hist_upper.status_code == 200
    assert res_hist_lower.status_code == 200
    assert res_hist_upper.json() == res_hist_lower.json()
    print("PASS: Case insensitivity - /api/historical-events/AMPHAN-2020 == /api/historical-events/amphan-2020")

    # Event detail case insensitivity
    res_det_upper = client.get("/api/event-detail/BOB-02")
    res_det_lower = client.get("/api/event-detail/bob-02")
    assert res_det_upper.status_code == 200
    assert res_det_lower.status_code == 200
    assert res_det_upper.json() == res_det_lower.json()
    print("PASS: Case insensitivity - /api/event-detail/BOB-02 == /api/event-detail/bob-02")


def test_keyed_nested_endpoints():
    # Test all sub-routes for event monitor
    for sub in ["trajectory", "timeline", "telemetry", "diagnostics", "intensity-distribution", "risk-alerts"]:
        res = client.get(f"/api/events/BOB-02/{sub}")
        assert res.status_code == 200, f"Failed on /api/events/BOB-02/{sub}"
        print(f"PASS: /api/events/BOB-02/{sub} (200 OK)")

    # Test all sub-routes for historical replay
    for sub in ["timeline", "track", "hazard-envelope", "map-layers", "metrics"]:
        res = client.get(f"/api/historical-events/amphan-2020/{sub}")
        assert res.status_code == 200, f"Failed on /api/historical-events/amphan-2020/{sub}"
        print(f"PASS: /api/historical-events/amphan-2020/{sub} (200 OK)")

    # Test all sub-routes for event detail
    for sub in ["overview", "map", "metrics", "hazard", "alerts"]:
        res = client.get(f"/api/event-detail/BOB-02/{sub}")
        assert res.status_code == 200, f"Failed on /api/event-detail/BOB-02/{sub}"
        print(f"PASS: /api/event-detail/BOB-02/{sub} (200 OK)")


def test_404_handling():
    # Non-existent event ID
    res1 = client.get("/api/events/NON-EXISTENT-ID")
    assert res1.status_code == 404
    assert "not found" in res1.json()["detail"].lower()
    print("PASS: 404 on /api/events/NON-EXISTENT-ID")

    res2 = client.get("/api/historical-events/unknown-cyclone-9999")
    assert res2.status_code == 404
    assert "not found" in res2.json()["detail"].lower()
    print("PASS: 404 on /api/historical-events/unknown-cyclone-9999")

    res3 = client.get("/api/event-detail/INVALID-EVENT")
    assert res3.status_code == 404
    assert "not found" in res3.json()["detail"].lower()
    print("PASS: 404 on /api/event-detail/INVALID-EVENT")


def test_openapi_schema_tags():
    res = client.get("/openapi.json")
    assert res.status_code == 200
    schema = res.json()
    paths = schema.get("paths", {})

    tags_found = set()
    for path_data in paths.values():
        for op in path_data.values():
            if isinstance(op, dict) and "tags" in op:
                tags_found.update(op["tags"])

    required_tags = {"Dashboard", "Model Analysis", "Event Monitor", "Historical Replay", "Event Detail"}
    assert required_tags.issubset(tags_found), f"Missing tags: {required_tags - tags_found}"
    print("PASS: All router OpenAPI tags present:", tags_found)


if __name__ == "__main__":
    test_model_analysis_routes()
    test_route_precedence()
    test_case_insensitivity()
    test_keyed_nested_endpoints()
    test_404_handling()
    test_openapi_schema_tags()
    print("\nALL PHASE 3 TESTS PASSED SUCCESSFULLY!")
