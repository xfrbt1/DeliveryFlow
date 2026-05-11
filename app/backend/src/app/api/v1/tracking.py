from fastapi import APIRouter

from app.api.dependencies import UoWDep
from app.api.schemas.order import TrackingResponse
from app.application.use_cases.order.track_order import track_order

router = APIRouter(prefix="/track", tags=["tracking"])


@router.get("/{tracking_url}", response_model=TrackingResponse)
async def track_order_endpoint(tracking_url: str, uow: UoWDep) -> TrackingResponse:
    result = await track_order(uow, tracking_url=tracking_url)
    return TrackingResponse(
        status=result.status,
        courier_lat=result.courier_lat,
        courier_lon=result.courier_lon,
        location_updated_at=result.location_updated_at,
        updated_at=result.updated_at,
    )
