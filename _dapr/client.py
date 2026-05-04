from dapr.ext.workflow import DaprWorkflowClient, DaprWorkflowContext
from typing import Any, Optional, Callable, Generator, TypeVar
from datetime import datetime

_client: DaprWorkflowClient = DaprWorkflowClient()

# Workflow function type
T = TypeVar("T")

WorkflowFn = Callable[
    [DaprWorkflowContext, Any],
    Generator[Any, Any, T]
]


def schedule_new_workflow(
    workflow: WorkflowFn[T],
    *,
    input: Any = None,
    instance_id: Optional[str] = None,
    start_at: Optional[datetime] = None,
) -> str:
    return _client.schedule_new_workflow(  # pyright: ignore[reportUnknownMemberType]
        workflow=workflow,
        input=input,
        instance_id=instance_id,
        start_at=start_at,
    )