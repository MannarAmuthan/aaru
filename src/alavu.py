from typing import List, Tuple

from strategies.leaky_bucket import LeakyBucket, CallBackRequest


class Alavu:
    def __init__(self,
                 max_requests_per_window: int,
                 window_in_seconds: int):
        self.max_actions_per_window = max_requests_per_window
        self.window_in_seconds = window_in_seconds
        self.index = 0

        self.strategy = LeakyBucket(
            bucket_size=max_requests_per_window,
            leak_window_in_seconds=window_in_seconds
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
        return [ r.get_result() for r in self.callback_requests]
