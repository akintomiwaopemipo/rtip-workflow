from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date

from models.tast_status import TaskStatus
from models.test_decision import TaskDecision, TaskDecisionType


class TaskState(BaseModel):
    id: str = Field(..., description="Unique task ID")
    workflow_instance_id: str = Field(..., description="Associated workflow instance ID")
    case_file_version_id: str = Field(..., description="Associated case file version ID")

    department_name: str
    assigned_to_user: str

    create_date: date
    due_date: date
    complete_date: Optional[date] = None

    status: TaskStatus

    decision: Optional[TaskDecision] = Field(
        default=None,
        description="Decision taken for the task (e.g., 'Approved', 'Declined', 'Valid', 'Yes')"
    )
    
    decision_type: Optional[TaskDecisionType] = Field(
        default=None,
        description="Type/category of decision (e.g., 'submission', 'validation', 'boolean')"
    )

    # Response from external system
    response: Optional[str] = None

    # Structured + flexible data
    data: Dict[str, Any] = Field(default_factory=dict)
    data_type: Optional[str] = Field(
        default=None,
        description="Type of data stored in `data` (e.g., 'finance', 'hr')"
    )



    class Config:
        use_enum_values = True