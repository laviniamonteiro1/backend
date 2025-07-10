from typing import Optional
from datetime import datetime

from blog.domain.entities.reservation import Reservation
from blog.domain.repositories.reservation_repository import ReservationRepository
from blog.domain.repositories.user_repository import UserRepository


class CreateReservation:
    def __init__(self, reservation_repo: ReservationRepository, user_repo: UserRepository):
        self._reservation_repo = reservation_repo
        self._user_repo = user_repo

    async def execute(self, user_id: str, title: str, address: str, check_in_str: str, check_out_str: str) -> Reservation:
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        new_reservation = Reservation(
            id=None,
            user_id=user_id,
            title=title,
            address=address,
            check_in=check_in_str,
            check_out=check_out_str,
            status="Pendente",
        )
        return await self._reservation_repo.create_reservation(new_reservation)