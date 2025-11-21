from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
import models, schemas

def create_user(db: Session, data: schemas.UserCreate):
    if db.scalar(select(models.User).where(models.User.email == data.email)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    user = models.User(name=data.name, email=data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session, limit: int = 100, offset: int = 0):
    stmt = select(models.User).offset(offset).limit(limit)
    return list(db.scalars(stmt).all())

def get_user(db: Session, user_id: int):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()

def create_incident(db: Session, data: schemas.IncidentCreate):
    user = get_user(db, data.id_user)
    incident = models.Incident(title=data.title, description=data.description, status=data.status, owner=user)
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

def list_incidents(db: Session, limit: int = 100, offset: int = 0):
    stmt = select(models.Incident).offset(offset).limit(limit)
    return list(db.scalars(stmt).all())

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

def delete_incident(db: Session, incident_id: int):
    incident = get_incident(db, incident_id)
    db.delete(incident)
    db.commit()