from datetime import UTC, datetime
from uuid import UUID

from app.application.dto.order import OrderDTO, UpdateOrderStatusDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto
from app.domain.exceptions import (
    InvalidStatusTransitionError,
    OrderAccessDeniedError,
    OrderNotFoundError,
)
from app.domain.value_objects.order_status import ALLOWED_TRANSITIONS, OrderStatus


async def update_order_status(
    uow: UnitOfWork,
    *,
    courier_id: UUID,
    order_id: UUID,
    dto: UpdateOrderStatusDTO,
) -> OrderDTO:
    new_status = OrderStatus(dto.status.strip().lower())
    async with uow:
        order = await uow.orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id=str(order_id))
        if order.courier_id != courier_id:
            raise OrderAccessDeniedError()
        allowed = ALLOWED_TRANSITIONS.get(order.status, set())
        if new_status not in allowed:
            msg = (
                f"Invalid transition from {order.status.value} to {new_status.value}"
            )
            raise InvalidStatusTransitionError(msg)
        order.status = new_status
        order.updated_at = datetime.now(UTC)
        await uow.orders.update(order)
        await uow.commit()
        return order_to_dto(order)
