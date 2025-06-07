from typing import List, Tuple

from strategies.batch_window import BatchWindow, CallBackRequest
from strategies.leaky_bucket import LeakyBucket


class RateStrategy:
    BATCH_WINDOW = 1
    LEAKY_BUCKET = 2

class Alavu:
    def __init__(self,
                 max_requests_per_window: int = None,
                 window_in_seconds: int = None,
                 strategy: RateStrategy = RateStrategy.BATCH_WINDOW):
        self.index = 0

        if strategy == RateStrategy.BATCH_WINDOW:
            self.strategy = BatchWindow(
                max_requests_per_window=max_requests_per_window,
                window_in_seconds=window_in_seconds
            )

        if strategy == RateStrategy.LEAKY_BUCKET:
            self.strategy = LeakyBucket(
                window_in_seconds=window_in_seconds
            )

        self.callback_requests = []

    def load(self, callback_requests: List[CallBackRequest]):
        self.strategy.fill(callback_requests)
        self.callback_requests.extend(callback_requests)

    def start(self):
        self.strategy.start()

    def stop(self):
        self.strategy.stop()

    def get_result(self):
        return [r.get_result() for r in self.callback_requests]
