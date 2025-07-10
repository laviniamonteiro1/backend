from typing import Optional

from blog.domain.entities.reservation import Reservation
from blog.domain.repositories.reservation_repository import ReservationRepository


class GetUserReservationById:
    def __init__(self, reservation_repo: ReservationRepository):
        self._reservation_repo = reservation_repo

    async def execute(self, reservation_id: str) -> Optional[Reservation]:
        return await self._reservation_repo.get_reservation_by_id(reservation_id)
