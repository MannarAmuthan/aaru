
### Alavu

Alavu is a flexible, client-side rate limiter and concurrency manager for Python applications. 
It allows you to manage the rate at which tasks are executed in parallel, adapting to dynamic workloads and system health metrics.

The library currently supports multiple strategies:

Batch Window — Executes a fixed batch of tasks per time window, ensuring rate limiting at batch granularity.
Leaky Bucket — Smoothens task execution by leaking tasks at a steady rate, avoiding sudden bursts.
PID-Based Adaptive Control (coming soon) — Adjusts concurrency dynamically based on process feedback like failure rate, CPU usage, or latency, ensuring smooth performance even under varying load conditions.

#### Example Use Cases:

1. Throttling API calls from your service to external APIs.
2. Managing workloads on a CPU-intensive data pipeline.
3. Preventing memory spikes by limiting task concurrency.
4. Adapting concurrency based on dynamic failure rates.

#### Example code samples

inside `examples`

#### example usage

```python
import requests
from requests import ConnectTimeout

from alavu import Alavu
from strategies.batch_window import CallBackRequest

def fetch_from_site():
    try:
        res = requests.get('https://www.example.com', timeout=2)
        return res
    except ConnectTimeout:
        return None

alavu = Alavu(max_requests_per_window=10,
              window_in_seconds=2)
alavu.load([CallBackRequest(callback=fetch_from_site, args=[]) for _ in range(0, 50)])
alavu.start()

results = alavu.get_result()

count = 0

for result in results:
    print(result)
    count += 1

assert count == 50
print("All results are got")
```