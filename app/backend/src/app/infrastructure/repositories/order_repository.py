from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.order import Order
from app.domain.repositories.order_repository import OrderRepository
from app.domain.value_objects.order_status import OrderStatus
from app.infrastructure.db.models.order import OrderModel


def _to_domain(row: OrderModel) -> Order:
    return Order(
        id=row.id,
        customer_id=row.customer_id,
        courier_id=row.courier_id,
        description=row.description,
        pickup_address=row.pickup_address,
        delivery_address=row.delivery_address,
        status=OrderStatus(row.status),
        tracking_url=row.tracking_url,
        courier_lat=row.courier_lat,
        courier_lon=row.courier_lon,
        location_updated_at=row.location_updated_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _to_model(entity: Order) -> OrderModel:
    return OrderModel(
        id=entity.id,
        customer_id=entity.customer_id,
        courier_id=entity.courier_id,
        description=entity.description,
        pickup_address=entity.pickup_address,
        delivery_address=entity.delivery_address,
        status=entity.status.value,
        tracking_url=entity.tracking_url,
        courier_lat=entity.courier_lat,
        courier_lon=entity.courier_lon,
        location_updated_at=entity.location_updated_at,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, order: Order) -> None:
        self._session.add(_to_model(order))

    async def get_by_id(self, order_id: UUID) -> Order | None:
        row = await self._session.get(OrderModel, order_id)
        return _to_domain(row) if row is not None else None

    async def get_by_tracking_url(self, tracking_url: str) -> Order | None:
        stmt = select(OrderModel).where(OrderModel.tracking_url == tracking_url).limit(1)
        res = await self._session.execute(stmt)
        row = res.scalar_one_or_none()
        return _to_domain(row) if row is not None else None

    async def list_by_customer(
        self,
        customer_id: UUID,
        *,
        limit: int,
        offset: int,
    ) -> list[Order]:
        stmt = (
            select(OrderModel)
            .where(OrderModel.customer_id == customer_id)
            .order_by(OrderModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        res = await self._session.execute(stmt)
        rows = res.scalars().all()
        return [_to_domain(r) for r in rows]

    async def list_available(self, *, limit: int, offset: int) -> list[Order]:
        stmt = (
            select(OrderModel)
            .where(OrderModel.status == OrderStatus.CREATED.value)
            .order_by(OrderModel.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        res = await self._session.execute(stmt)
        rows = res.scalars().all()
        return [_to_domain(r) for r in rows]

    async def list_by_courier(
        self,
        courier_id: UUID,
        *,
        limit: int,
        offset: int,
    ) -> list[Order]:
        stmt = (
            select(OrderModel)
            .where(OrderModel.courier_id == courier_id)
            .order_by(OrderModel.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        res = await self._session.execute(stmt)
        rows = res.scalars().all()
        return [_to_domain(r) for r in rows]

    async def accept(self, order_id: UUID, courier_id: UUID) -> Order | None:
        stmt = select(OrderModel).where(OrderModel.id == order_id).with_for_update()
        res = await self._session.execute(stmt)
        row = res.scalar_one_or_none()
        if row is None:
            return None
        if row.status != OrderStatus.CREATED.value or row.courier_id is not None:
            return None
        row.courier_id = courier_id
        row.status = OrderStatus.ACCEPTED.value
        await self._session.flush()
        await self._session.refresh(row)
        return _to_domain(row)

    async def update(self, order: Order) -> None:
        existing = await self._session.get(OrderModel, order.id)
        if existing is None:
            return
        existing.customer_id = order.customer_id
        existing.courier_id = order.courier_id
        existing.description = order.description
        existing.pickup_address = order.pickup_address
        existing.delivery_address = order.delivery_address
        existing.status = order.status.value
        existing.tracking_url = order.tracking_url
        existing.courier_lat = order.courier_lat
        existing.courier_lon = order.courier_lon
        existing.location_updated_at = order.location_updated_at
        existing.updated_at = order.updated_at
