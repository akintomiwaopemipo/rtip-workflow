from datetime import date

from fastapi import APIRouter
from typing import List

from models.task import TaskState, TaskStatus, TaskType
from state.task_repo import get_all_tasks, save_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskState])
def get_tasks():
    save_task(TaskState(
        id="wf-2",
        workflow_instance_id="instance_1",
        case_file_version_id="version_1",
        type=TaskType.SUBMISSION_REVIEW,
        status=TaskStatus.IN_PROCESS,
        create_date=date.today(),
        due_date=date.today(),
        department_name="Underwriting",
        assigned_to_user="user1"
    ))
    return get_all_tasks()