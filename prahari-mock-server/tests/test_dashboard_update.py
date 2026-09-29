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
from app.validator import (
    validate_system_consistency,
    validate_severity_alignment,
    ALLOWED_SEVERITIES,
)

client = TestClient(app)


def test_dashboard_kpis_extension():
    """
    Verifies GET /api/dashboard/kpis schema extension:
    - Status code 200 OK
    - Bare JSON resource (no wrapper envelopes)
    - Contains required fields nextCriticalWindow ("T+36h") and areasAtRisk (7)
    - Full 7-field contract verification
    """
    res = client.get("/api/dashboard/kpis")
    assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}"
    body = res.json()
    assert isinstance(body, dict), "Expected JSON object at top level"
    assert "data" not in body, "Response must not contain 'data' envelope"
    assert "result" not in body, "Response must not contain 'result' envelope"

    # Specific contract checks
    assert "nextCriticalWindow" in body, "Missing 'nextCriticalWindow' in /api/dashboard/kpis"
    assert body["nextCriticalWindow"] == "T+36h", f"Expected 'T+36h', got {body['nextCriticalWindow']}"
    assert isinstance(body["nextCriticalWindow"], str), "'nextCriticalWindow' must be a string"

    assert "areasAtRisk" in body, "Missing 'areasAtRisk' in /api/dashboard/kpis"
    assert body["areasAtRisk"] == 7, f"Expected 7, got {body['areasAtRisk']}"
    assert isinstance(body["areasAtRisk"], int), "'areasAtRisk' must be an integer"

    # Full 7-field validation
    expected_fields = {
        "activeStormCells": 3,
        "highRiskPopulationMillions": 4.82,
        "gridCellsDownscaled": 14200,
        "downscaleLatencyMs": 340,
        "spatialResolutionGain": "2.4x",
        "nextCriticalWindow": "T+36h",
        "areasAtRisk": 7,
    }
    for field, val in expected_fields.items():
        assert field in body, f"Field '{field}' missing from /api/dashboard/kpis"
        assert body[field] == val, f"Field '{field}' expected {val}, got {body[field]}"

    print("PASS: /api/dashboard/kpis verified (nextCriticalWindow='T+36h', areasAtRisk=7, 7 fields total)")


def test_dashboard_active_anomalies_extension():
    """
    Verifies GET /api/dashboard/active-anomalies schema extension:
    - Status code 200 OK
    - Bare JSON resource list
    - 3 active anomalies: BOB-02, AS-01, NE-04
    - Each anomaly contains severity, region, basin, forecastLeadTimeHours, and valid center coordinates
    """
    res = client.get("/api/dashboard/active-anomalies")
    assert res.status_code == 200, f"Expected 200 OK, got {res.status_code}"
    body = res.json()
    assert isinstance(body, list), "Expected list of anomaly objects"
    assert len(body) == 3, f"Expected 3 active anomalies, found {len(body)}"

    expected_ids = {"BOB-02", "AS-01", "NE-04"}
    found_ids = set()

    for idx, item in enumerate(body):
        assert isinstance(item, dict), f"Anomaly item at index {idx} must be a dictionary"
        anomaly_id = item.get("id")
        assert anomaly_id in expected_ids, f"Unexpected anomaly id '{anomaly_id}'"
        found_ids.add(anomaly_id)

        # 1. severity: in ["EXTREME", "HIGH", "MODERATE", "LOW"]
        assert "severity" in item, f"Missing 'severity' in anomaly {anomaly_id}"
        assert item["severity"] in ALLOWED_SEVERITIES, (
            f"Invalid severity '{item['severity']}' in {anomaly_id}. Must be one of {ALLOWED_SEVERITIES}"
        )

        # 2. region: non-empty string
        assert "region" in item, f"Missing 'region' in anomaly {anomaly_id}"
        assert isinstance(item["region"], str) and len(item["region"].strip()) > 0, (
            f"'region' must be a non-empty string in {anomaly_id}"
        )

        # 3. basin: non-empty string
        assert "basin" in item, f"Missing 'basin' in anomaly {anomaly_id}"
        assert isinstance(item["basin"], str) and len(item["basin"].strip()) > 0, (
            f"'basin' must be a non-empty string in {anomaly_id}"
        )

        # 4. forecastLeadTimeHours: integer
        assert "forecastLeadTimeHours" in item, f"Missing 'forecastLeadTimeHours' in anomaly {anomaly_id}"
        assert isinstance(item["forecastLeadTimeHours"], int), (
            f"'forecastLeadTimeHours' must be an integer in {anomaly_id}, got {type(item['forecastLeadTimeHours'])}"
        )
        assert item["forecastLeadTimeHours"] > 0, f"'forecastLeadTimeHours' must be positive in {anomaly_id}"

        # 5. center with valid lat and lon float coordinates
        assert "center" in item, f"Missing 'center' in anomaly {anomaly_id}"
        center = item["center"]
        assert isinstance(center, dict), f"'center' must be an object in {anomaly_id}"
        assert "lat" in center and "lon" in center, f"'center' must contain 'lat' and 'lon' in {anomaly_id}"
        assert isinstance(center["lat"], (float, int)), f"'lat' coordinate must be float/numeric in {anomaly_id}"
        assert isinstance(center["lon"], (float, int)), f"'lon' coordinate must be float/numeric in {anomaly_id}"
        assert -90.0 <= center["lat"] <= 90.0, f"'lat' out of bounds in {anomaly_id}"
        assert -180.0 <= center["lon"] <= 180.0, f"'lon' out of bounds in {anomaly_id}"

        # Additional metadata fields
        assert "category" in item, f"Missing 'category' in {anomaly_id}"
        assert "name" in item, f"Missing 'name' in {anomaly_id}"
        assert "status" in item, f"Missing 'status' in {anomaly_id}"
        assert "maxWindKmph" in item, f"Missing 'maxWindKmph' in {anomaly_id}"
        assert "centralPressureHpa" in item, f"Missing 'centralPressureHpa' in {anomaly_id}"

    assert found_ids == expected_ids, f"Expected IDs {expected_ids}, but got {found_ids}"
    print("PASS: /api/dashboard/active-anomalies verified (3 anomalies, all map filter fields validated)")


