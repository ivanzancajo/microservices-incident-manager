from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importaciones relativas (Crucial para que funcione dentro del paquete 'app')
from .database import Base, engine, get_db
from . import models, schemas, crud

# Crear las tablas de la BD de Usuarios al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio de Usuarios")

# Middleware CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "users-service"}

# --- Endpoints de Usuarios ---

@app.post("/usuarios", response_model=schemas.UserOut, status_code=201)
def create_user_endpoint(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)