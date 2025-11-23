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
    return {"status": "ok"}

@app.post("/usuarios", response_model=schemas.UserOut, status_code=201)
def create_user_endpoint(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)

@app.get("/usuarios", response_model=list[schemas.UserOut])
def list_users_endpoint(
    db: Session = Depends(get_db), 
    limit: int = Query(100, ge=1, le=1000), 
    offset: int = Query(0, ge=0)
):
    return crud.list_users(db, limit, offset)

@app.get("/usuarios/{user_id}", response_model=schemas.UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

@app.delete("/usuarios/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    # Nota: Con status_code=204, no se debe retornar contenido en el body.
    return