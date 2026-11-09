from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.task_model import TaskModel
from app.domain.schemas import TaskCreate, TaskUpdate
from app.domain.enums import TaskStatus

class ITaskRepository(ABC):
    @abstractmethod
    def get_all_by_user(self, user_id: int, estado: Optional[TaskStatus] = None) -> List[TaskModel]:
        pass

    @abstractmethod
    def get_by_id_and_user(self, task_id: int, user_id: int) -> Optional[TaskModel]:
        pass

    @abstractmethod
    def get_next_delivery_by_user(self, user_id: int) -> Optional[TaskModel]:
        pass

    @abstractmethod
    def create(self, task_data: TaskCreate, user_id: int) -> TaskModel:
        pass

    @abstractmethod
    def update(self, task_model: TaskModel, task_data: TaskUpdate) -> TaskModel:
        pass

    @abstractmethod
    def delete(self, task_model: TaskModel) -> None:
        pass
