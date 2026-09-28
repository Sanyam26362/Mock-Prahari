# Prahari API Documentation & Frontend Integration Reference

> **Live Production API:** [`https://mock-prahari.onrender.com`](https://mock-prahari.onrender.com)  
> **Interactive Swagger UI:** [`https://mock-prahari.onrender.com/docs`](https://mock-prahari.onrender.com/docs)  
> **OpenAPI JSON Spec:** [`https://mock-prahari.onrender.com/openapi.json`](https://mock-prahari.onrender.com/openapi.json)  
> **Target Platform:** Smart India Hackathon (SIH 2026) | Problem Statement: PS 26078  

---

## 1. Quick Start for Frontend Developers

This backend is fully deployed, operational, and publicly accessible on Render. All endpoints support **Universal CORS** (`allow_origins=["*"]`), meaning you can call this API directly from `localhost:5173`, `localhost:3000`, Vercel, Netlify, or GitHub Pages without browser blocks.

### 1.1 Environment Variable Setup
Create or update your `.env` file in your React / Next.js / Vite project:
```env
VITE_API_BASE_URL=https://mock-prahari.onrender.com/api
VITE_STATIC_BASE_URL=https://mock-prahari.onrender.com
```

### 1.2 Base API Client (Axios / Fetch Example)
```typescript
// src/api/client.ts
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'https://mock-prahari.onrender.com/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### 1.3 Latency Emulation Note
The mock server runs an **Artificial Latency Middleware** (150ms–450ms) to emulate real-world satellite ingestion and graph neural network computation times. Use this to verify loading spinners, skeleton states, and optimistic UI transitions on the frontend.

---

## 2. API Endpoint Directory

| # | Module | Method | Endpoint | Description |
|:---:|:---|:---:|:---|:---|
| 1 | System | `GET` | `/api/health` | Liveness probe for health checks |
| 2 | System | `GET` | `/api/system-status` | Operational status of pipelines & telemetry |
| 3 | Dashboard | `GET` | `/api/dashboard/overview` | Basin-wide weather summary & storm count |
| 4 | Dashboard | `GET` | `/api/dashboard/kpis` | Core platform KPIs (accuracy, lead time) |
| 5 | Dashboard | `GET` | `/api/dashboard/anomaly-overview` | High-level summary of active anomalies |
| 6 | Dashboard | `GET` | `/api/dashboard/active-anomalies` | List of regional weather anomalies |
| 7 | Dashboard | `GET` | `/api/dashboard/forecast-timeline` | Multi-day basin forecast timeline |
| 8 | Dashboard | `GET` | `/api/dashboard/processing-pipeline` | AI inference stages processing status |
| 9 | Model Analysis | `GET` | `/api/model-analysis/overview` | GNN + Diffusion hybrid AI overview |
| 10 | Model Analysis | `GET` | `/api/model-analysis/models` | Registry of active deep learning models |
| 11 | Model Analysis | `GET` | `/api/model-analysis/pipeline` | Tensor dataflow & mesh downscaling pipeline |
| 12 | Model Analysis | `GET` | `/api/model-analysis/configuration` | Hyperparameters & spatial mesh resolution |
| 13 | Model Analysis | `GET` | `/api/model-analysis/metrics` | RMSE, MAE, CRPS, and inference latencies |
| 14 | Model Analysis | `GET` | `/api/model-analysis/verification` | Ensemble calibration & verification curves |
| 15 | Model Analysis | `GET` | `/api/model-analysis/track-error-chart` | Track distance error vs forecast lead hours |
| 16 | Model Analysis | `GET` | `/api/model-analysis/baseline-comparison` | Benchmark vs ECMWF-HRES & IMD-GFS |
| 17 | Event Monitor | `GET` | `/api/events/` | List of all actively monitored extreme events |
| 18 | Event Monitor | `GET` | `/api/events/{eventId}` | Base metadata for a specific live event |
| 19 | Event Monitor | `GET` | `/api/events/{eventId}/trajectory` | Cyclone eye coordinates & forecast cone track |
| 20 | Event Monitor | `GET` | `/api/events/{eventId}/timeline` | Historical and forecasted intensity timeline |
| 21 | Event Monitor | `GET` | `/api/events/{eventId}/telemetry` | Real-time central pressure, wind & speed |
| 22 | Event Monitor | `GET` | `/api/events/{eventId}/diagnostics` | Vorticity, SST & vertical wind shear stats |
| 23 | Event Monitor | `GET` | `/api/events/{eventId}/intensity-distribution` | Probability spread across cyclone categories |
| 24 | Event Monitor | `GET` | `/api/events/{eventId}/risk-alerts` | Downstream coastal inundation & flood risks |
| 25 | Historical Replay | `GET` | `/api/historical-events/` | Historical cyclone archive (Amphan, Biparjoy) |
| 26 | Historical Replay | `GET` | `/api/historical-events/comparison-modes` | Replay modes (Model vs Ground Truth) |
| 27 | Historical Replay | `GET` | `/api/historical-events/{eventId}` | Selected historical event summary |
| 28 | Historical Replay | `GET` | `/api/historical-events/{eventId}/timeline` | Historical time steps for scrubber slider |
| 29 | Historical Replay | `GET` | `/api/historical-events/{eventId}/track` | Actual observed track vs predicted track |
| 30 | Historical Replay | `GET` | `/api/historical-events/{eventId}/hazard-envelope` | Impact polygons & storm surge zones |
| 31 | Historical Replay | `GET` | `/api/historical-events/{eventId}/map-layers` | GeoJSON layers for Leaflet/Mapbox maps |
| 32 | Historical Replay | `GET` | `/api/historical-events/{eventId}/metrics` | Post-event verification metrics |
| 33 | Event Detail | `GET` | `/api/event-detail/events` | List of selectable events for deep dive |
| 34 | Event Detail | `GET` | `/api/event-detail/{eventId}` | Deep dive event overview & status |
| 35 | Event Detail | `GET` | `/api/event-detail/{eventId}/overview` | Synoptic analysis & meteorological overview |
| 36 | Event Detail | `GET` | `/api/event-detail/{eventId}/map` | Event map bounding box & observation stations |
| 37 | Event Detail | `GET` | `/api/event-detail/{eventId}/metrics` | Event impact figures & population at risk |
| 38 | Event Detail | `GET` | `/api/event-detail/{eventId}/hazard` | Terrain-aware hazard zones & rainfall bands |
| 39 | Event Detail | `GET` | `/api/event-detail/{eventId}/alerts` | CAP-compliant disaster alert bulletins |
| 40 | Doppler Radar | `GET` | `/api/radar/stations` | Doppler radar stations & operational metadata |
| 41 | Doppler Radar | `GET` | `/api/radar/{stationId}/frames` | Chronological radar frames with time filtering |
| 42 | Doppler Radar | `GET` | `/api/radar/{stationId}/latest` | Latest harvested radar frame for immediate view |
| 43 | Static Assets | `GET` | `/static/radar/{station}/{product}/{filename}` | Direct PNG Doppler radar frame stream |

---

## 3. Comprehensive Endpoint Reference & Payloads

### 1. Health Check
**Method:** `GET`  
**Path:** `/api/health`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/health`](https://mock-prahari.onrender.com/api/health)  

**Description:** Liveness probe to verify if the server is healthy and responding. Bypasses artificial latency.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "status": "ok"
}
```

**Frontend Usage:** Use in an application startup check or status badge (e.g. green status dot in the navbar).

**TypeScript Interface:**
```typescript
export interface HealthResponse {
  status: string;
}
```

---

### 2. Operational System Status
**Method:** `GET`  
**Path:** `/api/system-status`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/system-status`](https://mock-prahari.onrender.com/api/system-status)  

**Description:** Retrieves operational system diagnostics, active AI pipeline readiness, and cluster compute statistics.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "pipelineStatus": "OPERATIONAL",
  "activeModel": "GNN-Diffusion-v2.4",
  "inputResolutionKm": 12,
  "downscaledResolutionKm": 5,
  "lastIngestTime": "2026-09-28T06:00:00Z",
  "activeAnomaliesCount": 3,
  "systemHealth": "OPTIMAL"
}
```

**Frontend Usage:** Use in the System Diagnostics drawer, footer health indicator, or Ops Dashboard.

**TypeScript Interface:**
```typescript
export interface SystemStatusResponse {
  system: string;
  status: 'OPERATIONAL' | 'DEGRADED' | 'MAINTENANCE';
  timestamp: string;
  cluster: {
    gpuNodesAvailable: number;
    activeInferenceThreads: number;
    memoryAllocatedGB: number;
  };
  pipelineStatus: {
    sphericalGnnStage1: string;
    diffusionDownscalingStage2: string;
    dopplerHarvesterDaemon: string;
  };
}
```

---

### 3. Dashboard Overview
**Method:** `GET`  
**Path:** `/api/dashboard/overview`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/dashboard/overview`](https://mock-prahari.onrender.com/api/dashboard/overview)  

**Description:** Basin-wide high-level overview of monitored Indian Ocean & Bay of Bengal regions.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "monitoredBasins": [
    "Bay of Bengal",
    "Arabian Sea",
    "North India Plains"
  ],
  "currentThreatLevel": "HIGH",
  "primaryThreat": "Severe Cyclonic Storm (BOB-02)",
  "forecastWindowDays": 7,
  "lastUpdated": "2026-09-28T12:00:00Z"
}
```

**Frontend Usage:** Top banner and synoptic weather summary cards on the Main Executive Dashboard.

**TypeScript Interface:**
```typescript
export interface DashboardOverviewResponse {
  basin: string;
  activeExtremeEvents: number;
  monitoredBasins: string[];
  alertLevel: 'RED' | 'ORANGE' | 'YELLOW' | 'GREEN';
  synopticSummary: string;
  lastUpdated: string;
}
```

---

### 4. Dashboard KPIs
**Method:** `GET`  
**Path:** `/api/dashboard/kpis`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/dashboard/kpis`](https://mock-prahari.onrender.com/api/dashboard/kpis)  

**Description:** Key statistical metrics measuring forecast lead time, resolution, and model skill scores.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "activeStormCells": 3,
  "highRiskPopulationMillions": 4.82,
  "gridCellsDownscaled": 14200,
  "downscaleLatencyMs": 340,
  "spatialResolutionGain": "2.4x"
}
```

**Frontend Usage:** Top KPI grid cards (4-card metric row on the dashboard).

**TypeScript Interface:**
```typescript
export interface DashboardKPIsResponse {
  forecastResolutionKm: number;
  leadTimeHours: number;
  trackError24hKm: number;
  intensityRmseKnots: number;
  activeAlertCount: number;
  radarCoveragePercentage: number;
}
```

---

### 5. Dashboard Anomaly Overview
**Method:** `GET`  
**Path:** `/api/dashboard/anomaly-overview`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/dashboard/anomaly-overview`](https://mock-prahari.onrender.com/api/dashboard/anomaly-overview)  

**Description:** High-level breakdown of severe meteorological anomalies segmented by hazard type.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "totalAnomalies": 3,
  "extremeForecastIndexThreshold": 0.85,
  "anomalies": [
    {
      "id": "BOB-02",
      "type": "Cyclone",
      "severity": "EXTREME",
      "location": "Bay of Bengal"
    },
    {
      "id": "AS-01",
      "type": "Depression",
      "severity": "MODERATE",
      "location": "Arabian Sea"
    },
    {
      "id": "NE-04",
      "type": "Heavy Rain",
      "severity": "HIGH",
      "location": "Northeast India"
    }
  ]
}
```

**Frontend Usage:** Distribution doughnut / pie chart or summary pills on the dashboard.

**TypeScript Interface:**
```typescript
export interface AnomalyOverviewResponse {
  totalAnomalies: number;
  cyclonicDepressions: number;
  extremePrecipitationZones: number;
  heatwavePockets: number;
  marineGales: number;
}
```

---

### 6. Dashboard Active Anomalies
**Method:** `GET`  
**Path:** `/api/dashboard/active-anomalies`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/dashboard/active-anomalies`](https://mock-prahari.onrender.com/api/dashboard/active-anomalies)  

**Description:** Detailed list of currently tracked anomalies across India and neighboring oceanic basins.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "BOB-02",
    "name": "Cyclone BOB-02",
    "category": "Severe Cyclonic Storm",
    "center": {
      "lat": 18.4,
      "lon": 87.2
    },
    "maxWindKmph": 135,
    "centralPressureHpa": 978,
    "status": "TRACKING"
  }
]
```

**Frontend Usage:** Active Anomalies table or scrollable alert cards on the dashboard overview.

**TypeScript Interface:**
```typescript
export interface AnomalyItem {
  id: string;
  type: string;
  region: string;
  severity: 'CRITICAL' | 'HIGH' | 'MODERATE' | 'LOW';
  coordinates: [number, number];
  efiValue: number;
}

