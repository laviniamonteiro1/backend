import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid
from blog.infra.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from blog.domain.entities.reservation import Reservation


class ReservationModel(Base):
    __tablename__ = "reservations"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(sa.String, sa.ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    address: Mapped[str] = mapped_column(sa.String, nullable=False)
    check_in: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    check_out: Mapped[datetime] = mapped_column(sa.DateTime, nullable=False)
    status: Mapped[str] = mapped_column(sa.String, default="Pendente")

    user = relationship("UserModel", back_populates="reservations")

    @classmethod
    def from_entity(cls, entity: "Reservation") -> "ReservationModel":
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            address=entity.address,
            check_in=entity.check_in,
            check_out=entity.check_out,
            status=entity.status,
        )

    def to_entity(self) -> "Reservation":
        from blog.domain.entities.reservation import Reservation

        return Reservation(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            address=self.address,
            check_in=self.check_in.strftime("%d/%m/%Y às %Hh%M"),
            check_out=self.check_out.strftime("%d/%m/%Y às %Hh%M"),
            status=self.status,
        )