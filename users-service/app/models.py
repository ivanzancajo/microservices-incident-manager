from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from .database import Base 

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    # Guardamos el hash, no la contraseña real. String(255) es suficiente para bcrypt.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)