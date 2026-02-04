class WorkingMemory:
    def __init__(self):
        self.steps_taken = []
        self.failures = []
        self.notes = []

    def record_step(self, step, output, result):
        self.steps_taken.append({
            "step": step,
            "output": output,
            "success": result.success
        })

    def record_failure(self, step, result):
        self.failures.append({
            "step": step,
            "reason": result.reason,
            "recoverable": result.recoverable,
            "severity": getattr(result, "severity", "normal")
        })
class WorkingMemory:
    def __init__(self):
        self.steps_taken = []
        self.failures = []
        self.assumptions = []

    def add_note(self, note: str):
        self.notes.append(note)

    def summary(self):
        return {
            "total_steps": len(self.steps_taken),
            "failures": self.failures,
            "notes": self.notes
        }
def failure_summary(self, max_items=3):
    summaries = []
    for f in self.failures[-max_items:]:
        summaries.append(
            f"- Step `{f['step']}` failed because: {f['reason']} "
            f"(recoverable={f['recoverable']})"
        )
    return "\n".join(summaries)


def planner_context(self):
    context = []

    if self.failures:
        context.append("Previous failures to consider:")
        context.append(self.failure_summary())

    if self.notes:
        context.append("Important notes:")
        for note in self.notes[-3:]:
            context.append(f"- {note}")

    return "\n".join(context)
