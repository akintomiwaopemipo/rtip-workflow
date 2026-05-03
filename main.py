from datetime import date

from models.task_state import TaskState
from models.tast_status import TaskStatus


task = TaskState(
    id="task123",
    case_file_version_id="casefilev1",
    department_name="Finance",
    assigned_to_user="alice",
    create_date= date(2024, 1, 1),
    due_date=date(2024, 1, 10),
    status= TaskStatus.IN_PROCESS,
)


print(task)