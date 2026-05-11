from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.dto.order import CreateOrderDTO, OrderDTO
from app.application.interfaces.unit_of_work import UnitOfWork
from app.application.mappers.order import order_to_dto
from app.domain.entities.order import Order
from app.domain.value_objects.order_status import OrderStatus


async def create_order(
    uow: UnitOfWork,
    *,
    customer_id: UUID,
    dto: CreateOrderDTO,
) -> OrderDTO:
    now = datetime.now(UTC)
    async with uow:
        order = Order(
            id=uuid4(),
            customer_id=customer_id,
            courier_id=None,
            description=dto.description.strip(),
            pickup_address=dto.pickup_address.strip(),
            delivery_address=dto.delivery_address.strip(),
            status=OrderStatus.CREATED,
            tracking_url=uuid4().hex,
            courier_lat=None,
            courier_lon=None,
            location_updated_at=None,
            created_at=now,
            updated_at=now,
        )
        await uow.orders.add(order)
        await uow.commit()
        return order_to_dto(order)
