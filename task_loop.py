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