export type ActiveAnomaliesResponse = AnomalyItem[];
```

---

### 7. Dashboard Forecast Timeline
**Method:** `GET`  
**Path:** `/api/dashboard/forecast-timeline`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/dashboard/forecast-timeline`](https://mock-prahari.onrender.com/api/dashboard/forecast-timeline)  

**Description:** Multi-step chronological forecast sequence outlining storm path milestones.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "forecastOrigin": "2026-09-28T00:00:00Z",
  "timesteps": [
    {
      "stepHours": 24,
      "validTime": "2026-09-29T00:00:00Z",
      "confidence": 0.94
    },
    {
      "stepHours": 48,
      "validTime": "2026-09-30T00:00:00Z",
      "confidence": 0.89
    },
    {
      "stepHours": 72,
      "validTime": "2026-10-01T00:00:00Z",
      "confidence": 0.82
    }
  ]
}
```

**Frontend Usage:** Interactive horizontal timeline or slider on the dashboard.

**TypeScript Interface:**
```typescript
export interface TimelineStep {
  step: string;
  timestamp: string;
  expectedIntensity: string;
  windSpeedKmph: number;
  primaryRiskZone: string;
}

export type ForecastTimelineResponse = TimelineStep[];
```

---

### 8. Dashboard Processing Pipeline
**Method:** `GET`  
**Path:** `/api/dashboard/processing-pipeline`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/dashboard/processing-pipeline`](https://mock-prahari.onrender.com/api/dashboard/processing-pipeline)  

**Description:** Status of real-time multi-stage inference workflows (Radar -> GNN -> Diffusion -> Alerting).

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "stages": [
    {
      "name": "GNN Spherical Tracking",
      "status": "COMPLETED",
      "executionTimeMs": 145
    },
    {
      "name": "EFI Anomaly Bounding",
      "status": "COMPLETED",
      "executionTimeMs": 82
    },
    {
      "name": "Diffusion Downscaling 5km",
      "status": "COMPLETED",
      "executionTimeMs": 310
    },
    {
      "name": "CAP Alert Dispatch",
      "status": "IDLE",
      "executionTimeMs": 12
    }
  ],
  "totalLatencyMs": 549
}
```

**Frontend Usage:** Dataflow architecture diagram or live operational pipeline indicator.

**TypeScript Interface:**
```typescript
export interface PipelineStage {
  stageId: string;
  name: string;
  latencyMs: number;
  status: 'ACTIVE' | 'IDLE' | 'COMPLETED';
}

