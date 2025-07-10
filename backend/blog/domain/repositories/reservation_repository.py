from abc import ABC, abstractmethod
from typing import List, Optional
from blog.domain.entities.reservation import Reservation


class ReservationRepository(ABC):
    @abstractmethod
    async def create_reservation(self, reservation: Reservation) -> Reservation:
        pass

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: str) -> Optional[Reservation]:
        pass

    @abstractmethod
    async def get_reservations_by_user_id(self, user_id: str) -> List[Reservation]:
        pass

    @abstractmethod
    async def update_reservation(self, reservation: Reservation) -> Optional[Reservation]:
        pass

    @abstractmethod
    async def delete_reservation(self, reservation_id: str) -> bool:
        pass

    @abstractmethod
    async def get_all_reservations(self) -> List[Reservation]:
        pass