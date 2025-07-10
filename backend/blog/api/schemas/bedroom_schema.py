from pydantic import BaseModel, Field
from typing import Optional, List


class BedroomOutput(BaseModel):
    id: str = Field(..., description="ID do quarto")
    title: str = Field(
        ..., min_length=3, max_length=100, description="Título do quarto"
    )
    description: str = Field(
        ..., min_length=10, description="Descrição detalhada do quarto"
    )
    price: str = Field(..., description="Preço do quarto por noite (ex: 'R$ 150.00')")
    image: str = Field(
        ..., description="URL ou nome do arquivo da imagem principal do quarto"
    )

    @classmethod
    def from_entity(cls, entity):
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            price=entity.price,
            image=entity.image,
        )


class MessageBedroomResponse(BaseModel):
    message: str
    bedroom: Optional[BedroomOutput] = None
    bedrooms: Optional[List[BedroomOutput]] = None
