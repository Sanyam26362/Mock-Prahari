# Dashboard KPI Cards & Active Anomaly Filter Schema Extension Report

**Project:** Prahari / Extreme Weather Intelligence (SIH 2026, PS 26078)  
**Target Environment:** Render Cloud Platform (`https://mock-prahari.onrender.com`)  
**Date:** September 29, 2026  
**Status:** Verification Passed & Deployed to GitHub `main`  
**Git Commit Hash:** `002bdcb8773fc4e65ba02c5a8ce4d2c79ef90115` (`002bdcb`)  

---

## 1. Executive Summary

This report documents the schema extension and fixture enhancements for the **Prahari Extreme Weather Intelligence Mock Server** to fulfill the frontend team's dynamic dashboard contract requirements. 

Key milestones achieved:
1. **Dynamic KPI Cards:** Extended `GET /api/dashboard/kpis` with `nextCriticalWindow` and `areasAtRisk`, completing the full 4-card metric row (`Active Anomalies`, `Severe Events`, `Next Critical Window`, `Areas at Risk`).
2. **Dynamic Map Filter Controls:** Enriched `GET /api/dashboard/active-anomalies` across all 3 active tracking anomalies (`BOB-02`, `AS-01`, and `NE-04`) with `severity`, `region`, `basin`, and `forecastLeadTimeHours`.
3. **Data Alignment & Consistency:** Verified cross-fixture consistency against `anomalyOverview.json` and `eventOptions.json`, confirming 0 warnings across all 4 startup validation rules in `app/validator.py`.
4. **Automated Regression Testing:** Authored `tests/test_dashboard_update.py` and executed the entire regression test suite (7 suites total) with 100% pass rate.
5. **Git Deployment:** Staged, committed, and pushed changes to `origin/main` on GitHub to trigger Render's automated cloud redeployment.

---

## 2. JSON Schema Comparison (Before vs. After)

### 2.1 Endpoint 1: `GET /api/dashboard/kpis`

#### Before Schema (5 fields)
```json
{
  "activeStormCells": 3,
  "highRiskPopulationMillions": 4.82,
  "gridCellsDownscaled": 14200,
  "downscaleLatencyMs": 340,
  "spatialResolutionGain": "2.4x"
}
```

#### After Schema (7 fields)
```json
{
  "activeStormCells": 3,
  "highRiskPopulationMillions": 4.82,
  "gridCellsDownscaled": 14200,
  "downscaleLatencyMs": 340,
  "spatialResolutionGain": "2.4x",
  "nextCriticalWindow": "T+36h",
  "areasAtRisk": 7
}
```

#### Field Diff
```diff
   "gridCellsDownscaled": 14200,
   "downscaleLatencyMs": 340,
   "spatialResolutionGain": "2.4x"
+  "nextCriticalWindow": "T+36h",
+  "areasAtRisk": 7
 }
```

---

### 2.2 Endpoint 2: `GET /api/dashboard/active-anomalies`

#### Before Schema (1 item, basic coordinates)
```json
[
  {
    "id": "BOB-02",
    "name": "Cyclone BOB-02",
    "category": "Severe Cyclonic Storm",
    "center": {"lat": 18.4, "lon": 87.2},
    "maxWindKmph": 135,
    "centralPressureHpa": 978,
    "status": "TRACKING"
  }
]
```

#### After Schema (3 items, fully enriched with map filter attributes)
```json
[
  {
    "id": "BOB-02",
    "name": "Severe Cyclonic Storm BOB-02",
    "category": "Cyclone",
    "severity": "EXTREME",
    "center": {
      "lat": 18.4,
      "lon": 87.2
    },
    "region": "Odisha",
    "basin": "Bay of Bengal",
    "forecastLeadTimeHours": 48,
    "maxWindKmph": 135,
    "centralPressureHpa": 978,
    "status": "TRACKING"
  },
  {
    "id": "AS-01",
    "name": "Deep Depression AS-01",
    "category": "Depression",
    "severity": "MODERATE",
    "center": {
      "lat": 15.2,
      "lon": 68.5
    },
    "region": "Gujarat Coast",
    "basin": "Arabian Sea",
    "forecastLeadTimeHours": 24,
    "maxWindKmph": 65,
    "centralPressureHpa": 998,
    "status": "MONITORING"
  },
  {
    "id": "NE-04",
    "name": "Flash Flood & Cloudburst NE-04",
    "category": "Heavy Rain",
    "severity": "HIGH",
    "center": {
      "lat": 26.1,
      "lon": 91.7
    },
    "region": "Assam",
    "basin": "Brahmaputra Basin",
    "forecastLeadTimeHours": 36,
    "maxWindKmph": 55,
    "centralPressureHpa": 1004,
    "status": "ALERT"
  }
]
```

#### Structural Additions per Anomaly Item
| Added Field | Type | Example Value | Target UI Control |
|---|---|---|---|
| `severity` | `string` (`EXTREME \| HIGH \| MODERATE \| LOW`) | `"EXTREME"` | Card 2 (Severe Events count) & Map Severity Filter |
| `region` | `string` | `"Odisha"` | Map Region Quick-filter |
| `basin` | `string` | `"Bay of Bengal"` | Oceanic Basin Filter |
| `forecastLeadTimeHours` | `integer` | `48` | Lead Time Range Slider / Dropdown |

