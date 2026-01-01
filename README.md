# ⚙️ Sistema de Gestión de Incidencias (Microservicios)

Este proyecto implementa una plataforma completa para la **gestión de usuarios e incidencias**, basada en una arquitectura de **microservicios contenerizada**. El sistema ha sido diseñado siguiendo principios de **desacoplamiento**, **escalabilidad** y **aislamiento de datos**, utilizando un **API Gateway (BFF)** como único punto de entrada.

---

## 🚀 Arquitectura y Tecnologías

El sistema se compone de los siguientes contenedores orquestados mediante **Docker Compose**:

| Servicio | Tecnología | Rol Principal | Puerto (Host) |
| :--- | :--- | :--- | :--- |
| **Frontend** | Vue.js 3 + Vite + Nginx | Interfaz de usuario (SPA). | `5173` |
| **BFF Gateway** | Python (FastAPI) | **Backend for Frontend**. Agrega datos y enruta peticiones. | `8080` |
| **Users Service** | Python (FastAPI) | Gestión de usuarios y **Autenticación (JWT)**. | *Interno* |
| **Incidents Service** | Python (FastAPI) | Gestión del ciclo de vida de incidencias. | *Interno* |
| **Databases** | PostgreSQL 15 | Dos instancias independientes (`users-db`, `incidents-db`). | *Interno* |

### Principios de Diseño Implementados

* **Database per Service:** Aislamiento estricto. Usuarios e Incidencias tienen sus propias bases de datos PostgreSQL.
* **API Gateway / BFF:** El frontend nunca habla directamente con los microservicios. El Gateway ("hidrata") las respuestas combinando datos (ej. unir `user_id` de una incidencia con los datos reales del usuario).
* **Seguridad JWT + Refresh Tokens:** Implementación robusta de autenticación con tokens de acceso (vida corta) y tokens de refresco (vida larga) con rotación automática en el cliente.
* **Red Interna:** Por seguridad, los microservicios de backend no exponen puertos al host por defecto; toda comunicación pasa por la red interna de Docker (`internal-network`).

---

## 🛠️ Instalación y Despliegue

### Requisitos Previos

* **Docker Engine** & **Docker Compose (v2)**
* Puerto `5173` y `8080` libres en tu máquina.

### Pasos de Despliegue

1.  **Clonar el repositorio**:
    ```bash
    git clone [https://github.com/ivanzancajo/microservices-incident-manager.git](https://github.com/ivanzancajo/microservices-incident-manager.git)
    cd microservices-incident-manager
    ```

2.  **Configurar entorno**:
    Copia el archivo de ejemplo para establecer las variables de entorno.
    ```bash
    cp .env.example .env
    ```

3.  **Construir y arrancar**:
    Levanta todos los servicios en segundo plano.
    ```bash
    docker compose up -d --build
    ```

4.  **Acceder a la aplicación**:
    Abre tu navegador en: **`http://localhost:5173`**

---

## 🧪 Carga de Datos de Prueba (Seed)

El proyecto incluye un script de inicialización (`init_db.py`) dentro del contenedor del Gateway. Este script crea usuarios, se loguea para obtener tokens JWT reales y genera incidencias asociadas.

Una vez los contenedores estén corriendo (`healthy`), ejecuta:

```bash
docker compose exec gateway python init_db.py
```

### ¿Qué hace este script?

- Espera a que los servicios `users` e `incidents` estén saludables (Healthchecks).  
- Crea usuarios de prueba si no existen.  
- Genera incidencias asociadas a esos usuarios utilizando sus IDs reales.

## 📖 Documentación de la API (Swagger/OpenAPI)

Gracias a FastAPI, la documentación interactiva se genera automáticamente. En este entorno de desarrollo, se han expuesto los puertos de los microservicios para facilitar la depuración:

- **Gateway (BFF)**: http://localhost:8080/docs  
  - Ver aquí endpoints agregados como `/incidencias-detalladas`.
- **Desarrolladores**: Si necesitas acceder directamente a los Swagger de los microservicios individuales (users o incidents) para depuración, descomenta las líneas de ports en el archivo docker-compose.yml y reinicia los contenedores.

## 📂 Estructura del Proyecto

practica-dbcs-l07/ \
├── docker-compose.yml # Orquestación de todos los servicios \
├── .env # Variables de entorno centralizadas\
├── frontend/ # Aplicación Vue.js + Configuración Nginx\
├── gateway/ # BFF Pattern (incluye script init_db.py)\
├── users-service/ # Microservicio de Usuarios (App + DB Model)\
└── incidents-service/ # Microservicio de Incidencias (App + DB Model)

