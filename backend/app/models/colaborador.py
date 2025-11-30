from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class Colaborador(Base):
    """Modelo de colaborador associado a um usuário"""
    __tablename__ = "colaboradores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agencia_id = Column(Integer, ForeignKey("agencias.id"), nullable=False)
    centro_custo = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=False)
    
    
    user = relationship("User", back_populates="colaborador")
    agencia = relationship("Agencia", back_populates="colaboradores")
    
    def __repr__(self):
        return f"<Colaborador(id={self.id}, user_id={self.user_id}, centro_custo='{self.centro_custo}', cargo='{self.cargo}')>"