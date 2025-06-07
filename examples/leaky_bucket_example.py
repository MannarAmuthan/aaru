import requests
from requests import ConnectTimeout

from aaru import Aaru, Mode
from strategies.batch_window import CallBackRequest


def fetch_from_site():
    try:
        res = requests.get('https://www.example.com', timeout=2)
        return res
    except ConnectTimeout:
        return None


aaru = Aaru(window_in_seconds=2,
            mode=Mode.LEAKY_BUCKET)
aaru.load([CallBackRequest(callback=fetch_from_site, args=[]) for _ in range(0, 4)])
aaru.start()

results = aaru.get_result()

count = 0

for result in results:
    print(result)
    count += 1

assert count == 4
print("All results are got")
