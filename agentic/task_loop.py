from agentic.planner import plan_task
from agentic.executor import execute_step
from agentic.evaluator import evaluate
from safety.governor import SafetyGovernor
from safety.confirmations import require_confirmation
from agentic.working_memory import WorkingMemory

def run_task(goal):
    memory = WorkingMemory()
    plan = planner.create_plan(goal)

    for step in plan.steps:
        output = executor.execute(step)
        result = evaluator.evaluate(step, output)

        memory.record_step(step, output, result)

        if not result.success:
            memory.record_failure(step, result)
            break

def run_agentic_task(goal: str):
    steps = plan_task(goal)
    governor = SafetyGovernor()

    for step in steps:
        risk = governor.check(step)
        if not require_confirmation(risk):
            return "Tugas dihentikan oleh pengguna."

        result = execute_step(step)

        if not evaluate(step, result):
            return f"Tugas gagal di langkah: {step}"

    return "Tugas selesai dengan sukses."
