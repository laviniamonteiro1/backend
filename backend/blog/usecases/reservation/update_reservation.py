from typing import Optional
from datetime import datetime

from blog.domain.entities.reservation import Reservation
from blog.domain.repositories.reservation_repository import ReservationRepository


class UpdateReservation:
    def __init__(self, reservation_repo: ReservationRepository):
        self._reservation_repo = reservation_repo

    async def execute(
        self,
        reservation_id: str,
        new_title: Optional[str] = None,
        new_address: Optional[str] = None,
        new_check_in_str: Optional[str] = None,
        new_check_out_str: Optional[str] = None,
        new_status: Optional[str] = None,
    ) -> Optional[Reservation]:
        reservation = await self._reservation_repo.get_reservation_by_id(reservation_id)
        if reservation:
            reservation.update_reservation(
                new_title=new_title,
                new_address=new_address,
                new_check_in_str=new_check_in_str,
                new_check_out_str=new_check_out_str,
                new_status=new_status,
            )
            return await self._reservation_repo.update_reservation(reservation)
        return None
