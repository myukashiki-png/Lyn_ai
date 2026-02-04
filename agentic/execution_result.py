class ExecutionResult:
    def __init__(
        self,
        success: bool,
        reason: str | None = None,
        recoverable: bool = True,
        severity: str = "normal"
    ):
        self.success = success
        self.reason = reason
        self.recoverable = recoverable
        self.severity = severity

    def __repr__(self):
        return (
            f"ExecutionResult(success={self.success}, "
            f"recoverable={self.recoverable}, "
            f"severity='{self.severity}', "
            f"reason='{self.reason}')"
        )
from agentic.execution_result import ExecutionResult

class ExecutionResult:
    def __init__(self, success, reason=None, recoverable=T>
        self.success = success
        self.reason = reason
        self.recoverable = recoverable

def evaluate(step, output):
    if output is None:
        return ExecutionResult(
            success=False,
            reason="No output produced",
            recoverable=True
        )

    if "permission denied" in str(output).lower():
        return ExecutionResult(
            success=False,
            reason="Permission denied",
            recoverable=False,
            severity="high"
        )

    if "timeout" in str(output).lower():
        return ExecutionResult(
            success=False,
            reason="Execution timeout",
            recoverable=True
        )

    return ExecutionResult(success=True)
