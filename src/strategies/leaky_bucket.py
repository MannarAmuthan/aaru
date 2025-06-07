import concurrent.futures
import time
from time import sleep

from strategies.Strategy import Strategy
from strategies.callback_request import CallBackRequest


class LeakyBucket(Strategy):
    def __init__(self,
                 window_in_seconds: float):
        super().__init__(1,
                         window_in_seconds)
        self.window_in_seconds = window_in_seconds

    def start(self):
        futures = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            while self.callbacks and self.run:
                callback_request: CallBackRequest = self.callbacks.popleft()
                futures[callback_request.uuid] = executor.submit(callback_request.execute)
                start_time = time.monotonic()
                try:
                    for future in concurrent.futures.as_completed([f for uid, f in futures.items()],
                                                                  timeout=self.window_in_seconds):
                        finished_uuid = future.result()
                        futures.pop(finished_uuid)
                except TimeoutError:
                    pass

                elapsed = time.monotonic() - start_time

                if elapsed < self.window_in_seconds:
                    sleep(self.window_in_seconds - elapsed)

