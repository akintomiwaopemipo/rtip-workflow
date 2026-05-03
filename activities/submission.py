from typing import Any

from dapr.ext.workflow import WorkflowActivityContext

from decorators import activity
from services.broker import get_submission as get_submission_service


@activity("get_submission")
async def get_submission(
    ctx: WorkflowActivityContext,
    payload: dict[str, Any]
) -> dict[str, Any]:
    return await get_submission_service(payload["caseFileVersionId"])