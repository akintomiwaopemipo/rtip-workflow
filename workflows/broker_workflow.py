from typing import Any, Generator
from dapr.ext.workflow import DaprWorkflowContext

from activities.broker import broker_submission, complete_task, create_task, update_task_after_submission
from activities.decline import decline_submission
from activities.submission import get_submission
from decorators import workflow




@workflow("broker_workflow")
def broker_workflow(ctx: DaprWorkflowContext, payload: Any) -> Generator[Any, Any, Any]:

    # Create initial task
    task_id = yield ctx.call_activity(
        create_task,
        input={
            "workflow_instance_id": ctx.instance_id,
            "payload": payload
        }
    )

    # Call broker submission
    result = yield ctx.call_activity(
        broker_submission,
        input=payload
    )

    case_file_version_id = result["caseFileVersionId"]
    violations = result.get("guidelinesViolations", [])

    # Update task with response
    yield ctx.call_activity(
        update_task_after_submission,
        input={
            "task_id": task_id,
            "response": result,
            "case_file_version_id": case_file_version_id
        }
    )

    # Decision branch
    if not violations:
        # APPROVED path
        yield ctx.call_activity(
            complete_task,
            input={
                "task_id": task_id,
                "decision": "Approved",
                "decision_type": "submission"
            }
        )

        return (yield ctx.call_activity(
            get_submission,
            input={"caseFileVersionId": case_file_version_id}
        ))

    else:
        # DECLINED path
        yield ctx.call_activity(
            complete_task,
            input={
                "task_id": task_id,
                "decision": "Declined",
                "decision_type": "submission"
            }
        )

        return (yield ctx.call_activity(
            decline_submission,
            input={"caseFileVersionId": case_file_version_id}
        ))