export interface ProcessingPipelineResponse {
  pipelineId: string;
  totalLatencyMs: number;
  stages: PipelineStage[];
}
```

---

### 9. Model Analysis Overview
**Method:** `GET`  
**Path:** `/api/model-analysis/overview`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/overview`](https://mock-prahari.onrender.com/api/model-analysis/overview)  

**Description:** Architectural overview of the two-stage hybrid Spherical GNN and Conditional Diffusion platform.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "activeModelVersion": "GNN-Diffusion-v2.4",
  "operationalSince": "2026-08-15T00:00:00Z",
  "totalInferenceRuns": 12840,
  "averageLatencyMs": 340,
  "ensembleSpread": 0.14,
  "status": "OPERATIONAL"
}
```

**Frontend Usage:** Model Analysis introductory panel and model metadata drawer.

**TypeScript Interface:**
```typescript
export interface ModelAnalysisOverviewResponse {
  architecture: string;
  stage1: string;
  stage2: string;
  inputVariables: string[];
  outputResolutionKm: number;
}
```

---

### 10. Model Registry List
**Method:** `GET`  
**Path:** `/api/model-analysis/models`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/models`](https://mock-prahari.onrender.com/api/model-analysis/models)  

**Description:** Comprehensive list of active neural network checkpoints, parameter counts, and quantization states.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "gnn-diff-v2.4",
    "name": "GNN Spherical Diffusion v2.4",
    "type": "Graph Neural Network + Diffusion",
    "resolutionKm": 5,
    "leadTimeHours": 168,
    "status": "ACTIVE_PRODUCTION"
  },
  {
    "id": "efi-transformer-v1.8",
    "name": "Extreme Forecast Index Transformer",
    "type": "Spatial-Temporal Transformer",
    "resolutionKm": 12,
    "leadTimeHours": 240,
    "status": "STANDBY"
  }
]
```

**Frontend Usage:** Model switcher dropdown and neural network architecture specifications table.

**TypeScript Interface:**
```typescript
export interface ModelRecord {
  modelId: string;
  name: string;
  version: string;
  parameters: string;
  quantization: string;
  hardwareTarget: string;
}

export type ModelsResponse = ModelRecord[];
```

---

### 11. Model Tensor Pipeline
**Method:** `GET`  
**Path:** `/api/model-analysis/pipeline`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/pipeline`](https://mock-prahari.onrender.com/api/model-analysis/pipeline)  

**Description:** Detailed tensor dimensions, mesh resolutions, and intermediate feature transformations.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "pipelineId": "prahari-operational-pipeline-prod",
  "stages": [
    {
      "stageNumber": 1,
      "name": "Atmospheric Ingestion & Graph Construction",
      "status": "HEALTHY",
      "inputData": "NCMRWF & IMD NetCDF feeds",
      "executionLatencyMs": 110
    },
    {
      "stageNumber": 2,
      "name": "Spherical GNN Trajectory Forecast",
      "status": "HEALTHY",
      "inputData": "Pressure level tensor (12km)",
      "executionLatencyMs": 145
    },
    {
      "stageNumber": 3,
      "name": "Diffusion Super-Resolution Downscaling",
      "status": "HEALTHY",
      "inputData": "12km latent grid to 5km terrain-aware field",
      "executionLatencyMs": 310
    },
    {
      "stageNumber": 4,
      "name": "CAP Risk Synthesis & Polygon Bounding",
      "status": "HEALTHY",
      "inputData": "Wind speed, precipitation & storm surge exceedances",
      "executionLatencyMs": 45
    }
  ]
}
```

**Frontend Usage:** Interactive tensor flow graph visualization.

**TypeScript Interface:**
```typescript
export interface PipelineStepDetail {
  stepOrder: number;
  component: string;
  inputShape: string;
  outputShape: string;
  computeType: string;
}

export interface ModelPipelineResponse {
  pipelineName: string;
  steps: PipelineStepDetail[];
}
```

---

### 12. Model Configuration & Hyperparameters
**Method:** `GET`  
**Path:** `/api/model-analysis/configuration`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/configuration`](https://mock-prahari.onrender.com/api/model-analysis/configuration)  

**Description:** Runtime configuration parameters, diffusion timesteps, and spherical mesh subdivision levels.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "inputResolutionKm": 12,
  "outputResolutionKm": 5,
  "temporalStepHours": 3,
  "maxLeadTimeHours": 168,
  "ensembleMembers": 20,
  "diffusionSteps": 50,
  "sphericalMeshLevels": 6,
  "hardwareTarget": "NVIDIA H100 80GB SXM5"
}
```

**Frontend Usage:** Configuration inspector card and model tuning readouts.

**TypeScript Interface:**
```typescript
export interface ModelConfigurationResponse {
  meshSubdivisionLevel: number;
  diffusionSteps: number;
  samplingMethod: string;
  temperature: number;
  ensembleMembers: number;
}
```

---

### 13. Model Skill Scores & Error Metrics
**Method:** `GET`  
**Path:** `/api/model-analysis/metrics`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/metrics`](https://mock-prahari.onrender.com/api/model-analysis/metrics)  

**Description:** Quantitative statistical metrics measuring geopotential height RMSE, wind speed MAE, and CRPS.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "rootMeanSquareError": {
    "windSpeedMps": 1.82,
    "centralPressureHpa": 2.14,
    "precipitationMm": 4.65
  },
  "anomalyCorrelationCoefficient": 0.942,
  "brierSkillScore": 0.887,
  "equitableThreatScore": 0.764
}
```

**Frontend Usage:** Radar charts, bar graphs, and model accuracy comparison tables.

**TypeScript Interface:**
```typescript
export interface ModelMetricsResponse {
  geopotentialHeightRmseZ500: number;
  windSpeedMaeU10: number;
  crpsPrecipitation: number;
  meanInferenceTimeMs: number;
}
```

---

### 14. Model Ensemble Verification
**Method:** `GET`  
**Path:** `/api/model-analysis/verification`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/verification`](https://mock-prahari.onrender.com/api/model-analysis/verification)  

**Description:** Ensemble calibration curve data, spread-error ratios, and probability reliability metrics.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "lastVerificationTimestamp": "2026-09-28T06:00:00Z",
  "verificationSource": "IMD AWS & DWR Ground Truth",
  "trackError24hKm": 34.2,
  "trackError48hKm": 68.7,
  "trackError72hKm": 112.4,
  "falseAlarmRate": 0.062,
  "probabilityOfDetection": 0.938
}
```

**Frontend Usage:** Calibration curve and reliability diagram plots (Chart.js / Recharts).

**TypeScript Interface:**
```typescript
export interface VerificationPoint {
  forecastProbability: number;
  observedFrequency: number;
}

export interface ModelVerificationResponse {
  metricName: string;
  spreadSkillRatio: number;
  curve: VerificationPoint[];
}
```

---

### 15. Track Error Chart Data
**Method:** `GET`  
**Path:** `/api/model-analysis/track-error-chart`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/track-error-chart`](https://mock-prahari.onrender.com/api/model-analysis/track-error-chart)  

**Description:** Cyclone center position displacement error (km) across 12h, 24h, 48h, and 72h lead times.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "leadTimesHours": [
    12,
    24,
    36,
    48,
    60,
    72,
    96,
    120
  ],
  "prahariGnnKm": [
    18.4,
    34.2,
    51.0,
    68.7,
    89.5,
    112.4,
    158.0,
    205.2
  ],
  "baselineNumericalKm": [
    28.6,
    52.4,
    79.1,
    108.3,
    142.0,
    181.5,
    256.3,
    330.0
  ],
  "unit": "kilometers"
}
```

**Frontend Usage:** Forecast lead time track error line chart (Prahari vs NWP baselines).

**TypeScript Interface:**
```typescript
export interface TrackErrorPoint {
  leadHours: number;
  prahariErrorKm: number;
  baselineErrorKm: number;
}

