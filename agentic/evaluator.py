def evaluate(step, output, memory=None):
    if memory and memory.failures:
        recent_failures = [f["step"] for f in memory.failures[-2:]]
        if step in recent_failures:
            return ExecutionResult(
                success=False,
                reason="Repeated failure on same step",
                recoverable=False
            )
def evaluate(step: str, result: str) -> bool:
    """
    Evaluasi sederhana:
    - sukses / gagal
    - aman / tidak
    """
    if "error" in result.lower():
        return False
    return True
