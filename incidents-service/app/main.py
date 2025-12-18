from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from . import models, schemas, crud
from . import external
from . import security

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Microservicio de Indicencias")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints de Incidencias ---

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/incidencias", response_model=schemas.IncidentOut, status_code=201)
def create_incident_endpoint(
    payload: schemas.IncidentCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(security.get_current_user_id) 
):
    payload.user_id = current_user_id
    
    # Ya no es estrictamente necesario validar si el usuario existe externamente, se podria eliminar esta linea
    external.validate_user_exists(payload.user_id)
    return crud.create_incident(db, payload)

@app.get("/incidencias", response_model=list[schemas.IncidentOut])
def list_incidents_endpoint(
    db: Session = Depends(get_db), 
    limit: int = Query(100, ge=1, le=1000), 
    offset: int = Query(0, ge=0)
):
    return crud.list_incidents(db, limit, offset)

@app.get("/incidencias/{incident_id}", response_model=schemas.IncidentOut)
def get_incident_endpoint( incident_id:int, db: Session = Depends(get_db)):
    return crud.get_incident(db, incident_id)

@app.delete("/incidencias/{incident_id}", status_code=204)
def delete_incident_endpoint(incident_id: int, db: Session = Depends(get_db)):
    crud.delete_incident(db, incident_id)
    return

@app.put("/incidencias/{incident_id}", response_model=schemas.IncidentOut)
def update_incident_endpoint( incident_id:int, payload: schemas.IncidentUpdate, db: Session = Depends(get_db)):
    return crud.update_incident(db, incident_id, payload)





