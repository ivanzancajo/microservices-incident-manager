from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
import models, schemas

def get_incident(db: Session, incident_id: int):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incidente no encontrado")
    return incident

def update_incident(db: Session, incident_id: int, data: schemas.IncidentUpdate):
    incident = get_incident(db, incident_id)
    if data.title is not None:
        incident.title = data.title
    if data.description is not None:
        incident.description = data.description
    if data.status is not None:
        incident.status = data.status
    db.commit()
    db.refresh(incident)
    return incident

