import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import Dict, List, Tuple
from app.loader import load_json, BASE_DATA_DIR

ALLOWED_SEVERITIES = {"EXTREME", "HIGH", "MODERATE", "LOW"}


def validate_event_monitor_completeness() -> List[str]:
    issues = []
    try:
        options = load_json("eventMonitor/eventOptions.json")
        event_ids = [opt["id"] for opt in options if "id" in opt]
    except Exception as e:
        return [f"Could not load eventMonitor/eventOptions.json: {e}"]

    keyed_files = [
        "eventMonitor/event.json",
        "eventMonitor/trajectory.json",
        "eventMonitor/timeline.json",
        "eventMonitor/telemetry.json",
        "eventMonitor/diagnostics.json",
        "eventMonitor/intensityDistribution.json",
        "eventMonitor/downstreamRiskAlerts.json",
    ]

    for file_rel in keyed_files:
        try:
            data = load_json(file_rel)
            if isinstance(data, dict):
                keys_lower = {str(k).lower() for k in data.keys()}
                for eid in event_ids:
                    if eid.lower() not in keys_lower:
                        issues.append(f"Event ID '{eid}' missing from '{file_rel}'")
            else:
                issues.append(f"Expected dict at top-level of '{file_rel}'")
        except Exception as e:
            issues.append(f"Error reading '{file_rel}': {e}")

    return issues


def validate_historical_completeness() -> List[str]:
    issues = []
    try:
        events = load_json("historicalReplay/events.json")
        event_ids = [ev["id"] for ev in events if "id" in ev]
    except Exception as e:
        return [f"Could not load historicalReplay/events.json: {e}"]

    keyed_files = [
        "historicalReplay/selectedEvent.json",
        "historicalReplay/timeline.json",
        "historicalReplay/track.json",
        "historicalReplay/hazardEnvelope.json",
        "historicalReplay/mapLayers.json",
        "historicalReplay/metrics.json",
    ]

    for file_rel in keyed_files:
        try:
            data = load_json(file_rel)
            if isinstance(data, dict):
                keys_lower = {str(k).lower() for k in data.keys()}
                for eid in event_ids:
                    if eid.lower() not in keys_lower:
                        issues.append(f"Historical ID '{eid}' missing from '{file_rel}'")
            else:
                issues.append(f"Expected dict at top-level of '{file_rel}'")
        except Exception as e:
            issues.append(f"Error reading '{file_rel}': {e}")

    return issues


def validate_severity_alignment() -> List[str]:
    issues = []

    # Check eventOptions.json
    try:
        options = load_json("eventMonitor/eventOptions.json")
        for opt in options:
            sev = opt.get("severity")
            if sev and sev.upper() not in ALLOWED_SEVERITIES:
                issues.append(f"Invalid severity '{sev}' in eventOptions.json for {opt.get('id')}")
            elif sev and sev != sev.upper():
                issues.append(f"Severity '{sev}' must be uppercase in eventOptions.json")
    except Exception as e:
        issues.append(f"Could not check eventOptions.json: {e}")

    # Check anomalyOverview.json
    try:
        overview = load_json("dashboard/anomalyOverview.json")
        for anomaly in overview.get("anomalies", []):
            sev = anomaly.get("severity")
            if sev and sev.upper() not in ALLOWED_SEVERITIES:
                issues.append(f"Invalid severity '{sev}' in anomalyOverview.json for {anomaly.get('id')}")
            elif sev and sev != sev.upper():
                issues.append(f"Severity '{sev}' must be uppercase in anomalyOverview.json")
    except Exception as e:
        issues.append(f"Could not check anomalyOverview.json: {e}")

    return issues


def validate_radar_station_consistency() -> List[str]:
    issues = []
    try:
        stations = load_json("radar/stations.json")
        for s in stations:
            sid = s["id"].lower()
            products = s.get("products", [])
            for p in products:
                p_folder = BASE_DATA_DIR / "radar" / sid / p.lower()
                if not p_folder.is_dir():
                    issues.append(f"Missing product folder '{sid}/{p}' for station '{s['id']}'")
    except Exception as e:
        issues.append(f"Could not check radar/stations.json: {e}")

    return issues


def validate_system_consistency() -> bool:
    """
    Runs all 4 consistency rules and prints a summary table to the console.
    Returns True if all checks pass or only warnings exist, False if fatal.
    """
    checks = [
        ("Rule 1: Event Monitor Keyed Completeness", validate_event_monitor_completeness()),
        ("Rule 2: Historical Replay Keyed Completeness", validate_historical_completeness()),
        ("Rule 3: Severity Field Alignment", validate_severity_alignment()),
        ("Rule 4: Radar Station Folder Consistency", validate_radar_station_consistency()),
    ]

    print("\n" + "=" * 76)
    print("           PRAHARI MOCK SERVER STARTUP CONSISTENCY VALIDATOR")
    print("=" * 76)
    print(f"{'Check / Rule':<50} | {'Status':<10} | {'Issues'}")
    print("-" * 76)

    all_passed = True
    total_issues = 0

    for name, issues in checks:
        if not issues:
            status = "PASSED"
            issues_str = "0"
        else:
            status = "FAILED"
            issues_str = str(len(issues))
            all_passed = False
            total_issues += len(issues)
        print(f"{name:<50} | {status:<10} | {issues_str}")
        for issue in issues:
            print(f"  --> [ISSUE] {issue}")

    print("-" * 76)
    if all_passed:
        print("RESULT: ALL CONSISTENCY CHECKS PASSED (System Healthy)")
    else:
        print(f"RESULT: {total_issues} ISSUE(S) DETECTED (Review Warnings Above)")
    print("=" * 76 + "\n")

    return all_passed


if __name__ == "__main__":
    success = validate_system_consistency()
    sys.exit(0 if success else 1)
