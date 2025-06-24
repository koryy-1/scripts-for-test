import requests
import datetime
import time
import statistics


url = "https://yandex.com/time/sync.json?geo=213"

print("a) raw data:")
response = requests.get(url)
print(response.text)

data = response.json()

unix_time = int(data["time"] / 1000)  # ms to seconds
moscow_time = datetime.datetime.fromtimestamp(unix_time) + datetime.timedelta(
    milliseconds=data["clocks"]["213"]["offset"]
)
formatted_time = moscow_time.strftime("%Y-%m-%d %H:%M:%S")
timezone = data["clocks"]["213"]["offsetString"]
print("\nb) human time:", formatted_time)
print("time zone:", timezone)

print("\nc) delta between local time and api time (sec):")
local_time = time.time()
api_time = int(requests.get(url).json()["time"] / 1000)
delta = abs(api_time - local_time)
print("delta (sec):", delta)

print("\nd) average delta in 5 requests:")
deltas = []
for _ in range(5):
    local_time = time.time()
    api_time = int(requests.get(url).json()["time"] / 1000)
    delta = abs(api_time - local_time)
    deltas.append(delta)
    time.sleep(0.5)
avg_delta = statistics.mean(deltas)
print("average delta (sec):", avg_delta)
