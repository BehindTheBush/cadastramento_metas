from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Agencia(Base):
    __tablename__ = "agencias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    criado_em = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    id_regional = Column(Integer, ForeignKey("regionais.id"), nullable=False)

    regional = relationship("Regional", back_populates="agencias")
    colaboradores = relationship("Colaborador", back_populates="agencia")

    def __repr__(self):
        return (
            f"<Agencia(id={self.id}, nome='{self.nome}', endereco='{self.endereco}')>"
        )
