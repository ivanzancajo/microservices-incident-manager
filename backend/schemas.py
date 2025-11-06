from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    
class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int

class IncidentBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
    status: str = Field(min_length=1, max_length=50)

class IncidentCreate(IncidentBase):
    id_user: int

class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    status: str | None = Field(default=None, min_length=1, max_length=50)

class IncidentOut(IncidentBase):
    id: int
    id_user: int

    class Config:
        orm_mode = True
