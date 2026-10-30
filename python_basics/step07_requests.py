import json
from datetime import date
from pathlib import Path

import requests

DATA_DIR = Path(__file__).parent.parent / "data"
BANK_HOLIDAYS_URL = "https://www.gov.uk/bank-holidays.json"

'''
First call.
Request the bank holidays feed and print the status code.
Print the top-level keys of the JSON.
For "england-and-wales", print its division value and how many events it has.
Print the first event in full, to see what one looks like.
'''

response = requests.get(BANK_HOLIDAYS_URL, timeout=10)
print(response.status_code)              # 200

data = response.json()

#print(data)

print(list(data))                        # ['england-and-wales', 'scotland', 'northern-ireland']

ew = data["england-and-wales"]
print(ew["division"], len(ew["events"]))
print(ew["events"][0])


'''
Filter the results.
Print every England and Wales bank holiday in 2026, as 2026-12-25 Christmas Day.
Find the next bank holiday from today. date.today().isoformat() gives today as a string like "2026-10-30".
'''

events = data["england-and-wales"]["events"]

for e in events:
    if e["date"].startswith("2026"):
        print(f"{e['date']}  {e['title']}")

today = date.today().isoformat()
upcoming = [e for e in events if e["date"] >= today]
next_holiday = min(upcoming, key=lambda e: e["date"])
print(f"Next: {next_holiday['title']} on {next_holiday['date']}")

'''
Query parameters. Get the current weather for Leeds from https://api.open-meteo.com/v1/forecast, with these parameters:
python
   {"latitude": 53.80, "longitude": -1.55, "current": "temperature_2m,wind_speed_10m"}
Print response.url to see how the parameters were added to the URL.
Look at the JSON, then print the temperature and wind speed with their units, which are in a separate part of the response.
'''

params = {"latitude": 53.80, "longitude": -1.55, "current": "temperature_2m,wind_speed_10m"}
response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=10)
response.raise_for_status()

print(response.url)
# https://api.open-meteo.com/v1/forecast?latitude=53.8&longitude=-1.55&current=temperature_2m%2Cwind_speed_10m

weather = response.json()
current = weather["current"]
units = weather["current_units"]
print(f"Leeds: {current['temperature_2m']}{units['temperature_2m']}, "
      f"wind {current['wind_speed_10m']} {units['wind_speed_10m']}")
# e.g. Leeds: 11.2°C, wind 14.8 km/h

'''
A safe fetch helper. Write fetch_json(url: str, params: dict | None = None, timeout: float = 10) -> dict | list. It should:
return the parsed JSON on success
raise RuntimeError with a clear message for a timeout, a connection failure or an HTTP error code
Test it with:
the bank holidays URL (should work)
https://www.gov.uk/no-such-page.json (404)
the bank holidays URL with timeout=0.001 (times out)
https://no-such-host.invalid (connection failure; .invalid is a domain that’s reserved so it never exists)
'''

def fetch_json(url: str, params: dict | None = None, timeout: float = 10) -> dict | list:
    """Send a GET request and return the parsed JSON response.

    Args:
        url: The URL to request.
        params: Optional query parameters.
        timeout: Seconds to wait for a response before giving up.

    Returns:
        The parsed JSON body.

    Raises:
        RuntimeError: If the request times out, can't connect, or returns an error status.
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Request to {url} timed out after {timeout}s.") from None
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Could not connect to {url}. Check the network connection.") from None
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Request to {url} failed with HTTP {e.response.status_code}.") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request to {url} failed: {e}") from e


tests = [
    (BANK_HOLIDAYS_URL, 10),
    ("https://www.gov.uk/no-such-page.json", 10),
    (BANK_HOLIDAYS_URL, 0.001),
    ("https://no-such-host.invalid", 10),
]
for url, timeout in tests:
    try:
        result = fetch_json(url, timeout=timeout)
        print(f"OK: got a {type(result)}")
    except RuntimeError as e:
        print(f"Error: {e}")

'''
Fall back to a cache. Write load_bank_holidays(url: str = BANK_HOLIDAYS_URL). It should:
fetch the feed and, on success, save a copy to data/bank_holidays_cache.json
if the fetch fails, load the cached copy instead
return two values, the data and where it came from ("api" or "cache"), as return data, "api"
raise a clear error if the fetch fails and there’s no cache
Call it once normally, then once with "https://no-such-host.invalid", and check that the second call used the cache.
'''

CACHE_PATH = DATA_DIR / "bank_holidays_cache.json"


def load_bank_holidays(url: str = BANK_HOLIDAYS_URL) -> tuple[dict, str]:
    """Fetch UK bank holidays, falling back to a local cached copy if the API fails.

    Args:
        url: The feed URL. Only changed for testing.

    Returns:
        A (data, source) pair, where source is "api" or "cache".

    Raises:
        RuntimeError: If the API fails and no cached copy exists.
    """
    try:
        data = fetch_json(url)
    except RuntimeError as api_error:
        if not CACHE_PATH.exists():
            raise RuntimeError(f"{api_error} No cached copy is available.") from api_error
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f), "cache"

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data, "api"


data, source = load_bank_holidays()
print(source)                                         # api

data, source = load_bank_holidays("https://no-such-host.invalid")
print(source)                                         # cache

'''
A tool. Write get_next_bank_holiday(region: str = "england-and-wales") -> dict, tool-style, using load_bank_holidays.
On success: return the region, the holiday’s title and date, and the source.
On failure: return error dicts for unavailable data, an unknown region (list the valid ones) and no upcoming holidays.
Test with no argument, "Scotland" and "wales".
'''