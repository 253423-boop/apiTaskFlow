from pydantic import BaseModel, Field, EmailStr, computed_field, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.enums import TaskStatus

# --- Schemas de Usuario (Auth) ---
class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    correo: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# --- Schemas de Tareas ---
class TaskBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    materia: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    fecha_entrega: datetime
    estado: TaskStatus = Field(default=TaskStatus.PENDIENTE)
    prioridad: int = Field(default=2, ge=1, le=3, description="Prioridad: 1=Baja, 2=Media, 3=Alta")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=150)
    materia: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    fecha_entrega: Optional[datetime] = None
    estado: Optional[TaskStatus] = None
    prioridad: Optional[int] = Field(None, ge=1, le=3)

class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    @computed_field
    @property
    def vencida(self) -> bool:
        now = datetime.now(self.fecha_entrega.tzinfo)
        return self.estado == TaskStatus.PENDIENTE and self.fecha_entrega < now

    model_config = ConfigDict(from_attributes=True)
