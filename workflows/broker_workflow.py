from typing import Any, Generator
from dapr.ext.workflow import DaprWorkflowContext

from activities.broker import broker_submission, complete_task, create_task, update_task_after_submission
from activities.decline import decline_submission
from activities.submission import get_submission
from decorators import workflow



@workflow("broker_workflow")
def broker_workflow(ctx: DaprWorkflowContext, payload: Any) -> Generator[Any, Any, Any]:

    workflow_response: dict[str, Any] = {
        "instance_id": ctx.instance_id
    }

    # Create initial task
    task_id = yield ctx.call_activity(
        create_task,
        input={
            "workflow_instance_id": ctx.instance_id,
            "payload": payload
        }
    )

    workflow_response["task_id"] = task_id

    
    # Call broker submission
    result = yield ctx.call_activity(
        broker_submission,
        input=payload
    )

    workflow_response["submission_response"] = result


    case_file_version_id = result["caseFileVersionId"]
    violations = result.get("guidelinesViolations", [])

    workflow_response["case_file_version_id"] = case_file_version_id
    workflow_response["violations"] = violations

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
        workflow_response["decision"] = "Approved"
        
        yield ctx.call_activity(
            complete_task,
            input={
                "task_id": task_id,
                "decision": "Approved",
                "decision_type": "submission"
            }
        )

        submission = yield ctx.call_activity(
            get_submission,
            input={"caseFileVersionId": case_file_version_id}
        )

        workflow_response["submission_data"] = submission

    else:
        # DECLINED path
        workflow_response["decision"] = "Declined"
        yield ctx.call_activity(
            complete_task,
            input={
                "task_id": task_id,
                "decision": "Declined",
                "decision_type": "submission"
            }
        )

        decline_submission_resonse = yield ctx.call_activity(
            decline_submission,
            input={"caseFileVersionId": case_file_version_id}
        )

        workflow_response["decline_submission_response"] = decline_submission_resonse

    return workflow_response