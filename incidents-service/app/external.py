import os
import httpx
from fastapi import HTTPException, status

# Leemos la URL del servicio de usuarios de las variables de entorno
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")

def validate_user_exists(user_id: int):
    url = f"{USERS_SERVICE_URL}/usuarios/{user_id}"
    try:
        # Timeout corto para no bloquear la API si el otro servicio es lento
        response = httpx.get(url, timeout=5.0)
        
        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"El usuario con ID {user_id} no existe."
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                detail="Error validando el usuario en el servicio externo."
            )
            
        return True

    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="No se pudo conectar con el servicio de usuarios."
        )