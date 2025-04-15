from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.schemas import user as user_schema
from app.core.config import settings

# Função para gerar o token de acesso
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Função para verificar o token e retornar os dados do usuário
def verify_access_token(token: str) -> user_schema.UserOut:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return user_schema.UserOut(**payload)  # Retorna os dados do usuário
    except JWTError:
        return None
