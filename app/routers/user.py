from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas import user as user_schema
from app.crud import user as user_crud
from app.utils.jwt import create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

@router.post("/", response_model=user_schema.UserOut)
def create(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, user)
    return db_user

@router.get("/{user_id}", response_model=user_schema.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.get("/", response_model=List[user_schema.UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_crud.get_all_users(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=user_schema.UserOut)
def update(user_id: int, user_data: user_schema.UserUpdate, db: Session = Depends(get_db)):
    updated = user_crud.update_user(db, user_id, user_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated

@router.delete("/{user_id}", response_model=user_schema.UserOut)
def delete(user_id: int, db: Session = Depends(get_db)):
    deleted = user_crud.soft_delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return deleted


@router.post("/login", response_model=user_schema.UserOut)
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    access_token = create_access_token(data={"sub": db_user.email})  
    return {"access_token": access_token, "token_type": "bearer", "user": db_user}

@router.get("/me", response_model=user_schema.UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user