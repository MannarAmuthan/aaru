import random
import threading
import time

from matplotlib import pyplot as plt, animation

from strategies.leaky_bucket import LeakyBucket, CallBackRequest


def test_leaky_bucket():
    triggered_times = []

    def sample_callback():
        triggered_times.append(time.monotonic())
        time.sleep(random.uniform(0.1, 0.4))

    leaky_bucket = LeakyBucket(bucket_size=1,
                               leak_window_in_seconds=5)

    leaky_bucket.fill([CallBackRequest(sample_callback, []) for i in range(0, 2)])

    leaky_bucket.start()

    assert len(triggered_times) == 2, "Both callbacks should have been triggered."

    time_diff = triggered_times[1] - triggered_times[0]
    assert time_diff >= 5, f"Expected at least 5 seconds between callbacks, but got {time_diff:.2f} seconds."


def test_leaky_bucket_2():
    triggered_times = []


    def sample_callback():
        current_time = time.time()
        triggered_times.append(current_time)
        # time.sleep(0.4)

    bucket_size = 10
    leak_window_in_seconds = 3

    leaky_bucket = LeakyBucket(bucket_size=bucket_size, leak_window_in_seconds=leak_window_in_seconds)
    leaky_bucket.fill([CallBackRequest(sample_callback, []) for i in range(0, 50)])

    leaky_bucket.start()
    triggered_times.sort()
    for i in range(len(triggered_times)):
        window_start = triggered_times[i]
        count_in_window = sum(1 for t in triggered_times if window_start <= t < window_start + leak_window_in_seconds)
        print(count_in_window)
        assert count_in_window <= bucket_size, f"Exceeded {bucket_size} requests in {leak_window_in_seconds} seconds: {count_in_window} requests."

