import os
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Leemos los secretos inyectados por Docker 
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

# Define que esperamos el token en el header 'Authorization: Bearer <token>'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    # Preparamos la excepción 401
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Valida firma y expiración automáticamente (SCRUM-92)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extraemos el ID (user_id) del 'sub'
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
            
        return int(user_id_str)
        
    except JWTError:
        # Si el token está mal formado, caducado o firma falsa -> 401 (SCRUM-93)
        raise credentials_exception