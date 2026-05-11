from uuid import UUID

from app.application.dto.order import OrderDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto
from app.domain.exceptions import OrderConflictError, OrderNotFoundError


async def accept_order(
    uow: UnitOfWork,
    *,
    courier_id: UUID,
    order_id: UUID,
) -> OrderDTO:
    async with uow:
        updated = await uow.orders.accept(order_id, courier_id)
        if updated is None:
            existing = await uow.orders.get_by_id(order_id)
            if existing is None:
                raise OrderNotFoundError(order_id=str(order_id))
            raise OrderConflictError("Order is not available for acceptance")
        await uow.commit()
        return order_to_dto(updated)