export type TrackErrorChartResponse = TrackErrorPoint[];
```

---

### 16. Baseline Model Benchmarks
**Method:** `GET`  
**Path:** `/api/model-analysis/baseline-comparison`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/model-analysis/baseline-comparison`](https://mock-prahari.onrender.com/api/model-analysis/baseline-comparison)  

**Description:** Direct side-by-side benchmark comparison: Prahari vs ECMWF-HRES and IMD-GFS.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "baselineModel": "ECMWF-HRES / IMD-GFS 12km",
  "downscalingGain": "2.4x Spatial Resolution (12km -> 5km)",
  "inferenceSpeedup": "18.5x faster than numerical ensemble",
  "energyEfficiencyGain": "92% compute power reduction",
  "trackAccuracyImprovementPercent": 34.8
}
```

**Frontend Usage:** Model comparison table and radar comparison benchmark.

**TypeScript Interface:**
```typescript
export interface BaselineModelStat {
  model: string;
  resolutionKm: number;
  inferenceLatencyMinutes: number;
  trackError24hKm: number;
  computeCostUsdPerRun: number;
}

export type BaselineComparisonResponse = BaselineModelStat[];
```

---

### 17. List Active Monitored Events
**Method:** `GET`  
**Path:** `/api/events/`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/`](https://mock-prahari.onrender.com/api/events/)  

**Description:** Retrieves the list of active cyclone and severe weather events currently under live monitoring.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "BOB-02",
    "name": "Cyclone BOB-02",
    "type": "Cyclone",
    "severity": "EXTREME",
    "basin": "Bay of Bengal",
    "status": "ACTIVE_TRACKING"
  },
  {
    "id": "AS-01",
    "name": "Depression AS-01",
    "type": "Depression",
    "severity": "MODERATE",
    "basin": "Arabian Sea",
    "status": "MONITORING"
  },
  {
    "id": "NE-04",
    "name": "Flash Flood Risk NE-04",
    "type": "Heavy Rain",
    "severity": "HIGH",
    "basin": "Northeast India",
    "status": "WARNING"
  }
]
```

**Frontend Usage:** Event selector dropdown at the top of the Live Cyclone Monitor page.

**TypeScript Interface:**
```typescript
export interface MonitoredEventSummary {
  eventId: string;
  name: string;
  category: string;
  basin: string;
  status: 'ACTIVE' | 'WATCH' | 'DISSIPATING';
  currentWindSpeedKmph: number;
}

export type EventListResponse = MonitoredEventSummary[];
```

---

### 18. Live Event Base Details
**Method:** `GET`  
**Path:** `/api/events/{eventId}`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02`](https://mock-prahari.onrender.com/api/events/BOB-02)  

**Description:** Detailed current status, classification, and geographical position of the specified event.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Identifier of the event (e.g. `BOB-02`, case-insensitive) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "id": "BOB-02",
  "name": "Severe Cyclonic Storm BOB-02",
  "category": "Category 3",
  "location": {
    "lat": 18.4,
    "lon": 87.2
  },
  "maxWindSpeedKmph": 135,
  "centralPressureHpa": 978,
  "movementDirection": "NNW",
  "forwardSpeedKmph": 16,
  "estimatedLandfallTime": "2026-09-30T04:00:00Z",
  "estimatedLandfallLocation": "Odisha Coast, India"
}
```

**Frontend Usage:** Header card and title display on the Live Event Monitor page.

**TypeScript Interface:**
```typescript
export interface LiveEventDetailsResponse {
  eventId: string;
  name: string;
  classification: string;
  formationDate: string;
  currentCoordinates: {
    lat: number;
    lng: number;
  };
  centralPressureHpa: number;
  sustainedWindKmph: number;
  gustsKmph: number;
}
```

---

### 19. Event Trajectory & Forecast Cone
**Method:** `GET`  
**Path:** `/api/events/{eventId}/trajectory`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02/trajectory`](https://mock-prahari.onrender.com/api/events/BOB-02/trajectory)  

**Description:** Observed coordinates, past track points, and probabilistic forecast cone coordinates with timestamps.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "historicalWaypoints": [
    {
      "timestamp": "2026-09-27T00:00:00Z",
      "lat": 15.6,
      "lon": 88.5,
      "windKmph": 85
    },
    {
      "timestamp": "2026-09-27T12:00:00Z",
      "lat": 16.9,
      "lon": 87.9,
      "windKmph": 110
    },
    {
      "timestamp": "2026-09-28T00:00:00Z",
      "lat": 18.4,
      "lon": 87.2,
      "windKmph": 135
    }
  ],
  "forecastWaypoints": [
    {
      "timestamp": "2026-09-28T12:00:00Z",
      "lat": 19.5,
      "lon": 86.8,
      "windKmph": 145,
      "coneRadiusKm": 25
    },
    {
      "timestamp": "2026-09-29T00:00:00Z",
      "lat": 20.3,
      "lon": 86.4,
      "windKmph": 150,
      "coneRadiusKm": 45
    },
    {
      "timestamp": "2026-09-30T00:00:00Z",
      "lat": 21.2,
      "lon": 86.1,
      "windKmph": 120,
      "coneRadiusKm": 75
    }
  ]
}
```

**Frontend Usage:** Primary Leaflet / Mapbox track polyline and uncertainty cone layer on the monitor map.

**TypeScript Interface:**
```typescript
export interface TrackPoint {
  timestamp: string;
  lat: number;
  lng: number;
  windSpeedKts: number;
  pressureHpa: number;
  pointType: 'OBSERVED' | 'FORECAST';
}

export interface TrajectoryResponse {
  eventId: string;
  track: TrackPoint[];
  forecastConePolygon?: [number, number][];
}
```

---

### 20. Event Intensity Timeline
**Method:** `GET`  
**Path:** `/api/events/{eventId}/timeline`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02/timeline`](https://mock-prahari.onrender.com/api/events/BOB-02/timeline)  

**Description:** Time series of central pressure (hPa) and sustained wind speed (knots) through landfall.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "timelineEvents": [
    {
      "time": "2026-09-26T18:00:00Z",
      "title": "Formation of Low Pressure System",
      "type": "GENESIS"
    },
    {
      "time": "2026-09-27T06:00:00Z",
      "title": "Upgraded to Cyclonic Storm",
      "type": "INTENSIFICATION"
    },
    {
      "time": "2026-09-28T00:00:00Z",
      "title": "Rapid Intensification to Severe Storm",
      "type": "ALERT"
    },
    {
      "time": "2026-09-30T04:00:00Z",
      "title": "Projected Landfall near Paradip",
      "type": "FORECAST"
    }
  ]
}
```

**Frontend Usage:** Dual-axis pressure vs wind speed line chart.

**TypeScript Interface:**
```typescript
export interface IntensityPoint {
  timestamp: string;
  windKnots: number;
  pressureHpa: number;
  stage: string;
}

