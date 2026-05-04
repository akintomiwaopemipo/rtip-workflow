from enum import Enum
from typing import Literal


class SubmissionDecision(str, Enum):
    APPROVED = "Approved"
    DECLINED = "Declined"


class ValidationDecision(str, Enum):
    VALID = "Valid"
    INVALID = "Invalid"


class BooleanDecision(str, Enum):
    YES = "Yes"
    NO = "No"


TaskDecision = SubmissionDecision | ValidationDecision | BooleanDecision
TaskDecisionType = Literal["submission", "validation", "boolean"]