from datetime import UTC, datetime
from uuid import UUID

from app.application.dto.order import OrderDTO, UpdateCourierLocationDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto
from app.domain.exceptions import (
    OrderAccessDeniedError,
    OrderConflictError,
    OrderNotFoundError,
)
from app.domain.value_objects.order_status import OrderStatus


_ACTIVE_DELIVERY_STATUSES = frozenset(
    {
        OrderStatus.ACCEPTED,
        OrderStatus.PICKED_UP,
        OrderStatus.IN_TRANSIT,
    },
)


async def update_courier_location(
    uow: UnitOfWork,
    *,
    courier_id: UUID,
    order_id: UUID,
    dto: UpdateCourierLocationDTO,
) -> OrderDTO:
    async with uow:
        order = await uow.orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id=str(order_id))
        if order.courier_id != courier_id:
            raise OrderAccessDeniedError()
        if order.status not in _ACTIVE_DELIVERY_STATUSES:
            raise OrderConflictError(
                "Location updates are allowed only for active deliveries",
            )
        now = datetime.now(UTC)
        order.courier_lat = dto.lat
        order.courier_lon = dto.lon
        order.location_updated_at = now
        order.updated_at = now
        await uow.orders.update(order)
        await uow.commit()
        return order_to_dto(order)
