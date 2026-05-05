
from fastapi import APIRouter
from typing import List

from models.task import TaskState
from state.task_repo import get_all_tasks

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskState])
def get_tasks():
    return get_all_tasks()