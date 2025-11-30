from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Regional(Base):
    """Modelo de regional da organização"""

    __tablename__ = "regionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False)
    descricao = Column(String(500), nullable=True)

    agencias = relationship("Agencia", back_populates="regional")

    def __repr__(self):
        return f"<Regional(id={self.id}, nome='{self.nome}', codigo='{self.codigo}')>"
