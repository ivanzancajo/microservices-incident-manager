from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from . import models, schemas

def create_incident(db: Session, data: schemas.IncidentCreate, user_id: int):
    # Verificamos si ya existe un incidente con el mismo título
    if db.scalar(select(models.Incident).where(models.Incident.title == data.title)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incidente con este título ya existe"
        )
    
    # Creamos la instancia del modelo usando los datos del esquema + el user_id seguro
    incident = models.Incident(
        title=data.title, 
        description=data.description,
        status=data.status, # Aseguramos que se pasa el status (por defecto abierta)
        user_id=user_id     # <--- AQUÍ VINCULAMOS LA AUTORÍA
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

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
    if data.user_id is not None:
        incident.user_id = data.user_id

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
