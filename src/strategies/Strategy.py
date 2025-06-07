import abc
from collections import deque
from typing import List

from strategies.callback_request import CallBackRequest


class Strategy:
    def __init__(self,
                 max_requests_per_window: int,
                 window_in_seconds: float):
        self.max_requests_per_window = max_requests_per_window
        self.window_in_seconds = window_in_seconds

        self.run = True
        self.callbacks = deque()

    def fill(self, callbacks: List[CallBackRequest]):
        for c in callbacks:
            self.callbacks.append(c)

    def stop(self):
        self.run = False

    @abc.abstractmethod
    def start(self):
        pass
