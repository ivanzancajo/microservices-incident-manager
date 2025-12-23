import httpx
import time
import sys
import os

# URLs internas de la red Docker
USERS_SERVICE_URL = "http://users-service:8000"
INCIDENTS_SERVICE_URL = "http://incidents-service:8000"

# Datos de prueba (Incluimos contraseña para el login)
DEFAULT_PASSWORD = "password123"

mock_users = [
    {"name": "Ana López", "email": "ana.lopez@example.com", "password": DEFAULT_PASSWORD},
    {"name": "Carlos Méndez", "email": "carlos.mendez@example.com", "password": DEFAULT_PASSWORD},
    {"name": "Beatriz Gámiz", "email": "beatriz.gamiz@example.com", "password": DEFAULT_PASSWORD}
]

mock_incidents = [
    {
        "title": "Fallo en la impresora red",
        "description": "La impresora de la planta 2 no responde al ping.",
        "user_email": "ana.lopez@example.com",
        "status": "abierta"
    },
    {
        "title": "VPN desconectada",
        "description": "No puedo acceder a los servidores internos desde casa.",
        "user_email": "carlos.mendez@example.com",
        "status": "en_progreso"
    },
    {
        "title": "Monitor parpadea",
        "description": "El monitor secundario se apaga intermitentemente.",
        "user_email": "ana.lopez@example.com",
        "status": "abierta"
    },
    {
        "title": "Solicitud licencia software",
        "description": "Necesito licencia para PyCharm Professional.",
        "user_email": "beatriz.gamiz@example.com",
        "status": "cerrada"
    }
]

def wait_for_services():
    print("⏳ Esperando a que los servicios estén listos...")
    retries = 10
    while retries > 0:
        try:
            u_resp = httpx.get(f"{USERS_SERVICE_URL}/health", timeout=2)
            i_resp = httpx.get(f"{INCIDENTS_SERVICE_URL}/health", timeout=2)
            if u_resp.status_code == 200 and i_resp.status_code == 200:
                print("✅ Servicios detectados y operativos.")
                return True
        except Exception:
            pass
        
        print(f"... reintentando en 2s ({retries} restantes)...")
        time.sleep(2)
        retries -= 1
    return False

def run_seed():
    if not wait_for_services():
        print("❌ Error: Los servicios no respondieron a tiempo.")
        sys.exit(1)

    print("\n🚀 Iniciando carga de datos AUTENTICADA...\n")

    # Diccionario para guardar el token de cada email
    # ¡Esta es la variable que te faltaba!
    user_tokens = {}

    print("--- 1. Creando Usuarios y Obteniendo Tokens ---")
    for user_data in mock_users:
        try:
            # A) Crear usuario (o ignorar si ya existe)
            resp_create = httpx.post(f"{USERS_SERVICE_URL}/usuarios", json=user_data)
            
            if resp_create.status_code == 201:
                print(f"👤 Usuario creado: {user_data['email']}")
            elif resp_create.status_code == 400:
                print(f"ℹ️  El usuario {user_data['email']} ya existe (continuamos con login).")
            else:
                print(f"❌ Fallo creando usuario {user_data['email']}: {resp_create.text}")
                # Si falla crear, intentamos login por si acaso ya existía
            
            # B) Login para obtener token
            # El endpoint /auth/login espera form-data
            login_data = {
                "username": user_data['email'],
                "password": user_data['password']
            }
            
            resp_login = httpx.post(f"{USERS_SERVICE_URL}/auth/login", data=login_data)
            
            if resp_login.status_code == 200:
                token = resp_login.json()["access_token"]
                user_tokens[user_data['email']] = token
                print(f"🔑 Token obtenido para: {user_data['email']}")
            else:
                print(f"⚠️ No se pudo loguear a {user_data['email']}. Status: {resp_login.status_code}")

        except Exception as e:
            print(f"❌ Excepción conectando con Users Service: {e}")

    print("\n--- 2. Creando Incidencias (Usando JWT) ---")
    for inc in mock_incidents:
        user_email = inc.pop("user_email") 
        token = user_tokens.get(user_email)

        if not token:
            print(f"⏭️  Saltando incidencia '{inc['title']}': No tenemos token para {user_email}")
            continue

        # Header de autorización
        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Nota: Ya NO enviamos 'user_id' porque lo eliminamos del esquema en SCRUM-94
        try:
            response = httpx.post(
                f"{INCIDENTS_SERVICE_URL}/incidencias", 
                json=inc,
                headers=headers
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Incidencia creada: '{data['title']}' (ID: {data['id']})")
            else:
                print(f"❌ Error creando incidencia: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Excepción conectando con Incidents Service: {e}")

    print("\n✨ Carga de datos finalizada exitosamente.")

if __name__ == "__main__":
    run_seed()