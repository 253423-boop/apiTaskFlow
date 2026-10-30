from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from app.domain.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.domain.enums import TaskStatus
from app.services.task_service import TaskService
from app.api.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["Tareas"])

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar tarea (CREATE)"
)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
):
    """Crea una nueva actividad académica. El estado es 'pendiente' por defecto."""
    return service.create_task(task_data)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Consultar y filtrar tareas (READ)"
)
def get_tasks(
    estado: Optional[TaskStatus] = Query(
        None,
        description="Filtrar por estado: 'pendiente' o 'completada'. Si se omite, devuelve todas."
    ),
    service: TaskService = Depends(get_task_service)
):
    """
    Sirve para la Pantalla 2 (Mis tareas).
    Permite aplicar los filtros: Todas (sin parámetro), Pendientes y Completadas.
    """
    return service.list_tasks(estado=estado)


@router.get(
    "/proxima-entrega",
    response_model=Optional[TaskResponse],
    summary="Consultar próxima entrega (READ - Pantalla Inicio)"
)
def get_next_delivery(
    service: TaskService = Depends(get_task_service)
):
    """
    Sirve para la tarjeta de 'Próxima entrega' en la Pantalla 1 (Inicio).
    Devuelve la tarea pendiente con la fecha de entrega más cercana o null si no hay pendientes.
    """
    return service.get_upcoming_task()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Detalle de tarea (READ - Pantalla Detalle)"
)
def get_task_by_id(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Obtiene la información completa de una tarea para la Pantalla 4."""
    return service.get_task_detail(task_id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Editar o completar tarea (UPDATE)"
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
):
    """
    Modifica la información de una actividad (Pantalla 3) o actualiza su estado a 'completada'.
    """
    return service.update_task(task_id, task_data)


@router.put(
    "/{task_id}/completar",
    response_model=TaskResponse,
    summary="Marcar tarea como completada (UPDATE directo)"
)
def mark_task_as_completed(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Atajo semántico con método PUT para el botón 'Marcar como completada' de la Pantalla 4."""
    return service.complete_task(task_id)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar tarea (DELETE)"
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    """Elimina una actividad de la base de datos tras la confirmación en la app móvil."""
    service.delete_task(task_id)
    return None