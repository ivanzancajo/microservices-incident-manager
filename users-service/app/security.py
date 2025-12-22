import os
from datetime import datetime, timedelta, timezone
from typing import Union
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, schemas, database

# 1. Configuración de Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuración JWT
SECRET_KEY = os.getenv("JWT_SECRET", "secret_fallback")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Esquema de autenticación: Le dice a FastAPI que el token viene en
# la cabecera "Authorization: Bearer <token>" y que el login es en "/auth/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db)
) -> schemas.UserOut:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales (Token inválido o expirado)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extraer el ID del usuario ('sub' es el estándar JWT para subject)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        # Si el token está mal formado, firma incorrecta o expirado
        raise credentials_exception

    # Verificar que el usuario sigue existiendo en la BD
    # Esto evita que un usuario borrado siga entrando con un token viejo.
    user = crud.get_user(db, user_id=int(user_id))
    
    if user is None:
        raise credentials_exception
        
    return user