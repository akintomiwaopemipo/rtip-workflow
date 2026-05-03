from typing import Any

from dapr.ext.workflow import WorkflowActivityContext

from decorators import activity
from services.broker import submit


@activity(name="broker_submission")
async def broker_submission(
    ctx: WorkflowActivityContext,
    payload: dict[str, Any]
) -> dict[str, Any]:
    return await submit(payload)



