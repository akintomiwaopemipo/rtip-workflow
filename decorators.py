from dapr.ext.workflow import WorkflowRuntime
from typing import Callable, Generator, TypeVar, Any, cast

A = TypeVar("A", bound=Callable[..., Any])
W = TypeVar("W", bound=Callable[..., Generator[Any, Any, Any]])

wfr = WorkflowRuntime()

def activity(name: str) -> Callable[[A], A]:
    def decorator(fn: A) -> A:
        wrapped = wfr.activity(name=name)(fn) # pyright: ignore[reportUntypedFunctionDecorator, reportCallIssue, reportUnknownMemberType, reportUnknownVariableType]
        return cast(A, wrapped)
    return decorator


def workflow(name: str) -> Callable[[W], W]:
    def decorator(fn: W) -> W:
        wrapped = wfr.workflow(name=name)(fn) # pyright: ignore[reportUnknownMemberType, reportCallIssue, reportUnknownVariableType]
        return cast(W, wrapped)
    return decorator