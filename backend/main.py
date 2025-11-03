from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import Base, engine, get_db
import models, schemas, crud

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Servicio de Usuarios con Persistencia")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuarios", response_model=schemas.UserOut, status_code=201)
def create_user_endpoint(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)

@app.get("/usuarios", response_model=list[schemas.UserOut])
def list_users_endpoint( db: Session = Depends(get_db), limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    return crud.list_users(db, limit, offset)

@app.get("/usuarios/{user_id}", response_model=schemas.UserOut)
def get_user_endpoint( user_id:int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

@app.delete("/usuarios/{user_id}", status_code=204)
def delete_user_endpoint( user_id:int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"ok": True}

# Endpoints Incidentes

@app.post("/incidentes", response_model=schemas.IncidentOut, status_code=201)
def create_incident_endpoint(payload: schemas.IncidentCreate, db: Session = Depends(get_db)):
    return crud.create_incident(db, payload)

@app.get("/incidentes", response_model=list[schemas.IncidentOut])
def list_incidents_endpoint( db: Session = Depends(get_db), limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    return crud.list_incidents(db, limit, offset)

@app.get("/incidentes/{incident_id}", response_model=schemas.IncidentOut)
def get_incident_endpoint( incident_id:int, db: Session = Depends(get_db)):
    return crud.get_incident(db, incident_id)

@app.put("/incidentes/{incident_id}", response_model=schemas.IncidentOut)
def update_incident_endpoint( incident_id:int, payload: schemas.IncidentUpdate, db: Session = Depends(get_db)):
    return crud.update_incident(db, incident_id, payload)

@app.delete("/incidentes/{incident_id}", status_code=204)
def delete_incident_endpoint( incident_id:int, db: Session = Depends(get_db)):
    crud.delete_incident(db, incident_id)
    return {"ok": True}



