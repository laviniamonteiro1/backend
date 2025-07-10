from typing import Optional, List, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from blog.domain.repositories.reservation_repository import ReservationRepository
from blog.infra.models.reservation_model import ReservationModel

if TYPE_CHECKING:
    from blog.domain.entities.reservation import Reservation


class SQLAlchemyReservationRepository(ReservationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_reservation(self, reservation: "Reservation") -> "Reservation":
        model = ReservationModel.from_entity(reservation)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        reservation.id = model.id
        return model.to_entity()

    async def get_reservation_by_id(self, reservation_id: str) -> Optional["Reservation"]:
        stmt = select(ReservationModel).where(ReservationModel.id == reservation_id)
        result = await self._session.execute(stmt)
        reservation_model = result.scalar_one_or_none()
        return reservation_model.to_entity() if reservation_model else None

    async def get_reservations_by_user_id(self, user_id: str) -> List["Reservation"]:
        stmt = select(ReservationModel).where(ReservationModel.user_id == user_id)
        result = await self._session.execute(stmt)
        reservation_models = result.scalars().all()
        return [model.to_entity() for model in reservation_models]

    async def update_reservation(self, reservation: "Reservation") -> Optional["Reservation"]:
        stmt = select(ReservationModel).where(ReservationModel.id == reservation.id)
        result = await self._session.execute(stmt)
        existing_model = result.scalar_one_or_none()

        if existing_model:
            existing_model.title = reservation.title
            existing_model.address = reservation.address
            existing_model.check_in = reservation.check_in
            existing_model.check_out = reservation.check_out
            existing_model.status = reservation.status

            await self._session.commit()
            await self._session.refresh(existing_model)
            return existing_model.to_entity()
        return None

    async def delete_reservation(self, reservation_id: str) -> bool:
        stmt = delete(ReservationModel).where(ReservationModel.id == reservation_id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount > 0

    async def get_all_reservations(self) -> List["Reservation"]:
        stmt = select(ReservationModel)
        result = await self._session.execute(stmt)
        reservation_models = result.scalars().all()
        return [model.to_entity() for model in reservation_models]