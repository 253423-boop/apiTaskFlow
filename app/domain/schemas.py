from pydantic import BaseModel, Field, computed_field, ConfigDict
from typing import Optional
from datetime import datetime
from app.domain.enums import TaskStatus

class TaskBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150, description="Título obligatorio de la tarea")
    materia: str = Field(..., min_length=1, max_length=100, description="Nombre libre de la materia")
    descripcion: Optional[str] = Field(None, description="Descripción opcional de la actividad")
    fecha_entrega: datetime = Field(..., description="Fecha y hora límite de entrega")
    estado: TaskStatus = Field(default=TaskStatus.PENDIENTE, description="Pendiente por defecto")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    """Permite editar toda la tarea o únicamente cambiar su estado a completada mediante PUT."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=150)
    materia: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    fecha_entrega: Optional[datetime] = None
    estado: Optional[TaskStatus] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    @computed_field
    @property
    def vencida(self) -> bool:
        """
        Detecta automáticamente si la actividad está vencida:
        Solo está vencida si sigue 'pendiente' y la fecha_entrega es menor a la fecha actual.
        """
        now = datetime.now(self.fecha_entrega.tzinfo)
        return self.estado == TaskStatus.PENDIENTE and self.fecha_entrega < now

    model_config = ConfigDict(from_attributes=True)