import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 1. Recuperamos las variables (Mantén los nombres genéricos)
# Docker se encargará de asignar aquí los valores de la BD de usuarios
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 2. Construimos la URL
# Usamos postgresql+psycopg para aprovechar el driver moderno que tienes en requirements
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Validación básica (Mejorada)
# Verificar componentes individuales es más seguro que verificar la URL completa construida
if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
   # Esto lanzará error si falta alguna variable crítica, evitando conexiones a "None"
   print("Advertencia: Faltan variables de entorno para la base de datos.")

# 4. Definición de Base para SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# 5. Creación del Engine
# pool_pre_ping=True ayuda a recuperar conexiones perdidas silenciosamente
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 6. SessionLocal
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 7. Dependencia para inyección en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()