---

## 3. Frontend KPI Cards Dynamic Mapping Verification

The frontend dashboard renders a 4-card KPI summary banner. The table below details the mapping and values verified through automated test suites:

| UI Card | Target API Endpoint | Frontend Mapping / Logic | Live Value | Verification Status |
|---|---|---|:---:|:---:|
| **Card 1: Active Anomalies** | `/api/dashboard/active-anomalies` | `activeAnomalies.length` | `3` | **VERIFIED** |
| **Card 2: Severe Events** | `/api/dashboard/active-anomalies` | Filter: `item.severity in ['EXTREME', 'HIGH']` | `2` (`BOB-02`, `NE-04`) | **VERIFIED** |
| **Card 3: Next Critical Window** | `/api/dashboard/kpis` | `kpis.nextCriticalWindow` | `"T+36h"` | **VERIFIED** |
| **Card 4: Areas at Risk** | `/api/dashboard/kpis` | `kpis.areasAtRisk` | `7` | **VERIFIED** |

---

## 4. Dynamic Map Filter Controls Verification

The interactive map component filters active anomaly pins across 4 distinct facets:

| Map Filter Control | Anomaly Field | Anomaly Values Present in Payload | UI Behavior / Expected Result |
|---|---|---|---|
| **Severity Filter** | `item.severity` | `EXTREME` (BOB-02), `HIGH` (NE-04), `MODERATE` (AS-01) | Renders color-coded severity badges (`Red`, `Orange`, `Amber`) |
| **Anomaly Type** | `item.category` | `Cyclone`, `Depression`, `Heavy Rain` | Filters marker icons by hazard typology |
| **Region / Basin** | `item.region` / `item.basin` | `Odisha` (`Bay of Bengal`), `Gujarat Coast` (`Arabian Sea`), `Assam` (`Brahmaputra Basin`) | Zooms/pans viewport to coastal or riverine basins |
| **Lead Time Horizon** | `item.forecastLeadTimeHours` | `48h`, `24h`, `36h` | Filters active anomalies within selected forecast horizon |

---

## 5. Verification & Testing Results

### 5.1 Automated Regression Test (`tests/test_dashboard_update.py`)
Executed with Python 3.11 TestClient against FastAPI routes:

```
PASS: /api/dashboard/kpis verified (nextCriticalWindow='T+36h', areasAtRisk=7, 7 fields total)
PASS: /api/dashboard/active-anomalies verified (3 anomalies, all map filter fields validated)
PASS: 4 KPI Cards Dynamic Mapping Verified -> Active: 3, Severe: 2, Window: T+36h, AreasAtRisk: 7
PASS: Dynamic Map Filter Controls Verified across all 4 filter facets
PASS: validate_system_consistency returned True with 0 issues

ALL DASHBOARD UPDATE REGRESSION TESTS PASSED SUCCESSFULLY!
```

### 5.2 System Consistency Validator (`app/validator.py`)
Checked all cross-module data relationships across the system:

```
============================================================================
           PRAHARI MOCK SERVER STARTUP CONSISTENCY VALIDATOR
============================================================================
Check / Rule                                       | Status     | Issues
----------------------------------------------------------------------------
Rule 1: Event Monitor Keyed Completeness           | PASSED     | 0
Rule 2: Historical Replay Keyed Completeness       | PASSED     | 0
Rule 3: Severity Field Alignment                   | PASSED     | 0
Rule 4: Radar Station Folder Consistency           | PASSED     | 0
----------------------------------------------------------------------------
RESULT: ALL CONSISTENCY CHECKS PASSED (System Healthy)
============================================================================
```

### 5.3 Full Test Suite Regression Results
All 7 test suites executed and passed with 0 failures:
- `test_phase2.py`: **PASSED**
- `test_phase3.py`: **PASSED**
- `test_phase4.py`: **PASSED**
- `test_phase5.py`: **PASSED**
- `test_phase6.py`: **PASSED**
- `test_hf_prep.py`: **PASSED**
- `test_dashboard_update.py`: **PASSED**

---

## 6. Git Deployment Audit Trail

- **Git Remote:** `origin` (`https://github.com/Sanyam26362/Mock-Prahari.git`)
- **Target Branch:** `main`
- **Commit SHA:** `002bdcb8773fc4e65ba02c5a8ce4d2c79ef90115`
- **Short SHA:** `002bdcb`
- **Commit Subject:** `feat(dashboard): extend kpis with critical window and enrich active anomalies with map filter fields`
- **Files Committed:**
  1. `data/dashboard/kpis.json`
  2. `data/dashboard/activeAnomalies.json`
  3. `tests/test_dashboard_update.py`
- **Push Output:**
  ```
  To https://github.com/Sanyam26362/Mock-Prahari.git
     18f2ff7..002bdcb  main -> main
  ```
- **Redeployment Trigger:** Render Git webhook automatically triggered build and native Python deployment for service `prahari-mock-server`.
