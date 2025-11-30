# Sistema de Gestión de Incidencias (Arquitectura de Microservicios)

Este proyecto implementa una plataforma completa para la gestión de usuarios e incidencias, migrada desde una arquitectura monolítica a una arquitectura de microservicios contenerizada. El sistema ha sido diseñado siguiendo principios de desacoplamiento, escalabilidad y aislamiento de datos (Database per Service), utilizando un API Gateway (BFF) para orquestar la comunicación con el Frontend.

## 🚀 Arquitectura y Tecnologías

El sistema se compone de los siguientes contenedores orquestados mediante Docker Compose:

| Servicio          | Tecnología           | Descripción                                                                 | Puerto (Host) |
|------------------|----------------------|-----------------------------------------------------------------------------|---------------|
| Frontend         | Vue.js 3 + Nginx     | Interfaz de usuario (SPA). Nginx actúa también como Reverse Proxy.         | 5173          |
| BFF Gateway      | Python (FastAPI)     | Backend for Frontend. Agrega datos de usuarios e incidencias para el cliente. | 8080       |
| Users Service    | Python (FastAPI)     | Microservicio de gestión de usuarios. Base de datos propia (PostgreSQL).   | 8001          |
| Incidents Service| Python (FastAPI)     | Microservicio de gestión de incidencias. Base de datos propia (PostgreSQL).| 8002          |
| Databases        | PostgreSQL 15        | Dos instancias independientes (users-db, incidents-db).                    | Interno       |

### Características Clave

- **Database per Service**: Aislamiento estricto de datos. No hay claves foráneas entre dominios.
- **API Composition**: El Gateway “hidrata” las respuestas combinando datos de múltiples servicios en memoria.
- **Resiliencia**: Manejo de usuarios eliminados (“Usuario no encontrado”) sin romper la integridad de las incidencias históricas.
- **Red Interna**: Los servicios se comunican a través de una red bridge (`app-network`), exponiendo solo lo necesario.

## 🛠️ Instalación y Despliegue

### Requisitos Previos

- Docker Engine  
- Docker Compose (v2)  
- Puerto `5173` libre en tu máquina  

### Pasos

1. **Clonar el repositorio**:

git clone https://gitlab.inf.uva.es/diegveg/practica-dbcs-l07.git
cd practica-dbcs-l07


2. **Configurar variables de entorno**  
Copia el archivo de ejemplo y ajústalo si es necesario (la configuración por defecto funciona *out of the box*).

cp .env.example .env


3. **Construir y arrancar los servicios**:

docker compose up -d --build


4. **Acceder a la aplicación**  
Abre tu navegador en:  
`http://localhost:5173`

## 🧪 Carga de Datos de Prueba (Seed)

El proyecto incluye un script de inicialización (`init_db.py`) alojado en el Gateway. Este script permite poblar las bases de datos con usuarios e incidencias ficticias para verificar que la comunicación entre microservicios funciona correctamente.

Con los contenedores corriendo, ejecuta:

docker compose exec gateway python init_db.py


### ¿Qué hace este script?

- Espera a que los servicios `users` e `incidents` estén saludables (Healthchecks).  
- Crea usuarios de prueba si no existen.  
- Genera incidencias asociadas a esos usuarios utilizando sus IDs reales.

## 📖 Documentación de la API (Swagger/OpenAPI)

Gracias a FastAPI, la documentación interactiva se genera automáticamente. En este entorno de desarrollo, se han expuesto los puertos de los microservicios para facilitar la depuración:

- **Gateway (BFF)**: http://localhost:8080/docs  
  - Ver aquí endpoints agregados como `/incidencias-detalladas`.
- **Users Service**: http://localhost:8001/docs  
  - Gestión CRUD directa de usuarios.
- **Incidents Service**: http://localhost:8002/docs  
  - Gestión CRUD directa de incidencias.

## 📂 Estructura del Proyecto

practica-dbcs-l07/
├── docker-compose.yml # Orquestación de todos los servicios
├── .env # Variables de entorno centralizadas
├── frontend/ # Aplicación Vue.js + Configuración Nginx
├── gateway/ # BFF Pattern (incluye script init_db.py)
├── users-service/ # Microservicio de Usuarios (App + DB Model)
└── incidents-service/ # Microservicio de Incidencias (App + DB Model)


## 👥 Autores

- Daniel Fernández García  
- Diego Vegas Losada  
- Iván Zancajo Arenas  

**Grupo L07 - Curso 2025/2026**
