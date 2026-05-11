"""Unit tests: order status graph (matches courier/customer lifecycle in integration flow)."""

import pytest

from app.domain.value_objects.order_status import ALLOWED_TRANSITIONS, OrderStatus


def _allowed_targets(status: OrderStatus) -> set[OrderStatus]:
    return ALLOWED_TRANSITIONS.get(status, set())


def test_status_values_match_api_contract() -> None:
    """Strings match HTTP/API payloads used in orders and tracking."""
    assert OrderStatus.CREATED.value == "created"
    assert OrderStatus.ACCEPTED.value == "accepted"
    assert OrderStatus.PICKED_UP.value == "picked_up"
    assert OrderStatus.IN_TRANSIT.value == "in_transit"
    assert OrderStatus.DELIVERED.value == "delivered"
    assert OrderStatus.CANCELLED.value == "cancelled"


def test_status_constructible_from_lowercase_api_strings() -> None:
    assert OrderStatus("created") is OrderStatus.CREATED
    assert OrderStatus("picked_up") is OrderStatus.PICKED_UP
    assert OrderStatus("in_transit") is OrderStatus.IN_TRANSIT


def test_courier_happy_path_chain_allowed() -> None:
    """Same progression as integration: accepted → picked_up → in_transit → delivered."""
    assert OrderStatus.ACCEPTED in _allowed_targets(OrderStatus.CREATED)
    assert OrderStatus.PICKED_UP in _allowed_targets(OrderStatus.ACCEPTED)
    assert OrderStatus.IN_TRANSIT in _allowed_targets(OrderStatus.PICKED_UP)
    assert OrderStatus.DELIVERED in _allowed_targets(OrderStatus.IN_TRANSIT)


def test_customer_can_cancel_only_before_pickup() -> None:
    """Cancel from created/accepted; not after picked_up (matches cancel_order guard)."""
    assert OrderStatus.CANCELLED in _allowed_targets(OrderStatus.CREATED)
    assert OrderStatus.CANCELLED in _allowed_targets(OrderStatus.ACCEPTED)
    assert OrderStatus.CANCELLED not in _allowed_targets(OrderStatus.PICKED_UP)
    assert OrderStatus.CANCELLED not in _allowed_targets(OrderStatus.IN_TRANSIT)


@pytest.mark.parametrize(
    ("current", "invalid_next"),
    [
        (OrderStatus.CREATED, OrderStatus.PICKED_UP),
        (OrderStatus.CREATED, OrderStatus.IN_TRANSIT),
        (OrderStatus.CREATED, OrderStatus.DELIVERED),
        (OrderStatus.ACCEPTED, OrderStatus.IN_TRANSIT),
        (OrderStatus.ACCEPTED, OrderStatus.DELIVERED),
        (OrderStatus.PICKED_UP, OrderStatus.DELIVERED),
        (OrderStatus.PICKED_UP, OrderStatus.CANCELLED),
        (OrderStatus.IN_TRANSIT, OrderStatus.CANCELLED),
        (OrderStatus.IN_TRANSIT, OrderStatus.PICKED_UP),
    ],
)
def test_invalid_transitions_not_in_allowed_map(
    current: OrderStatus,
    invalid_next: OrderStatus,
) -> None:
    assert invalid_next not in _allowed_targets(current)


def test_terminal_statuses_block_further_transitions() -> None:
    """Delivered/cancelled are not keys → update_order_status sees empty allowed set."""
    assert OrderStatus.DELIVERED not in ALLOWED_TRANSITIONS
    assert OrderStatus.CANCELLED not in ALLOWED_TRANSITIONS
    assert _allowed_targets(OrderStatus.DELIVERED) == set()
    assert _allowed_targets(OrderStatus.CANCELLED) == set()
