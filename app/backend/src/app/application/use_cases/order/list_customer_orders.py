from uuid import UUID

from app.application.dto.order import OrderDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto


async def list_customer_orders(
    uow: UnitOfWork,
    *,
    customer_id: UUID,
    limit: int,
    offset: int,
) -> list[OrderDTO]:
    async with uow:
        orders = await uow.orders.list_by_customer(customer_id, limit=limit, offset=offset)
        return [order_to_dto(o) for o in orders]
