import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
import uuid
from blog.infra.database import Base
from typing import Optional


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role: Mapped[str] = mapped_column(sa.String, default="user")

    phone: Mapped[Optional[str]] = mapped_column(sa.String, nullable=True)
    document: Mapped[Optional[str]] = mapped_column(sa.String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(sa.String, nullable=True)

    reservations = relationship(
        "ReservationModel", back_populates="user", cascade="all, delete"
    )

    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(
            id=entity.id,
            name=entity.name,
            email=str(entity.email),
            password=str(entity.password),
            role=entity.role,
            phone=entity.phone,
            document=entity.document,
            address=entity.address,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=Email(self.email),
            password=Password(self.password),
            role=self.role,
            phone=self.phone,
            document=self.document,
            address=self.address,
        )