import os
import httpx
from fastapi import FastAPI, HTTPException, Header
from typing import List, Optional

app = FastAPI(title="BFF Gateway")

# URLs internas de la red Docker
USERS_SERVICE_URL = os.getenv("USERS_SERVICE_URL")
INCIDENTS_SERVICE_URL = os.getenv("INCIDENTS_SERVICE_URL")

@app.get("/incidencias-detalladas")
async def get_incidents_with_details(authorization: Optional[str] = Header(None)):
    # Si no hay token, rechazamos antes de intentar nada (ahorra tiempo)
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autenticación no proporcionado")
    # Preparamos las cabeceras para las peticiones internas
    forward_headers = {"Authorization": authorization}
    async with httpx.AsyncClient() as client:
        # 1. Obtener todas las incidencias
        try:
            incidents_resp = await client.get(
                f"{INCIDENTS_SERVICE_URL}/incidencias",
                headers=forward_headers
            )

            # Si el token expiró o es inválido, el microservicio devolverá 401
            if incidents_resp.status_code == 401:
                raise HTTPException(status_code=401, detail="Token inválido o expirado")
            
            incidents_resp.raise_for_status()
            incidents = incidents_resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener incidencias: {str(e)}")

        # 2. Recolectar IDs de usuarios únicos
        user_ids = list({inc['user_id'] for inc in incidents if 'user_id' in inc})

        # 3. Obtener detalles de esos usuarios en una sola llamada (Batch)
        users_map = {}
        if user_ids:
            try:
                users_resp = await client.post(
                    f"{USERS_SERVICE_URL}/usuarios/batch", 
                    json=user_ids,
                    headers=forward_headers
                )
                users_resp.raise_for_status()
                users_list = users_resp.json()
                # Crear diccionario para búsqueda rápida: {id: {datos_usuario}}
                users_map = {u['id']: u for u in users_list}
            except Exception as e:
                print(f"Error recuperando usuarios: {e}")
                # Opcional: Continuar sin datos de usuario o fallar

        # 4. Mezclar datos (Hidratación)
        results = []
        for inc in incidents:
            # Creamos una copia para no mutar si no es necesario
            inc_extended = inc.copy()
            # Inyectamos el objeto 'owner' completo usando el mapa
            inc_extended['owner'] = users_map.get(inc['user_id'], None)
            results.append(inc_extended)

        return results