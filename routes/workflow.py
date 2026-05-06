from typing import Any

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from _dapr.client import schedule_new_workflow
from dapr.ext.workflow import DaprWorkflowClient
from workflows.broker_workflow import broker_workflow


router = APIRouter(prefix="/workflow", tags=["Workflow"])


@router.post("/start")
async def start_workflow(payload: dict[str, Any]):
 
    instance_id: str = schedule_new_workflow(
        workflow=broker_workflow,
        input=payload
    )

    return {"instance_id": instance_id}


@router.post("/failure-details/{instance_id}", response_class=PlainTextResponse)
async def get_failure_details(instance_id: str):
    client = DaprWorkflowClient()
    workflow_state = client.get_workflow_state(instance_id=instance_id)
    obj = getattr(workflow_state, "_WorkflowState__obj", None)
    failure: object = getattr(obj, "failure_details", {})

    error_message = "Message: " + getattr(failure, "_message", "N/A")
    error_message += "\n\n" + "Type: " + getattr(failure, "_error_type", "N/A")
    error_message += "\n\n" + "Stack Trace:" + "\n" + getattr(failure, "_stack_trace", "N/A")
    error_message += "\n\n"

    return error_message
    


@router.post("/state/{instance_id}")
async def get_workflow_state(instance_id: str):
    client = DaprWorkflowClient()
    state = client.get_workflow_state(instance_id=instance_id)
    return {"state": state}