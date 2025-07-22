from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


class RegisterUserInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")
    role: Literal["user", "admin"] = "user"
    phone: Optional[str] = Field(None, description="Número de telefone do usuário")
    document: Optional[str] = Field(None, description="Número de documento do usuário")
    address: Optional[str] = Field(None, description="Endereço completo do usuário")


class LoginUserInput(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")


class SetCurrentUserInput(BaseModel):
    user_id: str = Field(..., description="ID do usuário a ser definido como atual")


class UserOutput(BaseModel):
    id: str = Field(..., description="ID do usuário")
    name: str = Field(..., min_length=3, max_length=50, description="Nome do usuário")
    email: str = Field(..., description="Email do usuário")
    role: str = Field(..., description="Papel do usuário (admin, user)")
    phone: Optional[str] = Field(None, description="Número de telefone do usuário")
    document: Optional[str] = Field(None, description="Número de documento do usuário")
    address: Optional[str] = Field(None, description="Endereço completo do usuário")

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            email=str(user.email),
            role=user.role,
            phone=user.phone,
            document=user.document,
            address=user.address,
        )


class MessageUserResponse(BaseModel):
    message: str
    user: UserOutput