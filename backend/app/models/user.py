from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """Modelo de usuário do sistema"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    nivel_acesso = Column(String(50), nullable=False)  # 'admin' ou 'cadastrador'
    ativo = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    colaborador = relationship("Colaborador", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', nivel_acesso='{self.nivel_acesso}')>"
