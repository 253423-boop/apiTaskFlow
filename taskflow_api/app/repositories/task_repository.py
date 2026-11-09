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

    def get_all_by_user(self, user_id: int, estado: Optional[TaskStatus] = None) -> List[TaskModel]:
        query = self.db.query(TaskModel).filter(TaskModel.user_id == user_id)
        if estado is not None:
            query = query.filter(TaskModel.estado == estado)
        return query.order_by(TaskModel.fecha_entrega.asc(), TaskModel.prioridad.desc()).all()

    def get_by_id_and_user(self, task_id: int, user_id: int) -> Optional[TaskModel]:
        return self.db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()

    def get_next_delivery_by_user(self, user_id: int) -> Optional[TaskModel]:
        now = datetime.now()
        next_task = (
            self.db.query(TaskModel)
            .filter(TaskModel.user_id == user_id, TaskModel.estado == TaskStatus.PENDIENTE, TaskModel.fecha_entrega >= now)
            .order_by(TaskModel.fecha_entrega.asc())
            .first()
        )
        if not next_task:
            next_task = (
                self.db.query(TaskModel)
                .filter(TaskModel.user_id == user_id, TaskModel.estado == TaskStatus.PENDIENTE)
                .order_by(TaskModel.fecha_entrega.asc())
                .first()
            )
        return next_task

    def create(self, task_data: TaskCreate, user_id: int) -> TaskModel:
        new_task = TaskModel(**task_data.model_dump(), user_id=user_id)
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
