from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
# Usamos importación relativa porque estos archivos están en el mismo paquete 'app'
from . import models, schemas

def create_user(db: Session, data: schemas.UserCreate):
    # Verificamos si ya existe el email
    if db.scalar(select(models.User).where(models.User.email == data.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email ya registrado"
        )
    
    # Creamos la instancia del modelo
    user = models.User(name=data.name, email=data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session, limit: int = 100, offset: int = 0):
    stmt = select(models.User).offset(offset).limit(limit)
    return list(db.scalars(stmt).all())