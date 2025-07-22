import uuid
import pytest
import datetime

from blog.domain.entities.user import User
from blog.domain.entities.reservation import Reservation
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


def create_test_user() -> User:
    return User(
        id=str(uuid.uuid4()),
        name="Test User",
        email=Email("test@example.com"),
        password=Password("Secure@Pass123!"),
        role="user",
        # CORREÇÃO: Adicionado phone, document, address para o construtor de User
        phone=None,
        document=None,
        address=None,
    )


def create_test_reservation(user_id: str) -> Reservation:
    check_in_str = (
        datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=10)
    ).strftime("%d/%m/%Y às %Hh%M")
    check_out_str = (
        datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=15)
    ).strftime("%d/%m/%Y às %Hh%M")
    return Reservation(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title="Viagem de Teste",
        address="Rua Teste, 123",
        check_in=check_in_str,
        check_out=check_out_str,
        status="Pendente",  # Mantido "Pendente" para o estado inicial de criação
    )


@pytest.mark.asyncio
async def test_create_reservation_use_case():
    user_repo = InMemoryUserRepository()
    reservation_repo = InMemoryReservationRepository()
    user = create_test_user()
    await user_repo.register(user)

    usecase = CreateReservation(reservation_repo, user_repo)
    check_in_str = (
        datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=10)
    ).strftime("%d/%m/%Y às %Hh%M")
    check_out_str = (
        datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=15)
    ).strftime("%d/%m/%Y às %Hh%M")

    reservation = await usecase.execute(
        user_id=user.id,
        title="Reserva de Exemplo",
        address="Endereço Teste",
        check_in_str=check_in_str,
        check_out_str=check_out_str,
    )

    assert reservation is not None
    assert reservation.title == "Reserva de Exemplo"
    assert reservation.user_id == user.id
    assert await reservation_repo.get_reservation_by_id(reservation.id) == reservation


@pytest.mark.asyncio
async def test_get_user_reservation_by_id_use_case():
    reservation_repo = InMemoryReservationRepository()
    user = create_test_user()
    reservation = create_test_reservation(user.id)
    await reservation_repo.create_reservation(reservation)

    usecase = GetUserReservationById(reservation_repo)
    found_reservation = await usecase.execute(reservation.id)

    assert found_reservation == reservation


@pytest.mark.asyncio
async def test_get_user_reservation_by_id_not_found_use_case():
    reservation_repo = InMemoryReservationRepository()
    usecase = GetUserReservationById(reservation_repo)
    found_reservation = await usecase.execute(str(uuid.uuid4()))

    assert found_reservation is None


@pytest.mark.asyncio
async def test_cancel_reservation_use_case():
    reservation_repo = InMemoryReservationRepository()
    user = create_test_user()
    reservation = create_test_reservation(user.id)
    await reservation_repo.create_reservation(reservation)

    usecase = CancelReservation(reservation_repo)
    canceled_reservation = await usecase.execute(reservation.id)

    assert canceled_reservation is not None
    # CORREÇÃO: O status agora é "cancelled" (inglês, minúsculo)
    assert canceled_reservation.status == "cancelled"
    assert (
        await reservation_repo.get_reservation_by_id(reservation.id)
        == canceled_reservation
    )


@pytest.mark.asyncio
async def test_update_reservation_use_case():
    reservation_repo = InMemoryReservationRepository()
    user = create_test_user()
    reservation = create_test_reservation(user.id)
    await reservation_repo.create_reservation(reservation)

    usecase = UpdateReservation(reservation_repo)
    new_title = "Reserva Teste Atualizada"
    new_address = "Novo Endereço, 456"
    new_check_in_str = (
        datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=12)
    ).strftime("%d/%m/%Y às %Hh%M")
    new_check_out_str = (
        datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(days=18)
    ).strftime("%d/%m/%Y às %Hh%M")
    new_status = "confirmed"  # Status em inglês, como a entidade espera

    updated_reservation = await usecase.execute(
        reservation_id=reservation.id,
        # CORREÇÃO: Adicionado new_title e new_address
        new_title=new_title,
        new_address=new_address,
        new_check_in_str=new_check_in_str,
        new_check_out_str=new_check_out_str,
        new_status=new_status,
    )

    assert updated_reservation is not None
    assert updated_reservation.title == new_title
    assert updated_reservation.address == new_address
    assert updated_reservation.check_in == datetime.datetime.strptime(
        new_check_in_str, "%d/%m/%Y às %Hh%M"
    )
    assert updated_reservation.check_out == datetime.datetime.strptime(
        new_check_out_str, "%d/%m/%Y às %Hh%M"
    )
    assert updated_reservation.status == new_status
    assert (
        await reservation_repo.get_reservation_by_id(reservation.id)
        == updated_reservation
    )


@pytest.mark.asyncio
async def test_delete_reservation_use_case():
    reservation_repo = InMemoryReservationRepository()
    user = create_test_user()
    reservation = create_test_reservation(user.id)
    await reservation_repo.create_reservation(reservation)

    usecase = DeleteReservation(reservation_repo)
    deleted = await usecase.execute(reservation.id)

    assert deleted is True
    assert await reservation_repo.get_reservation_by_id(reservation.id) is None


@pytest.mark.asyncio
async def test_list_reservation_use_case():
    reservation_repo = InMemoryReservationRepository()
    user1 = create_test_user()
    reservation1 = create_test_reservation(user1.id)
    reservation2 = create_test_reservation(user1.id)

    user2 = create_test_user()
    reservation3 = create_test_reservation(user2.id)

    await reservation_repo.create_reservation(reservation1)
    await reservation_repo.create_reservation(reservation2)
    await reservation_repo.create_reservation(reservation3)

    usecase = ListReservation(reservation_repo)
    reservations = await usecase.execute()

    assert len(reservations) == 3
    assert reservation1 in reservations
    assert reservation2 in reservations
    assert reservation3 in reservations
