from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SqlEnum
from datetime import datetime, timezone
from app.core.config import Base
from app.domain.enums import TaskStatus

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    materia = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)  # No obligatorio según especificación
    fecha_entrega = Column(DateTime, nullable=False, index=True)
    estado = Column(SqlEnum(TaskStatus), default=TaskStatus.PENDIENTE, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))