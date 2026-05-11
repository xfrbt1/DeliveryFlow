"""Integration: orders, roles, tracking."""

from uuid import UUID

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_customer_courier_order_lifecycle_and_public_tracking(
    http_client: AsyncClient,
) -> None:
    cust_reg = await http_client.post(
        "/api/v1/auth/register",
        json={
            "email": "buyer@example.com",
            "password": "secretpass123",
            "full_name": "Buyer",
            "role": "customer",
        },
    )
    assert cust_reg.status_code == 201, cust_reg.text

    cour_reg = await http_client.post(
        "/api/v1/auth/register",
        json={
            "email": "rider@example.com",
            "password": "secretpass123",
            "full_name": "Rider",
            "role": "courier",
        },
    )
    assert cour_reg.status_code == 201, cour_reg.text

    cust_login = await http_client.post(
        "/api/v1/auth/login",
        json={"email": "buyer@example.com", "password": "secretpass123"},
    )
    assert cust_login.status_code == 200, cust_login.text
    cust_headers = {"Authorization": f"Bearer {cust_login.json()['access_token']}"}

    cour_login = await http_client.post(
        "/api/v1/auth/login",
        json={"email": "rider@example.com", "password": "secretpass123"},
    )
    assert cour_login.status_code == 200, cour_login.text
    cour_headers = {"Authorization": f"Bearer {cour_login.json()['access_token']}"}

    create = await http_client.post(
        "/api/v1/orders",
        headers=cust_headers,
        json={
            "pickup_address": "A street 1",
            "delivery_address": "B ave 2",
            "description": "Documents",
        },
    )
    assert create.status_code == 201, create.text
    order = create.json()
    order_id = order["id"]
    tracking_url = order["tracking_url"]
    assert order["status"] == "created"

    track = await http_client.get(f"/api/v1/track/{tracking_url}")
    assert track.status_code == 200, track.text
    track_body = track.json()
    assert track_body["status"] == "created"
    assert track_body["courier_lat"] is None

    avail = await http_client.get("/api/v1/orders", headers=cour_headers)
    assert avail.status_code == 200, avail.text
    ids = {UUID(o["id"]) for o in avail.json()}
    assert UUID(order_id) in ids

    accept = await http_client.post(
        f"/api/v1/orders/{order_id}/accept",
        headers=cour_headers,
    )
    assert accept.status_code == 200, accept.text
    assert accept.json()["status"] == "accepted"

    loc = await http_client.patch(
        f"/api/v1/orders/{order_id}/location",
        headers=cour_headers,
        json={"lat": 55.75, "lon": 37.62},
    )
    assert loc.status_code == 200, loc.text

    track2 = await http_client.get(f"/api/v1/track/{tracking_url}")
    assert track2.status_code == 200
    assert track2.json()["courier_lat"] == 55.75
    assert track2.json()["courier_lon"] == 37.62

    for status_val in ("picked_up", "in_transit", "delivered"):
        upd = await http_client.patch(
            f"/api/v1/orders/{order_id}/status",
            headers=cour_headers,
            json={"status": status_val},
        )
        assert upd.status_code == 200, upd.text
        assert upd.json()["status"] == status_val


@pytest.mark.asyncio
async def test_tracking_unknown_returns_404(http_client: AsyncClient) -> None:
    resp = await http_client.get("/api/v1/track/nonexistent-tracking-token-xxxxxxxx")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_courier_forbidden_on_customer_order_create(http_client: AsyncClient) -> None:
    reg = await http_client.post(
        "/api/v1/auth/register",
        json={
            "email": "onlycourier@example.com",
            "password": "secretpass123",
            "full_name": "Courier Only",
            "role": "courier",
        },
    )
    assert reg.status_code == 201, reg.text
    login = await http_client.post(
        "/api/v1/auth/login",
        json={"email": "onlycourier@example.com", "password": "secretpass123"},
    )
    assert login.status_code == 200, login.text
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    create = await http_client.post(
        "/api/v1/orders",
        headers=headers,
        json={
            "pickup_address": "X",
            "delivery_address": "Y",
            "description": "Z",
        },
    )
    assert create.status_code == 403, create.text


@pytest.mark.asyncio
async def test_courier_mine_list_get_detail_and_location(http_client: AsyncClient) -> None:
    await http_client.post(
        "/api/v1/auth/register",
        json={
            "email": "mine-cust@example.com",
            "password": "secretpass123",
            "full_name": "Mine Cust",
            "role": "customer",
        },
    )
    await http_client.post(
        "/api/v1/auth/register",
        json={
            "email": "mine-cour@example.com",
            "password": "secretpass123",
            "full_name": "Mine Cour",
            "role": "courier",
        },
    )
    cl = await http_client.post(
        "/api/v1/auth/login",
        json={"email": "mine-cust@example.com", "password": "secretpass123"},
    )
    cour_l = await http_client.post(
        "/api/v1/auth/login",
        json={"email": "mine-cour@example.com", "password": "secretpass123"},
    )
    cust_h = {"Authorization": f"Bearer {cl.json()['access_token']}"}
    cour_h = {"Authorization": f"Bearer {cour_l.json()['access_token']}"}

    empty_mine = await http_client.get(
        "/api/v1/orders",
        headers=cour_h,
        params={"courier_scope": "mine"},
    )
    assert empty_mine.status_code == 200
    assert empty_mine.json() == []

    created = await http_client.post(
        "/api/v1/orders",
        headers=cust_h,
        json={
            "pickup_address": "P",
            "delivery_address": "D",
            "description": "Box",
        },
    )
    assert created.status_code == 201
    order_id = created.json()["id"]

    mine_before = await http_client.get(
        "/api/v1/orders",
        headers=cour_h,
        params={"courier_scope": "mine"},
    )
    assert mine_before.json() == []

    acc = await http_client.post(
        f"/api/v1/orders/{order_id}/accept",
        headers=cour_h,
    )
    assert acc.status_code == 200

    mine_after = await http_client.get(
        "/api/v1/orders",
        headers=cour_h,
        params={"courier_scope": "mine"},
    )
    assert mine_after.status_code == 200
    body = mine_after.json()
    assert len(body) == 1
    assert body[0]["id"] == order_id
    assert body[0]["status"] == "accepted"

    detail = await http_client.get(
        f"/api/v1/orders/{order_id}",
        headers=cour_h,
    )
    assert detail.status_code == 200
    assert detail.json()["id"] == order_id

    loc = await http_client.patch(
        f"/api/v1/orders/{order_id}/location",
        headers=cour_h,
        json={"lat": 59.93, "lon": 30.33},
    )
    assert loc.status_code == 200
    assert loc.json()["courier_lat"] == 59.93
    assert loc.json()["courier_lon"] == 30.33
