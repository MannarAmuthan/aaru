
### Alavu

Advanced Client side rate limiter

#### example usage
```python
import requests

from alavu import Alavu
from strategies.leaky_bucket import CallBackRequest

def fetch_from_site():
    return requests.get('https://www.example.com')

alavu = Alavu(max_requests_per_window=10,
              window_in_seconds=2)
alavu.load([CallBackRequest(callback=fetch_from_site, args=[]) for _ in range(0, 50)])
alavu.start()

results = alavu.get_result()

for result in results:
    print(result)
```