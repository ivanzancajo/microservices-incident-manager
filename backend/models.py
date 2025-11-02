from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    incidents = relationship("Incident", back_populates="owner")


class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    id_user =  mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="incidents") 