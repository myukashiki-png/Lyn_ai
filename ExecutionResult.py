class ExecutionResult:
    def __init__(self, success, reason=None, recoverable=True):
        self.success = success
        self.reason = reason
        self.recoverable = recoverable
