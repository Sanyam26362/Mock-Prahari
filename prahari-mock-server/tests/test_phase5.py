import os
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from app.main import app
from app.validator import (
    validate_event_monitor_completeness,
    validate_historical_completeness,
    validate_severity_alignment,
    validate_radar_station_consistency,
    validate_system_consistency,
)

client = TestClient(app)


def test_validator_rules_passing():
    """Verify all 4 consistency rules pass on current mock fixtures."""
    ev_issues = validate_event_monitor_completeness()
    assert ev_issues == [], f"Event monitor issues: {ev_issues}"

    hist_issues = validate_historical_completeness()
    assert hist_issues == [], f"Historical replay issues: {hist_issues}"

    sev_issues = validate_severity_alignment()
    assert sev_issues == [], f"Severity alignment issues: {sev_issues}"

    radar_issues = validate_radar_station_consistency()
    assert radar_issues == [], f"Radar station consistency issues: {radar_issues}"

    assert validate_system_consistency() is True
    print("PASS: All 4 validator rules passed with 0 issues")


def test_latency_middleware_behavior():
    """Verify artificial latency applies to /api/* but NOT to /api/health or /static/*."""
    # Ensure latency is enabled with default 150-450ms
    os.environ["MOCK_LATENCY"] = "true"
    os.environ["MOCK_LATENCY_MIN_MS"] = "150"
    os.environ["MOCK_LATENCY_MAX_MS"] = "300"

    # 1. Health check should NOT have artificial latency (< 60ms)
    t0 = time.perf_counter()
    res_health = client.get("/api/health")
    health_elapsed_ms = (time.perf_counter() - t0) * 1000
    assert res_health.status_code == 200
    assert health_elapsed_ms < 100, f"Health check took too long: {health_elapsed_ms:.1f}ms"
    print(f"PASS: /api/health skipped latency ({health_elapsed_ms:.1f}ms)")

    # 2. API endpoint should have artificial latency (>= 140ms)
    t0 = time.perf_counter()
    res_api = client.get("/api/system-status")
    api_elapsed_ms = (time.perf_counter() - t0) * 1000
    assert res_api.status_code == 200
    assert api_elapsed_ms >= 140, f"Expected latency >= 140ms, got {api_elapsed_ms:.1f}ms"
    print(f"PASS: /api/system-status incurred expected latency ({api_elapsed_ms:.1f}ms)")

    # 3. Static files should NOT have artificial latency (< 100ms)
    t0 = time.perf_counter()
    res_static = client.get("/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1300Z.png")
    static_elapsed_ms = (time.perf_counter() - t0) * 1000
    assert res_static.status_code == 200
    assert static_elapsed_ms < 100, f"Static file took too long: {static_elapsed_ms:.1f}ms"
    print(f"PASS: /static/radar/... skipped latency ({static_elapsed_ms:.1f}ms)")


def test_latency_toggle_disabled():
    """Verify that setting MOCK_LATENCY=false disables artificial delay."""
    os.environ["MOCK_LATENCY"] = "false"
    t0 = time.perf_counter()
    res = client.get("/api/dashboard/kpis")
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert res.status_code == 200
    assert elapsed_ms < 100, f"Expected < 100ms with latency disabled, got {elapsed_ms:.1f}ms"
    print(f"PASS: MOCK_LATENCY=false disabled delay ({elapsed_ms:.1f}ms)")

    # Reset env for subsequent runs
    os.environ["MOCK_LATENCY"] = "true"


if __name__ == "__main__":
    test_validator_rules_passing()
    test_latency_middleware_behavior()
    test_latency_toggle_disabled()
    print("\nALL PHASE 5 TESTS PASSED SUCCESSFULLY!")
