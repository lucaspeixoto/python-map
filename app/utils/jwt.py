from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.schemas import user as user_schema

SECRET_KEY = "secret-key"  # Idealmente, use um segredo mais forte e salve isso em variáveis de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tempo de expiração do token em minutos

# Função para gerar o token de acesso
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token e retornar os dados do usuário
def verify_access_token(token: str) -> user_schema.UserOut:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return user_schema.UserOut(**payload)  # Retorna os dados do usuário
    except JWTError:
        return None
