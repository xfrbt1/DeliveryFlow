from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CreateOrderDTO:
    pickup_address: str
    delivery_address: str
    description: str


@dataclass(frozen=True, slots=True)
class UpdateOrderStatusDTO:
    status: str


@dataclass(frozen=True, slots=True)
class UpdateCourierLocationDTO:
    lat: float
    lon: float


@dataclass(frozen=True, slots=True)
class OrderDTO:
    id: UUID
    customer_id: UUID
    courier_id: UUID | None
    description: str
    pickup_address: str
    delivery_address: str
    status: str
    tracking_url: str
    courier_lat: float | None
    courier_lon: float | None
    location_updated_at: datetime | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class TrackingDTO:
    status: str
    courier_lat: float | None
    courier_lon: float | None
    location_updated_at: datetime | None
    updated_at: datetime
