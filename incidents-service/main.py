from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas, crud

# Crear las tablas de la BD de Incidencias al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio de Incidencias")

# Middleware CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints de Incidencias ---

@app.post("/incidencias", response_model=schemas.IncidentOut, status_code=201)
def create_incident_endpoint(payload: schemas.IncidentCreate, db: Session = Depends(get_db)):
    return crud.create_incident(db, payload)

@app.get("/incidencias", response_model=list[schemas.IncidentOut])
def list_incidents_endpoint(
    db: Session = Depends(get_db), 
    limit: int = Query(100, ge=1, le=1000), 
    offset: int = Query(0, ge=0)
):
    return crud.list_incidents(db, limit, offset)

@app.delete("/incidencias/{incident_id}", status_code=204)
def delete_incident_endpoint(incident_id: int, db: Session = Depends(get_db)):
    crud.delete_incident(db, incident_id)
    return
