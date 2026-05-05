from enum import Enum


class StateType(str, Enum):
    TASK = "task"
    WORKFLOW = "workflow"