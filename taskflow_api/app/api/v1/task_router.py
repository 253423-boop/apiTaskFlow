from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.domain.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.domain.enums import TaskStatus
from app.services.task_service import TaskService
from app.api.dependencies import get_task_service
from app.core.security import get_current_user
from app.models.user_model import UserModel

router = APIRouter(prefix="/tasks", tags=["Tareas"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    return service.create_task(task_data, current_user.id)

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    estado: Optional[TaskStatus] = Query(None),
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    return service.list_tasks(current_user.id, estado=estado)

@router.get("/proxima-entrega", response_model=Optional[TaskResponse])
def get_next_delivery(
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    return service.get_upcoming_task(current_user.id)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    return service.get_task_detail(task_id, current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    return service.update_task(task_id, current_user.id, task_data)

@router.put("/{task_id}/completar", response_model=TaskResponse)
def mark_task_as_completed(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    return service.update_task(task_id, current_user.id, TaskUpdate(estado=TaskStatus.COMPLETADA))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: UserModel = Depends(get_current_user)
):
    service.delete_task(task_id, current_user.id)
    return None
