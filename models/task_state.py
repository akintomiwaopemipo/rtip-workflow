from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import date

from models.tast_status import TaskStatus



class TaskState(BaseModel):
    id: str = Field(..., description="Unique task ID")
    case_file_version_id: str = Field(..., description="Associated case file version ID")
    department_name: str
    assigned_to_user: str
    create_date: date
    due_date: date
    complete_date: Optional[date] = None
    status: TaskStatus = TaskStatus.PENDING
    data: Dict[str, Any] = Field(default_factory=dict)
    data_type: Optional[str] = Field(
        default=None,
        description="Type of data stored in `data` (e.g., 'finance', 'hr')"
    )

    class Config:
        use_enum_values = True