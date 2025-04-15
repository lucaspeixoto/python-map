from passlib.context import CryptContext

# Instanciando o contexto para criptografia com Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criar o hash de uma senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar se a senha fornecida corresponde ao hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
