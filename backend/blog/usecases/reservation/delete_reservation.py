from blog.domain.repositories.reservation_repository import ReservationRepository


class DeleteReservation:
    def __init__(self, reservation_repo: ReservationRepository):
        self._reservation_repo = reservation_repo

    async def execute(self, reservation_id: str) -> bool:
        return await self._reservation_repo.delete_reservation(reservation_id)
