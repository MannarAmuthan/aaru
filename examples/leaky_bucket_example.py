import requests
from requests import ConnectTimeout

from alavu import Alavu, RateStrategy
from strategies.batch_window import CallBackRequest


def fetch_from_site():
    try:
        res = requests.get('https://www.example.com', timeout=2)
        return res
    except ConnectTimeout:
        return None


alavu = Alavu(window_in_seconds=2,
              strategy=RateStrategy.LEAKY_BUCKET)
alavu.load([CallBackRequest(callback=fetch_from_site, args=[]) for _ in range(0, 4)])
alavu.start()

results = alavu.get_result()

count = 0

for result in results:
    print(result)
    count += 1

assert count == 4
print("All results are got")