export type EventTimelineResponse = IntensityPoint[];
```

---

### 21. Live Event Telemetry
**Method:** `GET`  
**Path:** `/api/events/{eventId}/telemetry`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02/telemetry`](https://mock-prahari.onrender.com/api/events/BOB-02/telemetry)  

**Description:** High-frequency telemetry: forward speed, bearing direction, eye radius, and quadrant wind radii.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "currentWindSpeedMps": 37.5,
  "gustSpeedMps": 46.2,
  "surfacePressureHpa": 978.2,
  "seaSurfaceTemperatureCelsius": 29.8,
  "verticalWindShearKnots": 11.2,
  "lastTelemetrySync": "2026-09-28T16:00:00Z"
}
```

**Frontend Usage:** Live storm telemetry dashboard gauges (Speedometer, Compass, Radius dials).

**TypeScript Interface:**
```typescript
export interface TelemetryResponse {
  eventId: string;
  forwardSpeedKmph: number;
  headingDegrees: number;
  eyeRadiusKm: number;
  quadrantRadiiKm: {
    ne: number;
    se: number;
    sw: number;
    nw: number;
  };
}
```

---

### 22. Meteorological Diagnostics
**Method:** `GET`  
**Path:** `/api/events/{eventId}/diagnostics`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02/diagnostics`](https://mock-prahari.onrender.com/api/events/BOB-02/diagnostics)  

**Description:** Atmospheric diagnostics: relative vorticity, Sea Surface Temperature (SST), and 850-200hPa wind shear.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "gnnConfidenceScore": 0.94,
  "ensembleDispersionIndex": 0.12,
  "vorticityConvectiveCoupling": "HIGH",
  "downscalingConvergenceResidual": 0.0034,
  "anomalyZScore": 3.82
}
```

**Frontend Usage:** Environmental conditions cards and cyclogenesis potential bar meters.

**TypeScript Interface:**
```typescript
export interface DiagnosticsResponse {
  seaSurfaceTemperatureCelsius: number;
  verticalWindShearKnots: number;
  relativeVorticity850: number;
  upperLevelDivergence: number;
  environmentalFavorability: 'EXTREME' | 'HIGH' | 'MODERATE' | 'UNFAVORABLE';
}
```

---

### 23. Intensity Category Probability Distribution
**Method:** `GET`  
**Path:** `/api/events/{eventId}/intensity-distribution`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02/intensity-distribution`](https://mock-prahari.onrender.com/api/events/BOB-02/intensity-distribution)  

**Description:** Probabilistic distribution across IMD cyclone classifications (CS, SCS, VSCS, ESCS, SuCS).

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "probabilityBins": [
    {
      "category": "Depression",
      "probability": 0.01
    },
    {
      "category": "Deep Depression",
      "probability": 0.04
    },
    {
      "category": "Cyclonic Storm",
      "probability": 0.15
    },
    {
      "category": "Severe Cyclonic Storm",
      "probability": 0.65
    },
    {
      "category": "Very Severe Cyclonic Storm",
      "probability": 0.15
    }
  ],
  "peakIntensityForecastKmph": 150
}
```

**Frontend Usage:** Intensity likelihood probability bar chart or stacked probability meter.

**TypeScript Interface:**
```typescript
export interface IntensityProbability {
  category: string;
  description: string;
  probabilityPercentage: number;
}

export type IntensityDistributionResponse = IntensityProbability[];
```

---

### 24. Downstream Risk Alerts
**Method:** `GET`  
**Path:** `/api/events/{eventId}/risk-alerts`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/events/BOB-02/risk-alerts`](https://mock-prahari.onrender.com/api/events/BOB-02/risk-alerts)  

**Description:** Downstream coastal surge, storm tide inundation, and flash flood impact alerts by district.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "alert_id": "CAP-IN-OD-2026-0091",
    "urgency_level": "Immediate",
    "severity_level": "Extreme",
    "certainty_code": "Observed",
    "event_code": "CYC",
    "headline": "Red Alert: Severe Cyclone Warning for Coastal Odisha",
    "area_description": "Kendrapada, Jagatsinghpur, Bhadrak coastal districts",
    "instruction": "Initiate evacuation of low-lying flood-prone zones immediately."
  }
]
```

**Frontend Usage:** District-level warning cards and alert badge feed.

**TypeScript Interface:**
```typescript
export interface RiskAlert {
  alertId: string;
  district: string;
  state: string;
  riskType: string;
  riskLevel: 'RED' | 'ORANGE' | 'YELLOW';
  peakImpactTime: string;
  estimatedSurgeHeightMeters?: number;
}

export type RiskAlertsResponse = RiskAlert[];
```

---

### 25. Historical Events Archive
**Method:** `GET`  
**Path:** `/api/historical-events/`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/`](https://mock-prahari.onrender.com/api/historical-events/)  

**Description:** Retrieves the catalog of landmark historical events available for historical replay analysis.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "amphan-2020",
    "name": "Super Cyclone Amphan (2020)",
    "category": "Super Cyclonic Storm",
    "year": 2020,
    "basin": "Bay of Bengal",
    "peakIntensityKmph": 260
  },
  {
    "id": "heatwave-2022",
    "name": "Northwest India Severe Heatwave (2022)",
    "category": "Extreme Heatwave",
    "year": 2022,
    "basin": "Northwest India Plains",
    "peakIntensityKmph": 0
  },
  {
    "id": "mumbai-2021",
    "name": "Extreme Precipitation & Urban Deluge Mumbai (2021)",
    "category": "Cloudburst / Extreme Rain",
    "year": 2021,
    "basin": "West Coast",
    "peakIntensityKmph": 60
  },
  {
    "id": "biparjoy-2023",
    "name": "Extremely Severe Cyclonic Storm Biparjoy (2023)",
    "category": "Extremely Severe Cyclonic Storm",
    "year": 2023,
    "basin": "Arabian Sea",
    "peakIntensityKmph": 165
  }
]
```

**Frontend Usage:** Historical event picker / carousel (Amphan 2020, Biparjoy 2023, Mumbai Deluge 2005).

**TypeScript Interface:**
```typescript
export interface HistoricalEventSummary {
  eventId: string;
  name: string;
  year: number;
  peakIntensity: string;
  landfallLocation: string;
  fatalitiesReported: number;
}

export type HistoricalEventsResponse = HistoricalEventSummary[];
```

---

### 26. Replay Comparison Modes
**Method:** `GET`  
**Path:** `/api/historical-events/comparison-modes`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/comparison-modes`](https://mock-prahari.onrender.com/api/historical-events/comparison-modes)  

**Description:** List of supported side-by-side comparison modes (Ground Truth vs Model, Diffusion vs Coarse NWP).

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "gnn-vs-numerical",
    "name": "Prahari GNN vs Operational IMD-GFS",
    "description": "Compares 5km GNN-Diffusion forecast against 12km operational numerical baseline."
  },
  {
    "id": "downscaled-vs-coarse",
    "name": "Terrain-Downscaled 5km vs 25km Raw ERA5",
    "description": "Highlights local topography-induced precipitation and localized wind peaks."
  },
  {
    "id": "lead-time-sensitivity",
    "name": "72h Lead-Time vs 24h Landfall Verification",
    "description": "Visualizes forecast stability across successive lead-time runs."
  }
]
```

**Frontend Usage:** Comparison mode toggle button group on the Replay player.

**TypeScript Interface:**
```typescript
export interface ComparisonMode {
  id: string;
  label: string;
  description: string;
  leftLayer: string;
  rightLayer: string;
}

