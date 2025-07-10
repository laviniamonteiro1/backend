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
        new_check_in_str: Optional[str] = None,
        new_check_out_str: Optional[str] = None,
        new_status: Optional[str] = None,
    ) -> Optional[Reservation]:
        reservation = await self._reservation_repo.get_reservation_by_id(reservation_id)
        if reservation:
            check_in_dt = datetime.strptime(new_check_in_str, "%d/%m/%Y às %Hh%M") if new_check_in_str else None
            check_out_dt = datetime.strptime(new_check_out_str, "%d/%m/%Y às %Hh%M") if new_check_out_str else None

            reservation.update_reservation(
                new_check_in=check_in_dt,
                new_check_out=check_out_dt,
                new_status=new_status,
            )
            return await self._reservation_repo.update_reservation(reservation)
        return None