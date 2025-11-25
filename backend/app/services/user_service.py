from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional, List


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca usuário por email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Busca usuário por ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, apenas_ativos: bool = True) -> List[User]:
    """Lista usuários com paginação"""
    query = db.query(User)
    if apenas_ativos:
        query = query.filter(User.ativo == True)
    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Cria novo usuário"""
    hashed_password = get_password_hash(user.senha)
    db_user = User(
        email=user.email,
        nome=user.nome,
        senha_hash=hashed_password,
        nivel_acesso=user.nivel_acesso.value,
        ativo=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Atualiza usuário existente"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Se senha foi fornecida, fazer hash
    if 'senha' in update_data:
        update_data['senha_hash'] = get_password_hash(update_data.pop('senha'))
    
    # Converter enum para string se necessário
    if 'nivel_acesso' in update_data and update_data['nivel_acesso']:
        update_data['nivel_acesso'] = update_data['nivel_acesso'].value
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Desativa usuário (soft delete)"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db_user.ativo = False
    db.commit()
    return True


def authenticate_user(db: Session, email: str, senha: str) -> Optional[User]:
    """Autentica usuário com email e senha"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(senha, user.senha_hash):
        return None
    if not user.ativo:
        return None
    return user
