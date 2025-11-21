from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
# Nota: Importamos Base desde .database (el archivo que creamos en el paso anterior)
from .database import Base 

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)