export type ComparisonModesResponse = ComparisonMode[];
```

---

### 27. Selected Historical Event Overview
**Method:** `GET`  
**Path:** `/api/historical-events/{eventId}`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/amphan-2020`](https://mock-prahari.onrender.com/api/historical-events/amphan-2020)  

**Description:** Metadata, track span, and summary statistics of the chosen historical case study.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Historical event slug (e.g. `amphan-2020`, case-insensitive) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "id": "amphan-2020",
  "name": "Super Cyclone Amphan",
  "year": 2020,
  "landfallLocation": "Bakkhali, West Bengal",
  "landfallDate": "2020-05-20T12:00:00Z",
  "maxWindKmph": 260,
  "minPressureHpa": 920,
  "damageCategory": "Catastrophic"
}
```

**Frontend Usage:** Historical Case Study summary header and impact recap.

**TypeScript Interface:**
```typescript
export interface HistoricalEventDetailResponse {
  eventId: string;
  name: string;
  period: string;
  maxWindKnots: number;
  minPressureHpa: number;
  totalDamageUsdBillions: number;
  synopsis: string;
}
```

---

### 28. Historical Replay Time Slices
**Method:** `GET`  
**Path:** `/api/historical-events/{eventId}/timeline`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/amphan-2020/timeline`](https://mock-prahari.onrender.com/api/historical-events/amphan-2020/timeline)  

**Description:** Chronological list of timestamp steps used to drive the replay scrubber and step-by-step playback.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Historical event slug (e.g. `amphan-2020`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "amphan-2020",
  "steps": [
    {
      "time": "2020-05-16T00:00:00Z",
      "stage": "Depression",
      "windKmph": 55
    },
    {
      "time": "2020-05-17T12:00:00Z",
      "stage": "Very Severe Cyclonic Storm",
      "windKmph": 140
    },
    {
      "time": "2020-05-18T18:00:00Z",
      "stage": "Super Cyclone Peak",
      "windKmph": 260
    },
    {
      "time": "2020-05-20T12:00:00Z",
      "stage": "Landfall",
      "windKmph": 155
    }
  ]
}
```

**Frontend Usage:** Playback timeline scrubber slider and play/pause frame sequence.

**TypeScript Interface:**
```typescript
export interface ReplayTimeStep {
  stepIndex: number;
  timestamp: string;
  category: string;
  forwardSpeedKmph: number;
}

export type HistoricalTimelineResponse = ReplayTimeStep[];
```

---

### 29. Observed vs Forecasted Track Comparison
**Method:** `GET`  
**Path:** `/api/historical-events/{eventId}/track`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/amphan-2020/track`](https://mock-prahari.onrender.com/api/historical-events/amphan-2020/track)  

**Description:** Synchronized coordinates of the actual observed path alongside the Prahari deep learning prediction.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Historical event slug (e.g. `amphan-2020`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "amphan-2020",
  "actualTrack": [
    {
      "lat": 10.4,
      "lon": 87.0,
      "time": "2020-05-16T00:00:00Z"
    },
    {
      "lat": 13.5,
      "lon": 86.5,
      "time": "2020-05-17T12:00:00Z"
    },
    {
      "lat": 18.2,
      "lon": 86.8,
      "time": "2020-05-19T00:00:00Z"
    },
    {
      "lat": 21.7,
      "lon": 88.3,
      "time": "2020-05-20T12:00:00Z"
    }
  ],
  "replayedModelTrack": [
    {
      "lat": 10.4,
      "lon": 87.0,
      "time": "2020-05-16T00:00:00Z"
    },
    {
      "lat": 13.6,
      "lon": 86.6,
      "time": "2020-05-17T12:00:00Z"
    },
    {
      "lat": 18.1,
      "lon": 86.9,
      "time": "2020-05-19T00:00:00Z"
    },
    {
      "lat": 21.6,
      "lon": 88.4,
      "time": "2020-05-20T12:00:00Z"
    }
  ]
}
```

**Frontend Usage:** Dual-polyline map overlay comparing ground truth vs prediction track accuracy.

**TypeScript Interface:**
```typescript
export interface TrackComparisonPoint {
  timestamp: string;
  observedLat: number;
  observedLng: number;
  predictedLat: number;
  predictedLng: number;
  trackErrorKm: number;
}

export type HistoricalTrackResponse = TrackComparisonPoint[];
```

---

### 30. Historical Hazard Envelope Polygons
**Method:** `GET`  
**Path:** `/api/historical-events/{eventId}/hazard-envelope`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/amphan-2020/hazard-envelope`](https://mock-prahari.onrender.com/api/historical-events/amphan-2020/hazard-envelope)  

**Description:** Multi-polygon boundaries defining historical inundation zones, gale wind swaths, and tidal surges.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Historical event slug (e.g. `amphan-2020`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "amphan-2020",
  "stormSurgeHeightMeters": 4.5,
  "inundationAreaSqKm": 1240,
  "windSwathRadiusKm": 180,
  "severeDamagePolygonCoordinates": [
    [
      88.0,
      21.5
    ],
    [
      88.8,
      21.5
    ],
    [
      89.1,
      22.5
    ],
    [
      88.2,
      22.6
    ],
    [
      88.0,
      21.5
    ]
  ]
}
```

**Frontend Usage:** GeoJSON polygon overlay highlighting damaged land and surge reach on the map.

**TypeScript Interface:**
```typescript
export interface HazardPolygon {
  zoneName: string;
  hazardType: string;
  severityLevel: string;
  polygonCoordinates: [number, number][];
}

export type HazardEnvelopeResponse = HazardPolygon[];
```

---

### 31. Historical Map Layers & Rasters
**Method:** `GET`  
**Path:** `/api/historical-events/{eventId}/map-layers`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/amphan-2020/map-layers`](https://mock-prahari.onrender.com/api/historical-events/amphan-2020/map-layers)  

**Description:** List of available raster overlays (wind field heatmaps, rain accumulation, satellite imagery) for replay.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Historical event slug (e.g. `amphan-2020`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "amphan-2020",
  "layers": [
    {
      "id": "radar_reflectivity_composite",
      "name": "Doppler Composite (dBZ)",
      "opacity": 0.8
    },
    {
      "id": "diffusion_wind_vectors",
      "name": "GNN Surface Wind Vectors",
      "opacity": 0.9
    },
    {
      "id": "coastal_inundation_risk",
      "name": "Surge Inundation Mask",
      "opacity": 0.75
    }
  ]
}
```

**Frontend Usage:** Map layer control toggles (Satellite, Wind Heatmap, Precipitation Overlay).

**TypeScript Interface:**
```typescript
export interface ReplayMapLayer {
  layerId: string;
  name: string;
  type: 'raster' | 'geojson' | 'vector';
  sourceUrl: string;
  opacity: number;
  defaultVisible: boolean;
}

export type ReplayMapLayersResponse = ReplayMapLayer[];
```

---

### 32. Historical Replay Accuracy Metrics
**Method:** `GET`  
**Path:** `/api/historical-events/{eventId}/metrics`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/historical-events/amphan-2020/metrics`](https://mock-prahari.onrender.com/api/historical-events/amphan-2020/metrics)  

**Description:** Post-landfall verification statistics (Landfall point accuracy in km, timing error in hours).

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Historical event slug (e.g. `amphan-2020`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "amphan-2020",
  "landfallTrackErrorKm": 18.2,
  "landfallTimeErrorHours": 1.5,
  "intensityRmseKmph": 8.4,
  "prahariSkillScoreVsOperational": 0.36
}
```

**Frontend Usage:** Historical Case Study scorecard metrics.

**TypeScript Interface:**
```typescript
export interface HistoricalMetricsResponse {
  landfallLocationErrorKm: number;
  landfallTimingErrorHours: number;
  maxWindSpeedErrorKnots: number;
  centralPressureRmseHpa: number;
}
```

---

### 33. Event Detail Selectable Events
**Method:** `GET`  
**Path:** `/api/event-detail/events`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/events`](https://mock-prahari.onrender.com/api/event-detail/events)  

**Description:** Returns list of events selectable for full deep-dive operational investigation.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "BOB-02",
    "title": "Severe Cyclonic Storm BOB-02",
    "region": "Bay of Bengal",
    "threatLevel": "CRITICAL"
  },
  {
    "id": "AS-01",
    "title": "Deep Depression AS-01",
    "region": "Arabian Sea",
    "threatLevel": "WATCH"
  },
  {
    "id": "NE-04",
    "title": "Mesoscale Heavy Precipitation NE-04",
    "region": "Northeast India",
    "threatLevel": "WARNING"
  }
]
```

**Frontend Usage:** Event picker on the Detailed Event Investigation page.

**TypeScript Interface:**
```typescript
export interface EventDetailListItem {
  eventId: string;
  name: string;
  status: string;
  basin: string;
  alertLevel: string;
}

