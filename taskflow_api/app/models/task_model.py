from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SqlEnum
from datetime import datetime, timezone
from app.core.config import Base
from app.domain.enums import TaskStatus
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    titulo = Column(String(150), nullable=False)
    materia = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_entrega = Column(DateTime, nullable=False, index=True)
    estado = Column(SqlEnum(TaskStatus), default=TaskStatus.PENDIENTE, nullable=False)
    prioridad = Column(Integer, nullable=False, default=2)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("UserModel", back_populates="tasks")
