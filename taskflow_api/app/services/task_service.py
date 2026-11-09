from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.base_repository import ITaskRepository
from app.domain.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.domain.enums import TaskStatus

class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def list_tasks(self, user_id: int, estado: Optional[TaskStatus] = None) -> List[TaskResponse]:
        tasks = self.repository.get_all_by_user(user_id, estado=estado)
        return [TaskResponse.model_validate(t) for t in tasks]

    def get_task_detail(self, task_id: int, user_id: int) -> TaskResponse:
        task = self.repository.get_by_id_and_user(task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o no te pertenece.")
        return TaskResponse.model_validate(task)

    def get_upcoming_task(self, user_id: int) -> Optional[TaskResponse]:
        task = self.repository.get_next_delivery_by_user(user_id)
        if not task:
            return None
        return TaskResponse.model_validate(task)

    def create_task(self, task_data: TaskCreate, user_id: int) -> TaskResponse:
        created = self.repository.create(task_data, user_id)
        return TaskResponse.model_validate(created)

    def update_task(self, task_id: int, user_id: int, task_data: TaskUpdate) -> TaskResponse:
        task = self.repository.get_by_id_and_user(task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o no te pertenece.")
        updated = self.repository.update(task, task_data)
        return TaskResponse.model_validate(updated)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.repository.get_by_id_and_user(task_id, user_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada o no te pertenece.")
        self.repository.delete(task)
