from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas, crud
from . import external

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Microservicio de Indicencias")

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

@app.get("/incidencias/{incident_id}", response_model=schemas.IncidentOut)
def get_incident_endpoint( incident_id:int, db: Session = Depends(get_db)):
    return crud.get_incident(db, incident_id)

@app.put("/incidencias/{incident_id}", response_model=schemas.IncidentOut)
def update_incident_endpoint( incident_id:int, payload: schemas.IncidentUpdate, db: Session = Depends(get_db)):
    return crud.update_incident(db, incident_id, payload)






