from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

# Usamos importación relativa porque estos archivos están en el mismo paquete 'app'
from . import models, schemas, security


def create_user(db: Session, data: schemas.UserCreate):
    # Verificamos si ya existe el email
    if db.scalar(select(models.User).where(models.User.email == data.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado"
        )

    #Generamos el hash de la contraseña recibida
    hashed_pwd = security.get_password_hash(data.password)

    #Creamos el usuario guardando el hash, NO la contraseña plana
    user = models.User(
        name=data.name, 
        email=data.email, 
        password_hash=hashed_pwd 
    )
    # -------------------------

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return user


def delete_user(db: Session, user_id: int):
    # Reutilizamos get_user para asegurar que existe o lanzar 404
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()

# Recupera una lista de usuarios basada en una lista de IDs.
# Útil para operaciones en bloque (batch) desde el Gateway.
def get_users_by_ids(db: Session, user_ids: list[int]):
    stmt = select(models.User).where(models.User.id.in_(user_ids))
    return list(db.scalars(stmt).all())
