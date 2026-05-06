from typing import Any

from dapr.ext.workflow import WorkflowActivityContext

from services.broker import decline
from decorators import activity


@activity("decline_submission")
def decline_submission(
    ctx: WorkflowActivityContext,
    payload: dict[str, Any]
) -> dict[str, Any]:
    return decline(payload["caseFileVersionId"])