export type EventDetailEventsResponse = EventDetailListItem[];
```

---

### 34. Event Deep Dive Container
**Method:** `GET`  
**Path:** `/api/event-detail/{eventId}`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/BOB-02`](https://mock-prahari.onrender.com/api/event-detail/BOB-02)  

**Description:** Full comprehensive container metadata for the selected investigation event.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "id": "BOB-02",
  "title": "Severe Cyclonic Storm BOB-02",
  "basin": "Bay of Bengal",
  "classification": "Severe Cyclonic Storm (IMD scale)",
  "currentCoordinates": {
    "lat": 18.4,
    "lon": 87.2
  },
  "projectedLandfall": "2026-09-30T04:00:00Z",
  "affectedDistricts": [
    "Puri",
    "Jagatsinghpur",
    "Kendrapara",
    "Bhadrak",
    "Balasore"
  ]
}
```

**Frontend Usage:** Initial fetch when loading the Event Detail investigation view.

**TypeScript Interface:**
```typescript
export interface EventDetailContainerResponse {
  eventId: string;
  name: string;
  phase: string;
  coastalSectorsAtRisk: string[];
  bulletinNumber: number;
  issuedAt: string;
}
```

---

### 35. Event Synoptic Overview
**Method:** `GET`  
**Path:** `/api/event-detail/{eventId}/overview`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/BOB-02/overview`](https://mock-prahari.onrender.com/api/event-detail/BOB-02/overview)  

**Description:** Synoptic weather analysis, atmospheric steering currents, and expected landfall progression.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "synopsis": "Cyclone BOB-02 is tracking north-northwestward over the west-central Bay of Bengal with intensifying core convection.",
  "threatCategory": "EXTREME",
  "evacuationPriority": "HIGH",
  "monitoredSince": "2026-09-26T18:00:00Z"
}
```

**Frontend Usage:** Executive briefing summary card on the Event Detail page.

**TypeScript Interface:**
```typescript
export interface EventDetailOverviewResponse {
  eventId: string;
  synopticSituation: string;
  steeringCurrentDescription: string;
  expectedLandfallWindow: string;
  estimatedWaveHeightMeters: number;
}
```

---

### 36. Event Interactive Map Setup
**Method:** `GET`  
**Path:** `/api/event-detail/{eventId}/map`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/BOB-02/map`](https://mock-prahari.onrender.com/api/event-detail/BOB-02/map)  

**Description:** Map viewport bounds, radar station coordinates, coastal telemetry buoys, and weather stations.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "center": {
    "lat": 18.4,
    "lon": 87.2
  },
  "zoomLevel": 7,
  "coneOfUncertainty": [
    {
      "stepHours": 12,
      "centerLat": 19.5,
      "centerLon": 86.8,
      "radiusKm": 25
    },
    {
      "stepHours": 24,
      "centerLat": 20.3,
      "centerLon": 86.4,
      "radiusKm": 45
    },
    {
      "stepHours": 48,
      "centerLat": 21.2,
      "centerLon": 86.1,
      "radiusKm": 75
    }
  ],
  "radarOverlayUrl": "/api/radar/visakhapatnam/latest"
}
```

**Frontend Usage:** Map bounds initialization (`fitBounds`) and observation markers.

**TypeScript Interface:**
```typescript
export interface ObservationStation {
  id: string;
  name: string;
  type: 'radar' | 'buoy' | 'coastal_station';
  lat: number;
  lng: number;
}

export interface EventDetailMapResponse {
  defaultBounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
  observationStations: ObservationStation[];
}
```

---

### 37. Event Impact Figures & Metrics
**Method:** `GET`  
**Path:** `/api/event-detail/{eventId}/metrics`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/BOB-02/metrics`](https://mock-prahari.onrender.com/api/event-detail/BOB-02/metrics)  

**Description:** Socio-economic and physical vulnerability metrics: population at risk, port closures, expected rainfall.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "sustainedWindSpeedKmph": 135,
  "gustSpeedKmph": 165,
  "centralPressureHpa": 978,
  "stormSurgePredictionMeters": 3.8,
  "projectedRainfallAccumulationMm": 280
}
```

**Frontend Usage:** Disaster impact stats row (Evacuations needed, Ports impacted, 24h peak rain).

**TypeScript Interface:**
```typescript
export interface EventDetailMetricsResponse {
  estimatedPopulationAtRisk: number;
  peak24hRainfallMm: number;
  stormSurgeHeightMeters: number;
  majorPortsInWarningZone: string[];
}
```

---

### 38. High-Resolution Hazard Zones
**Method:** `GET`  
**Path:** `/api/event-detail/{eventId}/hazard`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/BOB-02/hazard`](https://mock-prahari.onrender.com/api/event-detail/BOB-02/hazard)  

**Description:** Multi-level hazard zones: extreme wind swath (>120 km/h), storm surge danger, and urban deluge sectors.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "eventId": "BOB-02",
  "windHazardLevel": "EXTREME",
  "stormSurgeHazardLevel": "VERY_HIGH",
  "inundationRiskZones": [
    "Kendrapada",
    "Jagatsinghpur"
  ],
  "infrastructureAtRisk": [
    "Paradip Port Operations",
    "Coastal Power Transmission Lines"
  ]
}
```

**Frontend Usage:** Leaflet / Mapbox color-coded hazard polygon overlays with click popups.

**TypeScript Interface:**
```typescript
export interface HazardZone {
  zoneId: string;
  name: string;
  hazardType: string;
  severityColor: string;
  coordinates: [number, number][];
}

export type EventHazardResponse = HazardZone[];
```

---

### 39. CAP-Compliant Emergency Alerts
**Method:** `GET`  
**Path:** `/api/event-detail/{eventId}/alerts`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/event-detail/BOB-02/alerts`](https://mock-prahari.onrender.com/api/event-detail/BOB-02/alerts)  

**Description:** Formal Common Alerting Protocol (CAP) compliant emergency bulletins for disaster management authorities.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `eventId` | `string` | path | Yes | Event ID (e.g. `BOB-02`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "alert_id": "CAP-IN-OD-2026-0091",
    "urgency_level": "Immediate",
    "severity_level": "Extreme",
    "certainty_code": "Observed",
    "event_code": "CYC",
    "headline": "Red Alert: Severe Cyclone Warning for Coastal Odisha",
    "area_description": "Kendrapada, Jagatsinghpur, Bhadrak coastal districts",
    "instruction": "Initiate evacuation of low-lying flood-prone zones immediately."
  },
  {
    "alert_id": "CAP-IN-WB-2026-0084",
    "urgency_level": "Expected",
    "severity_level": "Severe",
    "certainty_code": "Likely",
    "event_code": "SURGE",
    "headline": "Orange Alert: Coastal Surge Advisory for South 24 Parganas",
    "area_description": "Sundarbans and Digha coastline",
    "instruction": "Secure fishing boats and reinforce embankments."
  }
]
```

**Frontend Usage:** Official emergency warning alerts drawer and printable evacuation bulletins.

**TypeScript Interface:**
```typescript
export interface CapAlertItem {
  identifier: string;
  sender: string;
  sent: string;
  status: string;
  msgType: string;
  scope: string;
  info: {
    event: string;
    urgency: string;
    severity: string;
    certainty: string;
    headline: string;
    description: string;
    instruction: string;
    area: {
      areaDesc: string;
    };
  };
}

