from dapr.clients import DaprClient
from typing import Optional, List
import json

from pydantic import ValidationError

from models.state import StateType
from models.task import TaskState

STATE_STORE_NAME = "statestore"


def save_task(task: TaskState) -> None:
    with DaprClient() as client:
        client.save_state(
            store_name=STATE_STORE_NAME,
            key=f"task:{task.id}",
            value=task.model_dump_json(),
            state_metadata={"contentType": "application/json"}
        )


def get_task(task_id: str) -> Optional[TaskState]:
    with DaprClient() as client:
        resp = client.get_state(
            store_name=STATE_STORE_NAME,
            key=f"task:{task_id}",
        )

        if not resp.data:
            return None

        return TaskState(**json.loads(resp.data))


def add_task_to_workflow(instance_id: str, task_id: str) -> None:
    with DaprClient() as client:
        key = f"workflow:{instance_id}:tasks"

        resp = client.get_state(STATE_STORE_NAME, key)
        task_ids: List[str] = json.loads(resp.data) if resp.data else []

        task_ids.append(task_id)

        client.save_state(STATE_STORE_NAME, key, json.dumps(task_ids))




def get_workflow_tasks(instance_id: str) -> List[TaskState]:
    with DaprClient() as client:
        key = f"workflow:{instance_id}:tasks"

        resp = client.get_state(STATE_STORE_NAME, key)
        task_ids: List[str] = json.loads(resp.data) if resp.data else []

    return [t for t in (get_task(tid) for tid in task_ids) if t is not None]


def get_all_tasks() -> List[TaskState]:
    with DaprClient() as client:
        resp = client.query_state(
            store_name=STATE_STORE_NAME,
            query=json.dumps({
                "filter": {
                    "EQ": {"state_type": StateType.TASK}
                }
            })
        )

    
    tasks: list[TaskState] = []

    for item in resp.results:
        try:
            task = TaskState.model_validate(json.loads(item.value))
            tasks.append(task)
        except ValidationError:
            continue

    return tasks