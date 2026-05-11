from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.value_objects.order_status import OrderStatus


@dataclass(slots=True)
class Order:
    id: UUID
    customer_id: UUID
    courier_id: UUID | None
    description: str
    pickup_address: str
    delivery_address: str
    status: OrderStatus
    tracking_url: str
    courier_lat: float | None
    courier_lon: float | None
    location_updated_at: datetime | None
    created_at: datetime
    updated_at: datetime
