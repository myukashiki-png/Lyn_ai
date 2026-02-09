if eval.failed:
    raise AgentDoubtException()

def evaluate(result, task, memory_store):
    past_mistakes = memory_store.recall(
        categories=["mistake"]
    )

    risk = assess_risk(result, past_mistakes)

    if risk > 0.7:
        return {
            "verdict": "REJECT",
            "reason": "Mirip kesalahan sebelumnya"
        }

    return {"verdict": "ACCEPT"}

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
