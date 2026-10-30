from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.repositories.base_repository import ITaskRepository
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.services.task_service import TaskService

def get_task_repository(db: Session = Depends(get_db)) -> ITaskRepository:
    return SqlAlchemyTaskRepository(db)

def get_task_service(repo: ITaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(repo)