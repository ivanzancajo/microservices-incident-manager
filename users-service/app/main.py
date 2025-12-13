from fastapi import FastAPI, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importaciones relativas (Crucial para que funcione dentro del paquete 'app')
from .database import Base, engine, get_db
from . import models, schemas, crud, security

# Crear las tablas de la BD de Usuarios al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio de Usuarios")

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

@app.post("/usuarios", response_model=schemas.UserOut, status_code=201)
def create_user_endpoint(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload)

@app.get("/usuarios", response_model=list[schemas.UserOut])
def list_users_endpoint(
    db: Session = Depends(get_db), 
    limit: int = Query(100, ge=1, le=1000), 
    offset: int = Query(0, ge=0)
):
    return crud.list_users(db, limit, offset)

@app.get("/usuarios/{user_id}", response_model=schemas.UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

@app.delete("/usuarios/{user_id}", status_code=204)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    # Nota: Con status_code=204, no se debe retornar contenido en el body.
    return


#Endpoint interno para el Gateway.
#Devuelve los datos completos de los usuarios solicitados por sus IDs.
@app.post("/usuarios/batch", response_model=list[schemas.UserOut])
def get_users_batch(user_ids: list[int], db: Session = Depends(get_db)): 
    return crud.get_users_by_ids(db, user_ids)

@app.post("/auth/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Buscamos al usuario por email (el formulario usa 'username' genérico)
    user = crud.get_user_by_email(db, email=form_data.username)
    
    # 2. Verificamos si el usuario existe y si la contraseña coincide
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Si todo es correcto, generamos el Token JWT
    # Guardamos el ID (sub) y el email en el token
    access_token = security.create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )
    
    # 4. Devolvemos el token
    return {"access_token": access_token, "token_type": "bearer"}