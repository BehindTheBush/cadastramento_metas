from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    apenas_ativos: bool = True,
    db: Session = Depends(get_db)
):
    """Lista todos os usuários"""
    users = user_service.get_users(db, skip=skip, limit=limit, apenas_ativos=apenas_ativos)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def buscar_usuario(user_id: int, db: Session = Depends(get_db)):
    """Busca usuário por ID"""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    """Cria novo usuário"""
    # Verificar se email já existe
    db_user = user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    return user_service.create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse)
async def atualizar_usuario(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza usuário existente"""
    # Se email está sendo atualizado, verificar se não existe
    if user_update.email:
        existing_user = user_service.get_user_by_email(db, user_update.email)
        if existing_user is not None and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
    
    user = user_service.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(user_id: int, db: Session = Depends(get_db)):
    """Desativa usuário (soft delete)"""
    success = user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return None

