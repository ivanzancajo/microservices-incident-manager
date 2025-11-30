import httpx
import time
import sys

# URLs internas de la red Docker (acceso directo a los microservicios)
USERS_SERVICE_URL = "http://users-service:8000"
INCIDENTS_SERVICE_URL = "http://incidents-service:8000"

# Datos de prueba
mock_users = [
    {"name": "Ana López", "email": "ana.lopez@example.com"},
    {"name": "Carlos Méndez", "email": "carlos.mendez@example.com"},
    {"name": "Beatriz Gámiz", "email": "beatriz.gamiz@example.com"}
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
    """Espera a que los servicios estén disponibles antes de lanzar datos."""
    print("⏳ Esperando a que los servicios estén listos...")
    retries = 5
    while retries > 0:
        try:
            u_resp = httpx.get(f"{USERS_SERVICE_URL}/health", timeout=2)
            i_resp = httpx.get(f"{INCIDENTS_SERVICE_URL}/health", timeout=2)
            if u_resp.status_code == 200 and i_resp.status_code == 200:
                print("✅ Servicios detectados y operativos.")
                return True
        except Exception:
            pass
        
        print("... servicios no disponibles aún, reintentando en 2s ...")
        time.sleep(2)
        retries -= 1
    return False

def run_seed():
    if not wait_for_services():
        print("❌ Error: Los servicios no respondieron a tiempo.")
        sys.exit(1)

    print("\n🚀 Iniciando carga de datos de prueba...\n")

    # 1. Crear Usuarios y guardar sus IDs
    email_to_id_map = {}

    print("--- Creando Usuarios ---")
    for user_data in mock_users:
        try:
            # Intentamos crear el usuario
            response = httpx.post(f"{USERS_SERVICE_URL}/usuarios", json=user_data)
            
            if response.status_code == 201:
                created_user = response.json()
                print(f"✅ Usuario creado: {created_user['name']} (ID: {created_user['id']})")
                email_to_id_map[user_data['email']] = created_user['id']
            
            elif response.status_code == 400:
                print(f"⚠️  El usuario {user_data['email']} ya existe. Intentando recuperar ID...")
                # Si ya existe, listamos para buscar su ID (solución simple para script de seed)
                all_users = httpx.get(f"{USERS_SERVICE_URL}/usuarios").json()
                for u in all_users:
                    if u['email'] == user_data['email']:
                        email_to_id_map[user_data['email']] = u['id']
                        print(f"   -> ID recuperado: {u['id']}")
                        break
            else:
                print(f"❌ Error creando usuario {user_data['name']}: {response.text}")

        except Exception as e:
            print(f"❌ Excepción conectando con Users Service: {e}")

    # 2. Crear Incidencias usando los IDs recuperados
    print("\n--- Creando Incidencias ---")
    for inc in mock_incidents:
        email = inc.pop("user_email") # Sacamos el email y lo quitamos del dict
        user_id = email_to_id_map.get(email)

        if not user_id:
            print(f"⏭️  Saltando incidencia '{inc['title']}': Usuario no encontrado ({email})")
            continue

        # Asignamos el ID real
        inc["user_id"] = user_id

        try:
            response = httpx.post(f"{INCIDENTS_SERVICE_URL}/incidencias", json=inc)
            if response.status_code == 201:
                data = response.json()
                print(f"✅ Incidencia creada: '{data['title']}' asignada a User ID {user_id}")
            elif response.status_code == 400:
                 print(f"⚠️  Incidencia duplicada o error lógico: {response.text}")
            else:
                print(f"❌ Error creando incidencia: {response.text}")
        except Exception as e:
            print(f"❌ Excepción conectando con Incidents Service: {e}")

    print("\n✨ Carga de datos finalizada exitosamente.")

if __name__ == "__main__":
    run_seed()