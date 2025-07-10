from blog.domain.repositories.reservation_repository import ReservationRepository
from blog.domain.entities.reservation import Reservation
from typing import Optional, List
import pytest


class InMemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self._reservations = {}

    @pytest.mark.asyncio
    async def create_reservation(self, reservation: Reservation) -> Reservation:
        """Cria uma nova reserva no repositório em memória."""
        self._reservations[reservation.id] = reservation
        return reservation

    @pytest.mark.asyncio
    async def get_reservation_by_id(self, reservation_id: str) -> Optional[Reservation]:
        """Busca uma reserva pelo ID."""
        return self._reservations.get(reservation_id)

    @pytest.mark.asyncio
    async def get_reservations_by_user_id(self, user_id: str) -> List[Reservation]:
        """Busca todas as reservas de um usuário específico."""
        return [
            reservation
            for reservation in self._reservations.values()
            if reservation.user_id == user_id
        ]

    @pytest.mark.asyncio
    async def update_reservation(
        self, reservation: Reservation
    ) -> Optional[Reservation]:
        """Atualiza uma reserva existente. Retorna None se não encontrar a reserva."""
        if reservation.id in self._reservations:
            self._reservations[reservation.id] = reservation
            return reservation
        return None

    @pytest.mark.asyncio
    async def delete_reservation(self, reservation_id: str) -> bool:
        """Deleta uma reserva pelo ID. Retorna True se a reserva foi deletada, False caso contrário."""
        if reservation_id in self._reservations:
            del self._reservations[reservation_id]
            return True
        return False

    @pytest.mark.asyncio
    async def get_all_reservations(self) -> List[Reservation]:
        """Retorna todas as reservas no repositório."""
        return list(self._reservations.values())
