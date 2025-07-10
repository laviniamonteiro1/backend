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
    user = User("1", "User", email, pwd, "user")
    assert user.name == "User"


def test_invalid_role():
    with pytest.raises(ValueError):
        User("1", "User", Email("user@example.com"), Password("Secret@123"), "invalid")


def test_create_reservation():
    check_in_str = "25/12/2024 às 14h00"
    check_out_str = "30/12/2024 às 11h00"
    reservation = Reservation("res1", "user1", "Viagem de Férias", "Rua A, 123", check_in_str, check_out_str, "Pendente")
    assert reservation.title == "Viagem de Férias"
    assert isinstance(reservation.check_in, datetime)
    assert reservation.status == "Pendente"


def test_cancel_reservation():
    check_in_str = "25/12/2024 às 14h00"
    check_out_str = "30/12/2024 às 11h00"
    reservation = Reservation("res1", "user1", "Viagem de Férias", "Rua A, 123", check_in_str, check_out_str, "Pendente")
    reservation.cancel_reservation()
    assert reservation.status == "Cancelada"


def test_update_reservation():
    check_in_str = "25/12/2024 às 14h00"
    check_out_str = "30/12/2024 às 11h00"
    reservation = Reservation("res1", "user1", "Viagem de Férias", "Rua A, 123", check_in_str, check_out_str, "Pendente")

    new_check_in_dt = datetime.strptime("26/12/2024 às 15h00", "%d/%m/%Y às %Hh%M")
    new_check_out_dt = datetime.strptime("31/12/2024 às 12h00", "%d/%m/%Y às %Hh%M")

    reservation.update_reservation(
        new_check_in=new_check_in_dt,
        new_check_out=new_check_out_dt,
        new_status="Confirmada",
    )
    assert reservation.check_in == new_check_in_dt
    assert reservation.check_out == new_check_out_dt
    assert reservation.status == "Confirmada"


def test_create_bedroom():
    bedroom = Bedroom("bed1", "Quarto Deluxe", "Quarto espaçoso com vista para o mar", "R$ 300.00", "deluxe_img.jpg")
    assert bedroom.title == "Quarto Deluxe"
    assert bedroom.price == "R$ 300.00"