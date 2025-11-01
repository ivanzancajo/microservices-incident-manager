from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import Base, engine, get_db
import models, schemas, crud

Base.metadata.create_all(bind=engine) # Inicializa la base de datos
app = FastAPI(title="Servicio de Usuarios con Persistencia")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)