from datetime import date
import json
from typing import Any
from uuid import uuid4

from dapr.ext.workflow import WorkflowActivityContext

from decorators import activity
from models.task import TaskState, TaskStatus, TaskType
from services.broker import submit
from state.task_repo import get_task, save_task


@activity(name="broker_submission")
async def broker_submission(
    ctx: WorkflowActivityContext,
    payload: dict[str, Any]
) -> dict[str, Any]:
    return await submit(payload)


@activity("create_task")
async def create_task(
    ctx: WorkflowActivityContext,
    input: dict[str, Any] 
):
    task = TaskState(
        id=str(uuid4()),
        workflow_instance_id=input["workflow_instance_id"],
        case_file_version_id="",
        type=TaskType.SUBMISSION_REVIEW,
        status=TaskStatus.IN_PROCESS,
        create_date=date.today(),
        due_date=date.today(),
        department_name="Underwriting",
        assigned_to_user="system",
    )

    save_task(task)
    return task.id





@activity("update_task_after_submission")
async def update_task_after_submission(
        ctx: WorkflowActivityContext,
        input: dict[str, Any] 
):
    task = get_task(input["task_id"])

    if task is None:
        raise ValueError(f"Task not found: {input['task_id']}")

    task.case_file_version_id = input["case_file_version_id"]
    task.response = json.dumps(input["response"])
    task.data = {
        "premium": input["response"].get("premium"),
        "totalDue": input["response"].get("totalDue"),
    }

    save_task(task)



@activity("complete_task")
async def complete_task(
    ctx: WorkflowActivityContext,
    input: dict[str, Any] 
):
    task = get_task(input["task_id"])
    if task is None:
        raise ValueError(f"Task not found: {input['task_id']}")
    task.status = TaskStatus.COMPLETED
    task.decision = input["decision"]
    task.decision_type = input["decision_type"]
    task.complete_date = date.today()

    save_task(task)