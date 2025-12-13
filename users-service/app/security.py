import os
from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from jose import jwt

# 1. Configuración de Hashing (lo que ya tenías)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuración JWT (Leemos las variables que pusimos en el .env)
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Genera un JWT firmado con nuestra clave secreta.
    """
    to_encode = data.copy()
    
    # Calculamos cuándo expira
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadimos la expiración al payload del token
    to_encode.update({"exp": expire})
    
    # Firmamos el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt