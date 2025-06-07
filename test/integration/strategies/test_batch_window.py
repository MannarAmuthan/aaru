import random
import time

from strategies.batch_window import BatchWindow, CallBackRequest


def test_batch_window():
    triggered_times = []

    def sample_callback():
        triggered_times.append(time.monotonic())
        time.sleep(random.uniform(0.1, 0.4))

    batch_window = BatchWindow(max_requests_per_window=1,
                               window_in_seconds=5)

    batch_window.fill([CallBackRequest(sample_callback, []) for i in range(0, 2)])

    batch_window.start()

    assert len(triggered_times) == 2, "Both callbacks should have been triggered."

    time_diff = triggered_times[1] - triggered_times[0]
    assert time_diff >= 5, f"Expected at least 5 seconds between callbacks, but got {time_diff:.2f} seconds."


def test_batch_window_2():
    triggered_times = []

    def sample_callback():
        current_time = time.time()
        triggered_times.append(current_time)

    max_requests_per_window = 10
    leak_window_in_seconds = 3

    batch_window = BatchWindow(max_requests_per_window=max_requests_per_window,
                               window_in_seconds=leak_window_in_seconds)
    batch_window.fill([CallBackRequest(sample_callback, []) for i in range(0, 50)])

    batch_window.start()
    triggered_times.sort()
    for i in range(len(triggered_times)):
        window_start = triggered_times[i]
        count_in_window = sum(1 for t in triggered_times if window_start <= t < window_start + leak_window_in_seconds)
        print(count_in_window)
        assert count_in_window <= max_requests_per_window, f"Exceeded {max_requests_per_window} requests in {leak_window_in_seconds} seconds: {count_in_window} requests."
