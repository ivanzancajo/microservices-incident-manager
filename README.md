# practica-dbcs-l07

# Documentación técnica (Contraseñas necesarias)

Este documento lista las variables de entorno que **deben configurarse en el archivo `.env`** para que la aplicación funcione correctamente.

## Variables de entorno archivo .env

| Variable | Servicio | Descripción | Valor Configurado | 
| ----- | ----- | ----- | ----- | 
| `POSTGRES_USER` | BD | Usuario de PostgreSQL. | **`L07`** | 
| `POSTGRES_PASSWORD` | BD | Contraseña de la Base de Datos. | **`passL07`** | 
| `POSTGRES_DB` | BD | Nombre de la base de datos. | **`incidents_db`** | 
| `DB_USER` | Backend | Referencia a `POSTGRES_USER`. | `${POSTGRES_USER}` | 
| `DB_PASSWORD` | Backend | Referencia a `POSTGRES_PASSWORD`. | `${POSTGRES_PASSWORD}` | 
| `DB_NAME` | Backend | Referencia a `POSTGRES_DB`. | `${POSTGRES_DB}` | 
| `DB_HOST` | Backend | Host interno (nombre del servicio Docker). | `db` | 
| `DB_PORT` | Backend | Puerto interno de la BD. | `5432` |
| `VITE_API_URL` | Frontend | URL de conexion con el backend | `/api` |  

## Puertos 
| Servicio | Descripción | Puerto | 
| ----- | ----- | ----- | 
| Backend | Puerto externo de FastAPI. | `8000` | 
|  Frontend | Puerto externo de Vue.js. | `5173` | 