def test_frontend_kpi_cards_mapping():
    """
    Validates exact frontend contract mapping for the 4 Dashboard KPI Cards:
    Card 1: ACTIVE ANOMALIES -> activeAnomalies.length (3)
    Card 2: SEVERE EVENTS    -> Count of EXTREME + HIGH (2)
    Card 3: NEXT WINDOW      -> kpis.nextCriticalWindow ("T+36h")
    Card 4: AREAS AT RISK    -> kpis.areasAtRisk (7)
    """
    kpis_res = client.get("/api/dashboard/kpis")
    anomalies_res = client.get("/api/dashboard/active-anomalies")

    assert kpis_res.status_code == 200
    assert anomalies_res.status_code == 200

    kpis = kpis_res.json()
    anomalies = anomalies_res.json()

    # Card 1: Active Anomalies count
    active_anomalies_count = len(anomalies)
    assert active_anomalies_count == 3, f"Card 1 Expected 3, got {active_anomalies_count}"

    # Card 2: Severe Events count (EXTREME + HIGH)
    severe_events_count = len([
        a for a in anomalies if a.get("severity") in ("EXTREME", "HIGH")
    ])
    assert severe_events_count == 2, f"Card 2 Expected 2, got {severe_events_count}"

    # Card 3: Next Window
    next_window = kpis.get("nextCriticalWindow")
    assert next_window == "T+36h", f"Card 3 Expected 'T+36h', got {next_window}"

    # Card 4: Areas at Risk
    areas_at_risk = kpis.get("areasAtRisk")
    assert areas_at_risk == 7, f"Card 4 Expected 7, got {areas_at_risk}"

    print(
        f"PASS: 4 KPI Cards Dynamic Mapping Verified -> "
        f"Active: {active_anomalies_count}, Severe: {severe_events_count}, "
        f"Window: {next_window}, AreasAtRisk: {areas_at_risk}"
    )


def test_frontend_map_filter_controls():
    """
    Validates dynamic map filter controls across active anomalies:
    - Filter: Severity (EXTREME, MODERATE, HIGH)
    - Filter: Anomaly Type (Cyclone, Depression, Heavy Rain)
    - Filter: Region / Basin (Odisha/Bay of Bengal, Gujarat Coast/Arabian Sea, Assam/Brahmaputra Basin)
    - Filter: Lead Time (48, 24, 36 hours)
    """
    res = client.get("/api/dashboard/active-anomalies")
    assert res.status_code == 200
    anomalies = res.json()

    severities = {a["severity"] for a in anomalies}
    categories = {a["category"] for a in anomalies}
    regions = {a["region"] for a in anomalies}
    basins = {a["basin"] for a in anomalies}
    lead_times = {a["forecastLeadTimeHours"] for a in anomalies}

    assert severities == {"EXTREME", "HIGH", "MODERATE"}
    assert categories == {"Cyclone", "Depression", "Heavy Rain"}
    assert regions == {"Odisha", "Gujarat Coast", "Assam"}
    assert basins == {"Bay of Bengal", "Arabian Sea", "Brahmaputra Basin"}
    assert lead_times == {48, 24, 36}

    print("PASS: Dynamic Map Filter Controls Verified across all 4 filter facets")


def test_system_validator_consistency():
    """
    Runs startup consistency validator and ensures 0 issues across all 4 rules.
    """
    healthy = validate_system_consistency()
    assert healthy is True, "System consistency validator failed"
    print("PASS: validate_system_consistency returned True with 0 issues")


if __name__ == "__main__":
    test_dashboard_kpis_extension()
    test_dashboard_active_anomalies_extension()
    test_frontend_kpi_cards_mapping()
    test_frontend_map_filter_controls()
    test_system_validator_consistency()
    print("\nALL DASHBOARD UPDATE REGRESSION TESTS PASSED SUCCESSFULLY!")
