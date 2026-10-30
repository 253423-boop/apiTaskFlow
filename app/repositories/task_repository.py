from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.repositories.base_repository import ITaskRepository
from app.models.task_model import TaskModel
from app.domain.schemas import TaskCreate, TaskUpdate
from app.domain.enums import TaskStatus

class SqlAlchemyTaskRepository(ITaskRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, estado: Optional[TaskStatus] = None) -> List[TaskModel]:
        query = self.db.query(TaskModel)
        if estado is not None:
            query = query.filter(TaskModel.estado == estado)
        return query.order_by(TaskModel.fecha_entrega.asc()).all()

    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        return self.db.query(TaskModel).filter(TaskModel.id == task_id).first()

    def get_next_delivery(self) -> Optional[TaskModel]:
        """
        Obtiene la tarea pendiente cuya fecha de entrega sea la más cercana (futura o actual).
        Si no hay futuras, devuelve la pendiente más próxima por entregar.
        """
        now = datetime.now()
        next_task = (
            self.db.query(TaskModel)
            .filter(TaskModel.estado == TaskStatus.PENDIENTE, TaskModel.fecha_entrega >= now)
            .order_by(TaskModel.fecha_entrega.asc())
            .first()
        )
        # Fallback: si todas las pendientes están vencidas, muestra la pendiente más urgente
        if not next_task:
            next_task = (
                self.db.query(TaskModel)
                .filter(TaskModel.estado == TaskStatus.PENDIENTE)
                .order_by(TaskModel.fecha_entrega.asc())
                .first()
            )
        return next_task

    def create(self, task_data: TaskCreate) -> TaskModel:
        new_task = TaskModel(**task_data.model_dump())
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update(self, task_model: TaskModel, task_data: TaskUpdate) -> TaskModel:
        update_dict = task_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(task_model, key, value)
        self.db.commit()
        self.db.refresh(task_model)
        return task_model

    def delete(self, task_model: TaskModel) -> None:
        self.db.delete(task_model)
        self.db.commit()