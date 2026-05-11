from uuid import UUID

from app.application.dto.order import OrderDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto
from app.domain.exceptions import OrderAccessDeniedError, OrderNotFoundError


async def get_order_for_courier(
    uow: UnitOfWork,
    *,
    courier_id: UUID,
    order_id: UUID,
) -> OrderDTO:
    async with uow:
        order = await uow.orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id=str(order_id))
        if order.courier_id != courier_id:
            raise OrderAccessDeniedError()
        return order_to_dto(order)
