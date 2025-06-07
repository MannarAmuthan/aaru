import uuid
from typing import Callable, List


class CallBackRequest:
    def __init__(self, callback: Callable, args: List):
        self.callback = callback
        self.args = args
        self._completed = False
        self.result = None
        self.uuid = uuid.uuid4().hex

    def is_completed(self):
        return self._completed

    def execute(self):
        result = self.callback(*self.args)
        unique_id = self.uuid
        self._completed = True
        self.result = result
        return unique_id

    def get_result(self):
        return self.result
