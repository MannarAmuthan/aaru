import math
import random
import time

from strategies.callback_request import CallBackRequest
from strategies.leaky_bucket import LeakyBucket


def test_batch_window():
    triggered_times = []

    def sample_callback():
        triggered_times.append(time.monotonic())
        time.sleep(random.uniform(0.1, 0.4))

    leaky_bucket = LeakyBucket(window_in_seconds=2.7)
    leaky_bucket.fill([CallBackRequest(sample_callback, []) for i in range(0, 10)])
    leaky_bucket.start()

    triggered_times.sort()
    last = triggered_times[0]
    for i in range(1, len(triggered_times)):
        time_elapsed = math.fabs(triggered_times[i] - last)
        assert  time_elapsed >= 2.7
        last = triggered_times[i]



