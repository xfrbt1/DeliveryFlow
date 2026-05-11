from datetime import UTC, datetime
from uuid import UUID

from app.application.dto.order import OrderDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto
from app.domain.exceptions import (
    InvalidStatusTransitionError,
    OrderAccessDeniedError,
    OrderNotFoundError,
)
from app.domain.value_objects.order_status import ALLOWED_TRANSITIONS, OrderStatus


async def cancel_order(
    uow: UnitOfWork,
    *,
    customer_id: UUID,
    order_id: UUID,
) -> OrderDTO:
    async with uow:
        order = await uow.orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id=str(order_id))
        if order.customer_id != customer_id:
            raise OrderAccessDeniedError()
        target = OrderStatus.CANCELLED
        allowed = ALLOWED_TRANSITIONS.get(order.status, set())
        if target not in allowed:
            msg = f"Cannot cancel order in status {order.status.value}"
            raise InvalidStatusTransitionError(msg)
        order.status = target
        order.updated_at = datetime.now(UTC)
        await uow.orders.update(order)
        await uow.commit()
        return order_to_dto(order)
