from app.application.dto.order import TrackingDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_tracking_dto
from app.domain.exceptions import OrderNotFoundError


async def track_order(uow: UnitOfWork, *, tracking_url: str) -> TrackingDTO:
    key = tracking_url.strip()
    async with uow:
        order = await uow.orders.get_by_tracking_url(key)
        if order is None:
            raise OrderNotFoundError(tracking_url=key)
        return order_to_tracking_dto(order)
