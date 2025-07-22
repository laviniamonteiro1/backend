import uuid
import pytest
import datetime
from unittest.mock import AsyncMock, patch

from blog.domain.entities.reservation import Reservation
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from blog.infra.repositories.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)
from blog.infra.repositories.in_memory.in_memory_reservation_repository import (
    InMemoryReservationRepository,
)

from blog.usecases.reservation.create_reservation import CreateReservation
from blog.usecases.reservation.get_user_reservation_by_id import GetUserReservationById
from blog.usecases.reservation.cancel_reservation import CancelReservation
from blog.usecases.reservation.update_reservation import UpdateReservation
from blog.usecases.reservation.delete_reservation import DeleteReservation
from blog.usecases.reservation.list_reservation import ListReservation


async def register_and_login_test_user(
    client, email: str, password: str, name: str = "Test User", role: str = "user"
):
    register_response = await client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role,
            "phone": "11999998888",
            "document": "12345678901",
            "address": "Rua do Teste, 100",
        },
    )
    if (
        register_response.status_code == 400
        and "User with this email already exists"
        in register_response.json().get("detail", "")
    ):
        pass
    else:
        assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"], login_response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_and_get_reservation(client):
    user_token, _ = await register_and_login_test_user(
        client, "res_test_user@example.com", "ResTest@123!"
    )

    check_in_dt = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt = datetime.datetime.now() + datetime.timedelta(days=15)
    reservation_data = {
        "title": "Viagem de Teste",
        "address": "Rua Teste, 123",
        "check_in": check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
        "check_out": check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
        "status": "confirmed",
        "bedroom_id": str(uuid.uuid4()),
    }

    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json=reservation_data,
    )
    assert 200 <= create_response.status_code < 300

    create_data = create_response.json()
    assert create_data["message"] == "Reservation created successfully"
    assert create_data["reservation"]["title"] == "Viagem de Teste"
    reservation_id = create_data["reservation"]["id"]

    get_response = await client.get(
        f"/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["id"] == reservation_id
    assert get_data["status"] == "Pendente"
    assert get_data["check_in"] == reservation_data["check_in"]


@pytest.mark.asyncio
async def test_create_reservation_invalid_data_format(client):
    user_token, _ = await register_and_login_test_user(
        client, "create_inv_user@example.com", "InvUser@123!"
    )

    invalid_reservation_data = {
        "title": "Reserva com data inválida",
        "address": "Rua Invalida, 1",
        "check_in": "DATA_INVALIDA",
        "check_out": "DATA_INVALIDA",
        "status": "confirmed",
    }
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json=invalid_reservation_data,
    )
    assert create_response.status_code == 422
    data = create_response.json()
    assert "detail" in data
    assert "errors" in data

    assert any(
        "String should match pattern" in error.get("message", "")
        for error in data["errors"]
    )


@pytest.mark.asyncio
async def test_create_reservation_internal_server_error(client, mocker):
    user_token, _ = await register_and_login_test_user(
        client, "err_user_create@example.com", "ErrUser@123!"
    )

    mocker.patch(
        "blog.usecases.reservation.create_reservation.CreateReservation.execute",
        side_effect=Exception("Internal server error during creation"),
    )

    check_in_dt = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt = datetime.datetime.now() + datetime.timedelta(days=15)
    reservation_data = {
        "title": "Viagem de Erro Interno",
        "address": "Rua Erro Interno, 500",
        "check_in": check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
        "check_out": check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
        "status": "confirmed",
        "bedroom_id": str(uuid.uuid4()),
    }
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json=reservation_data,
    )
    assert create_response.status_code == 500
    assert "detail" in create_response.json()
    assert "Internal server error during creation" in create_response.json()["detail"]


