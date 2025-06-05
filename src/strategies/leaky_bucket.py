import concurrent.futures
import time
import uuid
from collections import deque
from typing import List, Callable, TypedDict, Optional, Dict


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


class LeakyBucket:
    def __init__(self,
                 bucket_size: int,
                 leak_window_in_seconds: int):
        self.leak_window_in_seconds = leak_window_in_seconds

        self.capacity = bucket_size
        self.size = 0
        self.callbacks = deque()
        self.uncompleted_ids = set()
        self.run = True

    def fill(self, callbacks: List[CallBackRequest]):
        for c in callbacks:
            self.callbacks.append(c)

    def stop(self):
        self.run = False

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

                remain = self.leak_window_in_seconds - (
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
            if elapsed > self.leak_window_in_seconds:
                break

            remain_ = self.leak_window_in_seconds - elapsed

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
