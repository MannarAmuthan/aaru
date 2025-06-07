import concurrent.futures
import time

from strategies.Strategy import Strategy
from strategies.callback_request import CallBackRequest


"""
BatchWindow Strategy

Allows up to `max_requests_per_window` requests to be executed
within each `window_in_seconds` time window. All requests are
submitted as a batch, and then the limiter waits until the next window.

This strategy is equivalent to a Fixed Window rate limiter.
"""

class BatchWindow(Strategy):
    def __init__(self,
                 max_requests_per_window: int,
                 window_in_seconds: int):
        super().__init__(max_requests_per_window, window_in_seconds)
        self.window_in_seconds = window_in_seconds

        self.capacity = max_requests_per_window
        self.size = 0

        self.uncompleted_ids = set()

    def start(self):
        futures = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while self.run:

                start_time = time.monotonic()

                for i in range(0, self.capacity):
                    if len(self.callbacks) > 0:
                        callback_request: CallBackRequest = self.callbacks.popleft()
                        futures[callback_request.uuid] = executor.submit(callback_request.execute)
                    else:
                        break

                self._check_results_for_remaining_time(futures, start_time)

                remain = self.window_in_seconds - (
                        time.monotonic() - start_time
                )

                if len(self.callbacks) == 0 and len(futures) == 0:
                    break

                if remain > 0:
                    time.sleep(remain)

    def _check_results_for_remaining_time(self, futures, start_time):
        while True:
            current_time = time.monotonic()

            elapsed = current_time - start_time
            if elapsed > self.window_in_seconds:
                break

            remain_ = self.window_in_seconds - elapsed

            future_temps = []
            max_count = self.capacity
            count = 0

            for unique_id, future in futures.items():
                count += 1
                if count <= max_count:
                    future_temps.append(future)
                else:
                    break

            for future in concurrent.futures.as_completed(future_temps):
                finished_uuid = future.result()
                futures.pop(finished_uuid)

            if len(futures) == 0:
                return
