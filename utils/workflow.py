import json
from typing import Any

from dapr.ext.workflow import DaprWorkflowClient


def wait_for_workflow_result(
    instance_id: str,
    timeout_in_seconds: int = 60
) -> dict[str, Any]:
    
    try:
        wf_client = DaprWorkflowClient()

        state = wf_client.wait_for_workflow_completion(
            instance_id=instance_id,
            timeout_in_seconds=timeout_in_seconds
        )

        if not state:
            return {
                "success": False,
                "error": "No state returned from workflow execution"
            }

        status = state.runtime_status.name

        if status == "COMPLETED":

            output = (
                json.loads(state.serialized_output)
                if state.serialized_output
                else None
            )

            return {
                "success": True,
                "workflow_status": status,
                "output": output
            }

        failure = None

        inner = getattr(state, "_WorkflowState__obj", None)
        if inner:
            failure = getattr(inner, "failure_details", None)

        return {
            "success": False,
            "status": status,
            "error": failure.message if failure else f"Workflow failed! Status: {status}",
            "error_type": failure.error_type if failure else None,
        }

    except TimeoutError:
        return {
            "success": False,
            "error": "Workflow timed out!"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }