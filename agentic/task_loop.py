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
MAX_ITERATIONS = 10

def run_task(goal):
    memory = WorkingMemory()
    plan = planner.create_plan(goal, memory)

    for iteration in range(MAX_ITERATIONS):

        if plan.is_complete():
            return SUCCESS

        step = plan.next_step()

        output = executor.execute(step)
        result = evaluator.evaluate(step, output)

        memory.steps_taken.append({
            "step": step,
            "output": output,
            "result": result
        })

        if result.success:
            continue

        # ===== failure handling =====
        memory.failures.append({
            "step": step,
            "reason": result.reason
        })

        if not result.recoverable:
            return HARD_FAIL

        # ask planner to rethink
        plan = planner.replan(
            goal=goal,
            memory=memory,
            failed_step=step,
            failure_reason=result.reason
        )

    return TIMEOUT_FAIL