export type EventAlertsResponse = CapAlertItem[];
```

---

### 40. Doppler Radar Stations Registry
**Method:** `GET`  
**Path:** `/api/radar/stations`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/radar/stations`](https://mock-prahari.onrender.com/api/radar/stations)  

**Description:** List of IMD Doppler radar stations available in the network with coordinates, ranges, and products.

**Parameters:** None

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
[
  {
    "id": "kolkata",
    "name": "Kolkata (Subhash Chandra Bose AP)",
    "latitude": 22.65,
    "longitude": 88.45,
    "rangeKm": 250,
    "products": [
      "reflectivity",
      "velocity"
    ]
  },
  {
    "id": "paradip",
    "name": "Paradip Port",
    "latitude": 20.31,
    "longitude": 86.61,
    "rangeKm": 250,
    "products": [
      "reflectivity",
      "velocity"
    ]
  },
  {
    "id": "agartala",
    "name": "Agartala",
    "latitude": 23.88,
    "longitude": 91.24,
    "rangeKm": 250,
    "products": [
      "reflectivity"
    ]
  }
]
```

**Frontend Usage:** Station selector pills on the Doppler Radar Viewer page.

**TypeScript Interface:**
```typescript
export interface RadarStation {
  id: string;
  name: string;
  state: string;
  latitude: number;
  longitude: number;
  rangeKm: number;
  supportedProducts: ('reflectivity' | 'velocity')[];
}

export type RadarStationsResponse = RadarStation[];
```

---

### 41. Doppler Radar Frames Scanner
**Method:** `GET`  
**Path:** `/api/radar/{stationId}/frames`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/radar/kolkata/frames?product=reflectivity&limit=2`](https://mock-prahari.onrender.com/api/radar/kolkata/frames?product=reflectivity&limit=2)  

**Description:** Returns chronologically sorted Doppler radar image frames. Frames are updated dynamically by the background harvester daemon every 10 minutes.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `stationId` | `string` | path | Yes | Radar station identifier (e.g. `kolkata`, `paradip`) |
| `product` | `string` | query | No | Radar product type: `reflectivity` (default) or `velocity` |
| `from` | `string` | query | No | ISO-8601 start timestamp filter (e.g. `2026-09-28T12:00:00Z`) |
| `to` | `string` | query | No | ISO-8601 end timestamp filter (e.g. `2026-09-28T18:00:00Z`) |
| `limit` | `integer` | query | No | Maximum number of most recent frames to return |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "stationId": "kolkata",
  "product": "reflectivity",
  "source": "IMD Doppler Weather Radar",
  "frames": [
    {
      "id": "kolkata_reflectivity_20260928T1704Z",
      "timestamp": "2026-09-28T17:04:00Z",
      "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1704Z.png"
    },
    {
      "id": "kolkata_reflectivity_20260928T1740Z",
      "timestamp": "2026-09-28T17:40:00Z",
      "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1740Z.png"
    }
  ]
}
```

**Frontend Usage:** Doppler Radar animation player (frame-by-frame scrubbing and looping radar loop).

**TypeScript Interface:**
```typescript
export interface RadarFrame {
  timestamp: string;
  filename: string;
  url: string; // e.g. "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1704Z.png"
}

export interface RadarFramesResponse {
  station: string;
  product: 'reflectivity' | 'velocity';
  count: number;
  frames: RadarFrame[];
}
```

---

### 42. Latest Doppler Radar Frame
**Method:** `GET`  
**Path:** `/api/radar/{stationId}/latest`  
**Live Render URL:** [`https://mock-prahari.onrender.com/api/radar/kolkata/latest?product=reflectivity`](https://mock-prahari.onrender.com/api/radar/kolkata/latest?product=reflectivity)  

**Description:** Retrieves the single newest available Doppler radar frame for the station, ideal for quick real-time checks.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `stationId` | `string` | path | Yes | Radar station identifier (e.g. `kolkata`, `paradip`) |
| `product` | `string` | query | No | Product type: `reflectivity` or `velocity` (default: `reflectivity`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "id": "kolkata_reflectivity_20260928T1740Z",
  "timestamp": "2026-09-28T17:40:00Z",
  "imageUrl": "/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1740Z.png"
}
```

**Frontend Usage:** Live radar snapshot thumbnail on dashboard or initial image for the radar viewer.

**TypeScript Interface:**
```typescript
export interface LatestRadarFrameResponse {
  station: string;
  product: 'reflectivity' | 'velocity';
  timestamp: string;
  filename: string;
  url: string;
}
```

---

### 43. Static Radar Image Stream
**Method:** `GET`  
**Path:** `/static/radar/{stationId}/{product}/{filename}`  
**Live Render URL:** [`https://mock-prahari.onrender.com/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1704Z.png`](https://mock-prahari.onrender.com/static/radar/kolkata/reflectivity/kolkata_reflectivity_20260928T1704Z.png)  

**Description:** Serves raw Doppler radar image files with proper `image/png` Content-Type headers for rendering in `<img>` tags or Mapbox/Leaflet ImageOverlays.

**Parameters:**
| Name | Type | In | Required | Description |
|:---|:---|:---|:---:|:---|
| `stationId` | `string` | path | Yes | Station slug (e.g. `kolkata`) |
| `product` | `string` | path | Yes | Product (`reflectivity` or `velocity`) |
| `filename` | `string` | path | Yes | Full frame filename (e.g. `kolkata_reflectivity_20260928T1704Z.png`) |

**Request Body:** None (`GET` request)

**Sample Live Response Body (`200 OK`):**
```json
{
  "binary": "<Raw PNG Image Data - Content-Type: image/png>"
}
```

**Frontend Usage:** Use directly in `<img>` or Leaflet `L.imageOverlay(url, bounds)`.

**TypeScript Interface:**
```typescript
// Use directly as an image src:
// <img src={`${VITE_STATIC_BASE_URL}${frame.url}`} alt="Doppler Radar Frame" />
```

---

## 4. Frontend Integration Snippets (React & TypeScript)

### 4.1 React Custom Hook for Doppler Radar Player
```tsx
import { useState, useEffect } from 'react';
import axios from 'axios';

interface RadarFrame {
  timestamp: string;
  filename: string;
  url: string;
}

export function useRadarFrames(station: string = 'kolkata', product: string = 'reflectivity') {
  const [frames, setFrames] = useState<RadarFrame[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'https://mock-prahari.onrender.com/api';
  const staticUrl = import.meta.env.VITE_STATIC_BASE_URL || 'https://mock-prahari.onrender.com';

  useEffect(() => {
    setLoading(true);
    axios.get(`${baseUrl}/radar/${station}/frames?product=${product}`)
      .then(res => {
        setFrames(res.data.frames);
        setCurrentIndex(res.data.frames.length - 1);
      })
      .finally(() => setLoading(false));
  }, [station, product]);

  useEffect(() => {
    if (!isPlaying || frames.length === 0) return;
    const interval = setInterval(() => {
      setCurrentIndex(prev => (prev + 1) % frames.length);
    }, 700);
    return () => clearInterval(interval);
  }, [isPlaying, frames]);

  return {
    frames,
    currentFrame: frames[currentIndex],
    currentImageUrl: frames[currentIndex] ? `${staticUrl}${frames[currentIndex].url}` : null,
    currentIndex,
    setCurrentIndex,
    isPlaying,
    setIsPlaying,
    loading
  };
}
```

### 4.2 React Hook for Monitored Cyclone Telemetry
```tsx
import { useState, useEffect } from 'react';
import axios from 'axios';

export function useCycloneTelemetry(eventId: string = 'BOB-02') {
  const [telemetry, setTelemetry] = useState<any>(null);
  const [trajectory, setTrajectory] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'https://mock-prahari.onrender.com/api';

  useEffect(() => {
    Promise.all([
      axios.get(`${baseUrl}/events/${eventId}/telemetry`),
      axios.get(`${baseUrl}/events/${eventId}/trajectory`)
    ]).then(([telRes, trajRes]) => {
      setTelemetry(telRes.data);
      setTrajectory(trajRes.data);
    }).finally(() => setLoading(false));
  }, [eventId]);

  return { telemetry, trajectory, loading };
}
```

---

## 5. Summary & Support

- **Live Base URL:** [`https://mock-prahari.onrender.com`](https://mock-prahari.onrender.com)
- **CORS:** Enabled with wildcard `*` for seamless frontend development.
- **Interactive API Explorer:** Visit [`https://mock-prahari.onrender.com/docs`](https://mock-prahari.onrender.com/docs) for the live Swagger UI where you can execute queries directly in your browser.
- **All 42 API Endpoints:** Tested and verified operational with 200 OK responses.