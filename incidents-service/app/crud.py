from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
import models, schemas

def create_incident(db: Session, data: schemas.IncidentCreate):
    # Verificamos si ya existe un incidente con el mismo título
    if db.scalar(select(models.Incident).where(models.Incident.title == data.title)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incidente con este título ya existe"
        )
    
    # Creamos la instancia del modelo
    incident = models.Incident(
        title=data.title, 
        description=data.description, 
        severity=data.severity
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

def list_incidents(db: Session, limit: int = 100, offset: int = 0):
    stmt = select(models.Incident).offset(offset).limit(limit)
    return list(db.scalars(stmt).all())

def delete_incident(db: Session, incident_id: int):
    incident = db.get(models.Incident, incident_id)
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Incidente no encontrado"
        )
    db.delete(incident)
    db.commit()