from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.utils.jwt import verify_access_token
from app.db.database import get_db
from app.crud.user import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar o usuário.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_data = verify_access_token(token)
    if not user_data or not user_data.email:
        raise credentials_exception

    user = get_user_by_email(db, email=user_data.email)
    if not user or user.deleted_at is not None:
        raise credentials_exception

    return user
