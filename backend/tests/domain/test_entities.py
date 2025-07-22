import pytest
from blog.domain.entities.user import User
from blog.domain.entities.reservation import Reservation
from blog.domain.entities.bedroom import Bedroom
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from datetime import datetime


def test_create_user():
    email = Email("user@example.com")
    pwd = Password("Secret@123")
    user = User(
        "1", "User", email, pwd, "user", phone=None, document=None, address=None
    )
    assert user.name == "User"
    assert user.phone is None


def test_invalid_role():
    with pytest.raises(ValueError):
        User(
            "1",
            "User",
            Email("user@example.com"),
            Password("Secret@123"),
            "invalid",
            phone=None,
            document=None,
            address=None,
        )


def test_create_reservation():
    check_in_str = "25/12/2024 às 14h00"
    check_out_str = "30/12/2024 às 11h00"
    reservation = Reservation(
        "res1",
        "user1",
        "Viagem de Férias",
        "Rua A, 123",
        check_in_str,
        check_out_str,
        "Pendente",
    )
    assert reservation.title == "Viagem de Férias"
    assert isinstance(reservation.check_in, datetime)
    assert reservation.status == "Pendente"


def test_cancel_reservation():
    check_in_str = "25/12/2024 às 14h00"
    check_out_str = "30/12/2024 às 11h00"
    reservation = Reservation(
        "res1",
        "user1",
        "Viagem de Férias",
        "Rua A, 123",
        check_in_str,
        check_out_str,
        "Pendente",
    )
    reservation.cancel_reservation()
    assert reservation.status == "cancelled"


def test_update_reservation():
    check_in_str = "25/12/2024 às 14h00"
    check_out_str = "30/12/2024 às 11h00"
    reservation = Reservation(
        "res1",
        "user1",
        "Viagem de Férias",
        "Rua A, 123",
        check_in_str,
        check_out_str,
        "Pendente",
    )

    new_title = "Viagem Atualizada"
    new_address = "Av. B, 456"
    new_check_in_str_updated = "26/12/2024 às 15h00"
    new_check_out_str_updated = "31/12/2024 às 12h00"
    new_status = "confirmed"

    reservation.update_reservation(
        new_title=new_title,
        new_address=new_address,
        new_check_in_str=new_check_in_str_updated,
        new_check_out_str=new_check_out_str_updated,
        new_status=new_status,
    )

    assert reservation.title == new_title
    assert reservation.address == new_address
    assert reservation.check_in == datetime.strptime(
        new_check_in_str_updated, "%d/%m/%Y às %Hh%M"
    )
    assert reservation.check_out == datetime.strptime(
        new_check_out_str_updated, "%d/%m/%Y às %Hh%M"
    )
    assert reservation.status == new_status


def test_create_bedroom():
    bedroom = Bedroom(
        "bed1",
        "Quarto Deluxe",
        "Quarto espaçoso com vista para o mar",
        "R$ 300.00",
        "deluxe_img.jpg",
    )
    assert bedroom.title == "Quarto Deluxe"
    assert bedroom.price == "R$ 300.00"
