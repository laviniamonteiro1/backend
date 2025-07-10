import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from blog.infra.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # A importação da classe Bedroom é necessária aqui APENAS para o type checking do Pylance/MyPy.
    from blog.domain.entities.bedroom import Bedroom


class BedroomModel(Base):
    __tablename__ = "bedrooms"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    description: Mapped[str] = mapped_column(sa.String, nullable=False)
    price: Mapped[str] = mapped_column(sa.String, nullable=False)
    image: Mapped[str] = mapped_column(sa.String, nullable=False)

    @classmethod
    def from_entity(cls, entity: "Bedroom") -> "BedroomModel":  # "Bedroom" como string
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            price=entity.price,
            image=entity.image,
        )

    def to_entity(self) -> "Bedroom":
        from blog.domain.entities.bedroom import Bedroom

        return Bedroom(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price,
            image=self.image,
        )
