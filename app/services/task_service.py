from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.base_repository import ITaskRepository
from app.domain.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.domain.enums import TaskStatus

class TaskService:

    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def list_tasks(self, estado: Optional[TaskStatus] = None) -> List[TaskResponse]:
        tasks = self.repository.get_all(estado=estado)
        return [TaskResponse.model_validate(t) for t in tasks]

    def get_task_detail(self, task_id: int) -> TaskResponse:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La tarea con ID {task_id} no fue encontrada."
            )
        return TaskResponse.model_validate(task)

    def get_upcoming_task(self) -> Optional[TaskResponse]:
        task = self.repository.get_next_delivery()
        if not task:
            return None
        return TaskResponse.model_validate(task)

    def create_task(self, task_data: TaskCreate) -> TaskResponse:
        created = self.repository.create(task_data)
        return TaskResponse.model_validate(created)

    def update_task(self, task_id: int, task_data: TaskUpdate) -> TaskResponse:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La tarea con ID {task_id} no fue encontrada."
            )
        updated = self.repository.update(task, task_data)
        return TaskResponse.model_validate(updated)

    def complete_task(self, task_id: int) -> TaskResponse:
        """Caso de uso directo para el botón 'Marcar como completada' usando PUT."""
        return self.update_task(task_id, TaskUpdate(estado=TaskStatus.COMPLETADA))

    def delete_task(self, task_id: int) -> None:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La tarea con ID {task_id} no fue encontrada."
            )
        self.repository.delete(task)