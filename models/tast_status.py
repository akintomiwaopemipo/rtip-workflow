from enum import Enum

class TaskStatus(str, Enum):
    IN_PROCESS = "InProcess"
    COMPLETED = "Completed"
    PENDING = "Pending"
    CANCELLED = "Cancelled"