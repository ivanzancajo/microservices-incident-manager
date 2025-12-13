import os
from datetime import datetime, timedelta, timezone
from typing import Union
from passlib.context import CryptContext
from jose import jwt

# 1. Configuración de Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET", "secret_fallback")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Genera un JWT firmado con nuestra clave secreta.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos la expiración al payload
    to_encode.update({"exp": expire})
    
    # Firmamos el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt