from typing import List
from blog.domain.entities.reservation import Reservation
from blog.domain.repositories.reservation_repository import ReservationRepository


class ListReservation:
    def __init__(self, reservation_repo: ReservationRepository):
        self._reservation_repo = reservation_repo

    async def execute(self) -> List[Reservation]:
        return await self._reservation_repo.get_all_reservations()
