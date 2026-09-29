# Frontend Integration Guide: Dashboard KPIs & Active Anomaly Map Filters

> **Target Platform:** Smart India Hackathon (SIH 2026) | Problem Statement: PS 26078  
> **Project:** Prahari — Extreme Weather Intelligence Platform  
> **Live Production Server:** [`https://mock-prahari.onrender.com`](https://mock-prahari.onrender.com)  
> **Interactive Swagger UI:** [`https://mock-prahari.onrender.com/docs`](https://mock-prahari.onrender.com/docs)  
> **OpenAPI JSON Specification:** [`https://mock-prahari.onrender.com/openapi.json`](https://mock-prahari.onrender.com/openapi.json)  
> **Verification Status:** All endpoints tested live with `200 OK` (Universal CORS `*` enabled)  

---

## 1. Quick Start for Frontend Developers

### 1.1 Environment Variables
Add to your `.env` or `.env.local` (React / Vite / Next.js):
```env
# Production API (Render)
VITE_API_BASE_URL=https://mock-prahari.onrender.com/api

# Local Development API (if running backend locally)
# VITE_API_BASE_URL=http://localhost:8000/api
```

### 1.2 Universal CORS
Universal CORS is enabled (`allow_origins=["*"]`). You will not encounter CORS blocks whether developing on `http://localhost:5173`, `http://localhost:3000`, or deployed on Vercel/Netlify.

### 1.3 Latency Emulation
The server runs an artificial latency middleware (150ms–450ms) to emulate satellite ingestion and GNN model inference. Skeleton loaders or spinners will display accurately in development.

---

## 2. Tested API Endpoints & Live Responses

### 2.1 Endpoint 1: `GET /api/dashboard/kpis`
Provides the statistical telemetry powering the 4 dashboard KPI cards.

- **Live URL:** `https://mock-prahari.onrender.com/api/dashboard/kpis`
- **Method:** `GET`
- **Status:** `200 OK` (Bare JSON resource, no wrapper envelope)
- **Live Tested Response Payload:**
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

---

### 2.2 Endpoint 2: `GET /api/dashboard/active-anomalies`
Returns all actively monitored storm cells and weather anomalies across Indian basins, fully equipped with map filter attributes.

- **Live URL:** `https://mock-prahari.onrender.com/api/dashboard/active-anomalies`
- **Method:** `GET`
- **Status:** `200 OK`
- **Live Tested Response Payload:**
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

---

### 2.3 Additional Dashboard Endpoints (Verified Live)

| Endpoint | Method | Live Status | Summary Description |
|---|:---:|:---:|---|
| `/api/dashboard/overview` | `GET` | `200 OK` | Basin threat level (`HIGH`), primary threat, update time |
| `/api/dashboard/anomaly-overview` | `GET` | `200 OK` | EFI threshold (0.85) & anomaly category summary |
| `/api/dashboard/forecast-timeline` | `GET` | `200 OK` | 7-day lead-time intensity progression & tracks |
| `/api/dashboard/processing-pipeline` | `GET` | `200 OK` | GNN tensor downscaling pipeline execution stages |
| `/api/system-status` | `GET` | `200 OK` | Platform operational health & active model registry |
| `/api/health` | `GET` | `200 OK` | Liveness probe (`{"status": "ok"}`) |

---

## 3. UI Component Binding Guide

### 3.1 The 4 Dashboard KPI Cards
Here is the exact derivation logic for the 4 dashboard metric cards:

| Card | Label | API Source | Extraction / Calculation Logic | Displayed Value |
|:---:|---|---|---|:---:|
| **1** | **Active Anomalies** | `/api/dashboard/active-anomalies` | `activeAnomalies.length` | `3` |
| **2** | **Severe Events** | `/api/dashboard/active-anomalies` | `activeAnomalies.filter(a => ['EXTREME', 'HIGH'].includes(a.severity)).length` | `2` |
| **3** | **Next Window** | `/api/dashboard/kpis` | `kpis.nextCriticalWindow` | `"T+36h"` |
| **4** | **Areas at Risk** | `/api/dashboard/kpis` | `kpis.areasAtRisk` | `7` |

#### JavaScript / TypeScript Calculation Snippet
```typescript
// Assuming 'kpis' and 'activeAnomalies' are fetched
const activeAnomaliesCount = activeAnomalies?.length ?? 0;
const severeEventsCount = activeAnomalies?.filter(
  item => item.severity === 'EXTREME' || item.severity === 'HIGH'
).length ?? 0;
const nextCriticalWindow = kpis?.nextCriticalWindow ?? 'T+0h';
const areasAtRiskCount = kpis?.areasAtRisk ?? 0;
```

---

### 3.2 Dynamic Map Filter Controls

The interactive map requires 4 filter facets that can now be controlled dynamically:

| Filter Facet | Data Field | Available Values in API | Suggested UI Control | Recommended Theme Colors |
|---|---|---|---|---|
| **Severity** | `item.severity` | `EXTREME`, `HIGH`, `MODERATE`, `LOW` | Multi-select buttons or badge pills | **EXTREME:** `#EF4444` (Red-500)<br>**HIGH:** `#F97316` (Orange-500)<br>**MODERATE:** `#FBBF24` (Amber-400)<br>**LOW:** `#10B981` (Emerald-500) |
| **Hazard Typology** | `item.category` | `Cyclone`, `Depression`, `Heavy Rain` | Dropdown or tab filter | **Cyclone:** Hurricane icon<br>**Depression:** Cloud/wind icon<br>**Heavy Rain:** Cloud-rain icon |
| **Basin & Region** | `item.basin` / `item.region` | `Bay of Bengal` / `Odisha`<br>`Arabian Sea` / `Gujarat Coast`<br>`Brahmaputra Basin` / `Assam` | Select dropdown or map quick-zoom buttons | Panning map to `item.center.lat` / `item.center.lon` |
| **Lead Time Horizon** | `item.forecastLeadTimeHours` | `24`, `36`, `48` | Slider (e.g. 0h – 72h) or quick radio buttons (`24h`, `36h`, `48h`, `All`) | Filter: `item.forecastLeadTimeHours <= selectedHours` |

---

## 4. Copy-Paste TypeScript Interfaces

Create `src/types/dashboard.ts`:

```typescript
export type SeverityLevel = 'EXTREME' | 'HIGH' | 'MODERATE' | 'LOW';

export interface AnomalyCenter {
  lat: number;
  lon: number;
}

export interface ActiveAnomaly {
  id: string;
  name: string;
  category: 'Cyclone' | 'Depression' | 'Heavy Rain' | string;
  severity: SeverityLevel;
  center: AnomalyCenter;
  region: string;
  basin: string;
  forecastLeadTimeHours: number;
  maxWindKmph: number;
  centralPressureHpa: number;
  status: 'TRACKING' | 'MONITORING' | 'ALERT' | string;
}

export interface DashboardKPIs {
  activeStormCells: number;
  highRiskPopulationMillions: number;
  gridCellsDownscaled: number;
  downscaleLatencyMs: number;
  spatialResolutionGain: string;
  nextCriticalWindow: string; // e.g. "T+36h"
  areasAtRisk: number;        // e.g. 7
}

export interface AnomalyOverviewItem {
  id: string;
  type: string;
  severity: SeverityLevel;
  location: string;
}

export interface AnomalyOverview {
  totalAnomalies: number;
  extremeForecastIndexThreshold: number;
  anomalies: AnomalyOverviewItem[];
}

export interface MapFilters {
  severities: SeverityLevel[];
  category: string; // "ALL" or specific category
  basin: string;    // "ALL" or specific basin
  maxLeadTimeHours: number;
}
```

---

## 5. Copy-Paste React Integration Hook (`useDashboard.ts`)

Create `src/hooks/useDashboard.ts`:

```typescript
import { useState, useEffect, useCallback, useMemo } from 'react';
import type { DashboardKPIs, ActiveAnomaly, MapFilters } from '../types/dashboard';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://mock-prahari.onrender.com/api';

export function useDashboard() {
  const [kpis, setKpis] = useState<DashboardKPIs | null>(null);
  const [anomalies, setAnomalies] = useState<ActiveAnomaly[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Map Filter State
  const [filters, setFilters] = useState<MapFilters>({
    severities: ['EXTREME', 'HIGH', 'MODERATE', 'LOW'],
    category: 'ALL',
    basin: 'ALL',
    maxLeadTimeHours: 72,
  });

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [kpisRes, anomaliesRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard/kpis`),
        fetch(`${API_BASE}/dashboard/active-anomalies`),
      ]);

      if (!kpisRes.ok) throw new Error(`KPIs HTTP ${kpisRes.status}`);
      if (!anomaliesRes.ok) throw new Error(`Anomalies HTTP ${anomaliesRes.status}`);

      const [kpisData, anomaliesData] = await Promise.all([
        kpisRes.json(),
        anomaliesRes.json(),
      ]);

      setKpis(kpisData);
      setAnomalies(anomaliesData);
    } catch (err: any) {
      setError(err?.message || 'Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Derived 4 KPI Cards
  const kpiCards = useMemo(() => {
    const activeCount = anomalies.length;
    const severeCount = anomalies.filter(a => a.severity === 'EXTREME' || a.severity === 'HIGH').length;
    const nextWindow = kpis?.nextCriticalWindow ?? 'N/A';
    const areasAtRisk = kpis?.areasAtRisk ?? 0;

    return {
      activeAnomalies: activeCount,
      severeEvents: severeCount,
      nextCriticalWindow: nextWindow,
      areasAtRisk: areasAtRisk,
      highRiskPopulationMillions: kpis?.highRiskPopulationMillions ?? 0,
      gridCellsDownscaled: kpis?.gridCellsDownscaled ?? 0,
    };
  }, [kpis, anomalies]);

  // Client-side filtered anomalies for Map view
  const filteredAnomalies = useMemo(() => {
    return anomalies.filter(item => {
      // 1. Severity filter
      if (!filters.severities.includes(item.severity)) return false;

      // 2. Category filter
      if (filters.category !== 'ALL' && item.category !== filters.category) return false;

      // 3. Basin filter
      if (filters.basin !== 'ALL' && item.basin !== filters.basin) return false;

      // 4. Lead time horizon filter
      if (item.forecastLeadTimeHours > filters.maxLeadTimeHours) return false;

      return true;
    });
  }, [anomalies, filters]);

  return {
    kpis,
    anomalies,
    filteredAnomalies,
    kpiCards,
    filters,
    setFilters,
    loading,
    error,
    refresh: fetchData,
  };
}
```

---

## 6. Live cURL Commands (for Testing from Terminal)

You or your teammate can paste these commands directly into any PowerShell or Bash terminal:

```bash
# Test KPIs
curl -s https://mock-prahari.onrender.com/api/dashboard/kpis

# Test Active Anomalies
curl -s https://mock-prahari.onrender.com/api/dashboard/active-anomalies

# Test Anomaly Overview
curl -s https://mock-prahari.onrender.com/api/dashboard/anomaly-overview

# Test System Status
curl -s https://mock-prahari.onrender.com/api/system-status
```
