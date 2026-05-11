from app.application.dto.order import OrderDTO, TrackingDTO
from app.domain.entities.order import Order


def order_to_dto(entity: Order) -> OrderDTO:
    return OrderDTO(
        id=entity.id,
        customer_id=entity.customer_id,
        courier_id=entity.courier_id,
        description=entity.description,
        pickup_address=entity.pickup_address,
        delivery_address=entity.delivery_address,
        status=entity.status.value,
        tracking_url=entity.tracking_url,
        courier_lat=entity.courier_lat,
        courier_lon=entity.courier_lon,
        location_updated_at=entity.location_updated_at,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def order_to_tracking_dto(entity: Order) -> TrackingDTO:
    return TrackingDTO(
        status=entity.status.value,
        courier_lat=entity.courier_lat,
        courier_lon=entity.courier_lon,
        location_updated_at=entity.location_updated_at,
        updated_at=entity.updated_at,
    )
