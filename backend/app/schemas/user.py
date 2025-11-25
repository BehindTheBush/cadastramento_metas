from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class NivelAcesso(str, Enum):
    """Níveis de acesso permitidos"""
    ADMIN = "admin"
    CADASTRADOR = "cadastrador"


class UserBase(BaseModel):
    """Schema base de usuário"""
    email: EmailStr
    nome: str
    nivel_acesso: NivelAcesso


class UserCreate(UserBase):
    """Schema para criação de usuário"""
    senha: str
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        return v


class UserUpdate(BaseModel):
    """Schema para atualização de usuário"""
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    senha: Optional[str] = None
    nivel_acesso: Optional[NivelAcesso] = None
    ativo: Optional[bool] = None
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('Senha deve ter no mínimo 6 caracteres')
        return v


class UserResponse(UserBase):
    """Schema de resposta de usuário"""
    id: int
    ativo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    senha: str


class Token(BaseModel):
    """Schema de token de autenticação"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Dados do token decodificado"""
    email: Optional[str] = None
    nivel_acesso: Optional[str] = None

