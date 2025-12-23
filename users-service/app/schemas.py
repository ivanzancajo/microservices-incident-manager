from pydantic import BaseModel, EmailStr, Field

# 1. Definición base común
class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    
# 2. Esquema para creación (Input)
class UserCreate(UserBase):
    password: str = Field(min_length=4, description="Contraseña en texto plano")

# 3. Esquema para respuesta (Output)
class UserOut(UserBase):
    id: int

    # 4. Configuración Pydantic V2
    class Config:
        from_attributes = True