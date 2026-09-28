from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.radar_scanner import get_stations, scan_radar_frames

router = APIRouter(prefix="/api/radar", tags=["Doppler Radar"])


def _find_station(station_id: str):
    stations = get_stations()
    norm_id = station_id.strip().lower()
    for s in stations:
        if s["id"].lower() == norm_id:
            return s
    raise HTTPException(status_code=404, detail=f"Station '{station_id}' not found")


def _validate_product(station: dict, product: str):
    allowed_products = [p.lower() for p in station.get("products", [])]
    if product.lower() not in allowed_products:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product}' not supported for station '{station['id']}'",
        )


@router.get("/stations")
async def list_stations():
    return get_stations()


@router.get("/{stationId}/frames")
async def get_frames(
    stationId: str,
    product: str = "reflectivity",
    from_time: Optional[str] = Query(None, alias="from"),
    to_time: Optional[str] = Query(None, alias="to"),
    limit: Optional[int] = Query(None),
):
    station = _find_station(stationId)
    _validate_product(station, product)

    frames = scan_radar_frames(
        station_id=station["id"],
        product=product.lower(),
        from_time=from_time,
        to_time=to_time,
        limit=limit,
    )

    return {
        "stationId": station["id"],
        "product": product.lower(),
        "source": "IMD Doppler Weather Radar",
        "frames": frames,
    }


@router.get("/{stationId}/latest")
async def get_latest_frame(
    stationId: str,
    product: str = "reflectivity",
):
    station = _find_station(stationId)
    _validate_product(station, product)

    frames = scan_radar_frames(
        station_id=station["id"],
        product=product.lower(),
    )

    if not frames:
        raise HTTPException(
            status_code=404,
            detail=f"No radar frames found for station '{stationId}' and product '{product}'",
        )

    return frames[-1]
