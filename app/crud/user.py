from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from app.db import models
from app.schemas import user as user_schema
from app.utils.security import hash_password, verify_password

def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        is_active=True,
        is_superuser=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(
        models.User.id == user_id,
        models.User.deleted_at.is_(None)
    ).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(
        models.User.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_data: user_schema.UserUpdate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def soft_delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.deleted_at = datetime.utcnow()
    db.commit()
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and verify_password(password, user.password):  
        return user
    return None