@pytest.mark.asyncio
async def test_get_reservation_not_found(client):
    user_token, _ = await register_and_login_test_user(
        client, "get_not_found_user@example.com", "NotFound@123!"
    )

    non_existent_id = str(uuid.uuid4())
    get_response = await client.get(
        f"/reservations/{non_existent_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Reservation not found"


@pytest.mark.asyncio
async def test_get_reservation_unauthorized_user(client):
    user1_token, user1_id = await register_and_login_test_user(
        client, "user1_get@example.com", "User1Get@123!"
    )
    check_in_dt1 = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt1 = datetime.datetime.now() + datetime.timedelta(days=15)
    create_response1 = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={
            "title": "Reserva User 1",
            "address": "End User 1",
            "check_in": check_in_dt1.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": check_out_dt1.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response1.status_code == 201
    reservation_id1 = create_response1.json()["reservation"]["id"]

    user2_token, _ = await register_and_login_test_user(
        client, "user2_get@example.com", "User2Get@123!"
    )
    get_response_unauth = await client.get(
        f"/reservations/{reservation_id1}",
        headers={"Authorization": f"Bearer {user2_token}"},
    )
    assert get_response_unauth.status_code == 403
    assert (
        get_response_unauth.json()["detail"]
        == "Not authorized to view this reservation"
    )


@pytest.mark.asyncio
async def test_delete_reservation_not_found(client):
    user_token, _ = await register_and_login_test_user(
        client, "delete_not_found_user@example.com", "DeleteNF@123!"
    )

    non_existent_id = str(uuid.uuid4())
    delete_response = await client.delete(
        f"/reservations/{non_existent_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert delete_response.status_code == 404
    assert delete_response.json()["detail"] == "Reservation not found"


@pytest.mark.asyncio
async def test_get_reservations_by_user_id_no_reservations(client):
    user_token, _ = await register_and_login_test_user(
        client, "no_res_user@example.com", "NoRes@123!"
    )

    list_response = await client.get(
        "/reservations/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert list_response.status_code == 200
    assert list_response.json()["reservations"] == []


@pytest.mark.asyncio
async def test_get_reservations_by_user_id_with_reservations(client):
    user_token, _ = await register_and_login_test_user(
        client, "has_res_user@example.com", "HasRes@123!"
    )

    for i in range(2):
        check_in_dt = datetime.datetime.now() + datetime.timedelta(days=20 + i)
        check_out_dt = datetime.datetime.now() + datetime.timedelta(days=25 + i)
        create_response = await client.post(
            "/reservations/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "title": f"Reserva {i+1}",
                "address": f"Rua {i+1}",
                "check_in": check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
                "check_out": check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
                "status": "Pendente",
                "bedroom_id": str(uuid.uuid4()),
            },
        )
        assert create_response.status_code == 201

    list_response = await client.get(
        "/reservations/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert list_response.status_code == 200
    assert len(list_response.json()["reservations"]) == 2
    assert list_response.json()["reservations"][0]["title"] == "Reserva 1"


@pytest.mark.asyncio
async def test_update_reservation(client):
    user_token, _ = await register_and_login_test_user(
        client, "update_user@example.com", "Update@123!"
    )

    initial_check_in_dt = datetime.datetime.now() + datetime.timedelta(days=10)
    initial_check_out_dt = datetime.datetime.now() + datetime.timedelta(days=15)
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "Reserva para Atualizar",
            "address": "Av. Teste, 456",
            "check_in": initial_check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": initial_check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
            "status": "confirmed",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response.status_code == 201

    reservation_id = create_response.json()["reservation"]["id"]

    new_check_in_dt = datetime.datetime.now() + datetime.timedelta(days=12)
    update_data = {
        "title": "Título Atualizado",
        "address": "Endereço Atualizado",
        "check_in": new_check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
        "status": "confirmed",
    }

    update_response = await client.put(
        f"/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data,
    )
    assert update_response.status_code == 200

    updated_data = update_response.json()["reservation"]
    assert updated_data["id"] == reservation_id
    assert updated_data["title"] == update_data["title"]
    assert updated_data["address"] == update_data["address"]
    assert updated_data["status"] == update_data["status"]
    assert updated_data["check_in"] == update_data["check_in"]


@pytest.mark.asyncio
async def test_update_reservation_internal_server_error(client, mocker):
    user_token, _ = await register_and_login_test_user(
        client, "err_upd_user@example.com", "ErrUpd@123!"
    )

    check_in_dt = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt = datetime.datetime.now() + datetime.timedelta(days=15)
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "Reserva para erro interno",
            "address": "Rua erro internal",
            "check_in": check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response.status_code == 201
    reservation_id = create_response.json()["reservation"]["id"]

    mocker.patch(
        "blog.usecases.reservation.update_reservation.UpdateReservation.execute",
        side_effect=Exception("Database error during update"),
    )

    update_response = await client.put(
        f"/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"status": "confirmed"},
    )
    assert update_response.status_code == 500
    assert "detail" in update_response.json()
    assert "Database error during update" in update_response.json()["detail"]


@pytest.mark.asyncio
async def test_cancel_reservation(client):
    user_token, _ = await register_and_login_test_user(
        client, "cancel_user@example.com", "Cancel@123!"
    )

    initial_check_in_dt = datetime.datetime.now() + datetime.timedelta(days=5)
    initial_check_out_dt = datetime.datetime.now() + datetime.timedelta(days=10)
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "Reserva para Cancelar",
            "address": "Rua do Cancelamento, 1",
            "check_in": initial_check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": initial_check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response.status_code == 201

    reservation_id = create_response.json()["reservation"]["id"]

    cancel_response = await client.post(
        f"/reservations/{reservation_id}/cancel",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert cancel_response.status_code == 200

    canceled_data = cancel_response.json()["reservation"]
    assert canceled_data["id"] == reservation_id
    assert canceled_data["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancel_reservation_unauthorized_user(client):
    user1_token, _ = await register_and_login_test_user(
        client, "user1_cancel@example.com", "User1Cancel@123!"
    )
    check_in_dt1 = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt1 = datetime.datetime.now() + datetime.timedelta(days=15)
    create_response1 = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={
            "title": "Reserva User 1 Cancel",
            "address": "End User 1 Cancel",
            "check_in": check_in_dt1.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": check_out_dt1.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response1.status_code == 201
    reservation_id1 = create_response1.json()["reservation"]["id"]

    user2_token, _ = await register_and_login_test_user(
        client, "user2_cancel@example.com", "User2Cancel@123!"
    )
    cancel_response_unauth = await client.post(
        f"/reservations/{reservation_id1}/cancel",
        headers={"Authorization": f"Bearer {user2_token}"},
    )
    assert cancel_response_unauth.status_code == 403
    assert (
        cancel_response_unauth.json()["detail"]
        == "Not authorized to cancel this reservation"
    )


@pytest.mark.asyncio
async def test_cancel_reservation_internal_server_error(client, mocker):
    user_token, _ = await register_and_login_test_user(
        client, "err_cancel_user@example.com", "ErrCancel@123!"
    )

    check_in_dt = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt = datetime.datetime.now() + datetime.timedelta(days=15)
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "Reserva para erro interno cancel",
            "address": "Rua erro internal cancel",
            "check_in": check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response.status_code == 201
    reservation_id = create_response.json()["reservation"]["id"]

    mocker.patch(
        "blog.usecases.reservation.cancel_reservation.CancelReservation.execute",
        side_effect=Exception("Database error during cancel"),
    )

    cancel_response = await client.post(
        f"/reservations/{reservation_id}/cancel",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert cancel_response.status_code == 500
    assert "detail" in cancel_response.json()
    assert "Database error during cancel" in cancel_response.json()["detail"]


@pytest.mark.asyncio
async def test_list_all_reservations_admin_access(client):
    admin_token, admin_user_id = await register_and_login_test_user(
        client, "admin_res@example.com", "AdminRes@123!", role="admin"
    )

    check_in_dt_admin = datetime.datetime.now() + datetime.timedelta(days=1)
    check_out_dt_admin = datetime.datetime.now() + datetime.timedelta(days=2)
    admin_reservation_data = {
        "title": "Reserva Admin Teste",
        "address": "Endereço Admin, 1",
        "check_in": check_in_dt_admin.strftime("%d/%m/%Y às %Hh%M"),
        "check_out": check_out_dt_admin.strftime("%d/%m/%Y às %Hh%M"),
        "status": "confirmed",
        "bedroom_id": str(uuid.uuid4()),
    }
    create_admin_res_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=admin_reservation_data,
    )
    assert create_admin_res_response.status_code == 201

    list_response = await client.get(
        "/reservations/",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert list_response.status_code == 200
    list_data = list_response.json()
    assert "reservations" in list_data
    assert len(list_data["reservations"]) >= 1


@pytest.mark.asyncio
async def test_list_all_reservations_user_forbidden(client):
    user_token, _ = await register_and_login_test_user(
        client, "forbidden_user@example.com", "Forbidden@123!"
    )

    forbidden_response = await client.get(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert forbidden_response.status_code == 403
    assert (
        forbidden_response.json()["detail"] == "Only admins can list all reservations"
    )


@pytest.mark.asyncio
async def test_delete_reservation(client):
    user_token, _ = await register_and_login_test_user(
        client, "delete_user@example.com", "Delete@123!"
    )

    initial_check_in_dt = datetime.datetime.now() + datetime.timedelta(days=20)
    initial_check_out_dt = datetime.datetime.now() + datetime.timedelta(days=25)
    create_response = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "Reserva para Deletar",
            "address": "Rua da Exclusão, 789",
            "check_in": initial_check_in_dt.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": initial_check_out_dt.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response.status_code == 201

    reservation_id = create_response.json()["reservation"]["id"]

    delete_response = await client.delete(
        f"/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Reservation deleted successfully"

    get_after_delete_response = await client.get(
        f"/reservations/{reservation_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert get_after_delete_response.status_code == 404
    assert get_after_delete_response.json()["detail"] == "Reservation not found"


@pytest.mark.asyncio
async def test_delete_reservation_unauthorized_user(client):
    user1_token, _ = await register_and_login_test_user(
        client, "user1_del@example.com", "User1Del@123!"
    )
    check_in_dt1 = datetime.datetime.now() + datetime.timedelta(days=10)
    check_out_dt1 = datetime.datetime.now() + datetime.timedelta(days=15)
    create_response1 = await client.post(
        "/reservations/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={
            "title": "Reserva User 1 Delete",
            "address": "End User 1 Delete",
            "check_in": check_in_dt1.strftime("%d/%m/%Y às %Hh%M"),
            "check_out": check_out_dt1.strftime("%d/%m/%Y às %Hh%M"),
            "status": "Pendente",
            "bedroom_id": str(uuid.uuid4()),
        },
    )
    assert create_response1.status_code == 201
    reservation_id1 = create_response1.json()["reservation"]["id"]

    user2_token, _ = await register_and_login_test_user(
        client, "user2_del@example.com", "User2Del@123!"
    )
    delete_response_unauth = await client.delete(
        f"/reservations/{reservation_id1}",
        headers={"Authorization": f"Bearer {user2_token}"},
    )
    assert delete_response_unauth.status_code == 403
    assert (
        delete_response_unauth.json()["detail"]
        == "Not authorized to delete this reservation"
    )
