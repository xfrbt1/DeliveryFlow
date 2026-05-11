from typing import Protocol
from uuid import UUID

from app.domain.entities.order import Order


class OrderRepository(Protocol):
    async def add(self, order: Order) -> None:
        """Persist new order."""

    async def get_by_id(self, order_id: UUID) -> Order | None:
        """Return order by id or None."""

    async def get_by_tracking_url(self, tracking_url: str) -> Order | None:
        """Return order by tracking token or None."""

    async def list_by_customer(
        self,
        customer_id: UUID,
        *,
        limit: int,
        offset: int,
    ) -> list[Order]:
        """Paginated orders for customer."""

    async def list_available(self, *, limit: int, offset: int) -> list[Order]:
        """Orders waiting for courier."""

    async def list_by_courier(
        self,
        courier_id: UUID,
        *,
        limit: int,
        offset: int,
    ) -> list[Order]:
        """Orders assigned to this courier."""

    async def accept(self, order_id: UUID, courier_id: UUID) -> Order | None:
        """Lock row and assign courier if still CREATED."""

    async def update(self, order: Order) -> None:
        """Persist changes to existing order."""
