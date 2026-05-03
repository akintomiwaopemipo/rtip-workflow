from typing import Any, Generator
from dapr.ext.workflow import DaprWorkflowContext

from activities.broker import broker_submission
from activities.decline import decline_submission
from activities.submission import get_submission
from decorators import workflow




@workflow("broker_workflow")
def broker_workflow(ctx: DaprWorkflowContext, payload: Any) -> Generator[Any, Any, Any]:

    result = yield ctx.call_activity(broker_submission, input = payload)

    case_file_version_id = result["caseFileVersionId"]
    violations = result.get("guidelinesViolations", [])

    if not violations:
        return (yield ctx.call_activity(
            get_submission,
            input = {"caseFileVersionId": case_file_version_id}
        ))
    else:
        return (yield ctx.call_activity(
            decline_submission,
            input = {"caseFileVersionId": case_file_version_id}
        ))