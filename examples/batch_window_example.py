import requests
from requests import ConnectTimeout

from aaru import Aaru
from strategies.batch_window import CallBackRequest


def fetch_from_site():
    try:
        res = requests.get('https://www.example.com', timeout=2)
        return res
    except ConnectTimeout:
        return None


aaru = Aaru(max_requests_per_window=10,
            window_in_seconds=2)
aaru.load([CallBackRequest(callback=fetch_from_site, args=[]) for _ in range(0, 50)])
aaru.start()

results = aaru.get_result()

count = 0

for result in results:
    print(result)
    count += 1

assert count == 50
print("All results are got")
