from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateOrderRequest(BaseModel):
    pickup_address: str = Field(min_length=1, max_length=500)
    delivery_address: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1, max_length=5000)


class UpdateOrderStatusRequest(BaseModel):
    status: str = Field(min_length=1, max_length=32)


class UpdateCourierLocationRequest(BaseModel):
    lat: float = Field(ge=-90.0, le=90.0)
    lon: float = Field(ge=-180.0, le=180.0)


class OrderResponse(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)


class TrackingResponse(BaseModel):
    status: str
    courier_lat: float | None
    courier_lon: float | None
    location_updated_at: datetime | None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
