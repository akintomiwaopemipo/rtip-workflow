from typing import Any

from fastapi import APIRouter
from _dapr.client import schedule_new_workflow

from workflows.broker_workflow import broker_workflow


router = APIRouter(prefix="/workflow", tags=["Workflow"])


@router.post("/start")
async def start_workflow(payload: dict[str, Any]):
    instance_id: str = schedule_new_workflow(
        workflow=broker_workflow,
        input=payload
    )

    return {"instance_id": instance_id}