from agentic.planner import plan_task
from agentic.executor import execute_step
from agentic.evaluator import evaluate
from safety.governor import SafetyGovernor
from safety.confirmations import require_confirmation
from agentic.working_memory import WorkingMemory
from agentic.planner import plan
from agentic.executor import execute, simulate
from agentic.evaluator import evaluate
from core_ai.reflection import reflect
from memory.memory_store import MemoryStore

def run_task(task):
    memory = MemoryStore()
    state = AgentState()

    while state.loop_count < state.max_loops:
        state.loop_count += 1

        # 1️⃣ PLANNING (dengan memory)
        plan_steps = plan(task, memory)

        # 2️⃣ SIMULATION (ragu sebelum bertindak)
        sim_result = simulate(plan_steps)

        if not sim_result["safe"]:
            state.confidence *= 0.7
            if state.confidence < 0.4:
                return "ABORT: confidence too low"
            continue  # replan

        # 3️⃣ EXECUTION
        result = execute(plan_steps)

        # 4️⃣ EVALUATION (hak veto)
        evaluation = evaluate(result, task, memory)

        if evaluation["verdict"] == "REJECT":
            state.confidence *= 0.6
            reflect(task, result, evaluation, memory)

            if state.confidence < 0.3:
                return "STOPPED: evaluator veto"
            continue  # replan

        # 5️⃣ SUCCESS PATH
        reflect(task, result, evaluation, memory)
        return "SUCCESS"

    return "FAILED: max loops reached"

memory = MemoryStore()

plan = planner.plan(task, memory)
result = executor.execute(plan)
evaluation = evaluator.evaluate(result, task, memory)
reflection.reflect(task, result, evaluation, memory)

if evaluation["risk"] > THRESHOLD:
    planner.replan(reason=evaluation["reason"])
task.confidence *= 0.85
if task.confidence < MIN_CONF:
    ask_user_or_pause()
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
