"""Bank holiday tool, backed by the GOV.UK bank holidays feed with a local cache."""
import json
from datetime import date

import requests

from .data_loader import DATA_DIR

BANK_HOLIDAYS_URL = "https://www.gov.uk/bank-holidays.json"
CACHE_PATH = DATA_DIR / "bank_holidays_cache.json"


def fetch_json(url: str, params: dict | None = None, timeout: float = 10) -> dict | list:
    """Send a GET request and return the parsed JSON response.

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
        raise RuntimeError(f"Could not connect to {url}.") from None
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Request to {url} failed with HTTP {e.response.status_code}.") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request to {url} failed: {e}") from e


def load_bank_holidays(url: str = BANK_HOLIDAYS_URL) -> tuple[dict, str]:
    """Fetch UK bank holidays, falling back to a local cached copy if the API fails.

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


def get_next_bank_holiday(region: str = "england-and-wales") -> dict:
    """Find the next UK bank holiday for a region.

    Args:
        region: One of "england-and-wales", "scotland" or "northern-ireland".
            Use "england-and-wales" if the user doesn't say.

    Returns:
        On success, a dict with "status": "success" plus the region, the
        holiday's title and date (YYYY-MM-DD), and "source": "api" or "cache"
        to show whether the data is live or a saved copy. On failure, a dict
        with "status": "error" and an error_message.
    """
    try:
        data, source = load_bank_holidays()
    except RuntimeError as e:
        return {"status": "error", "error_message": f"Bank holiday data is unavailable: {e}"}

    region = region.strip().lower()
    if region not in data:
        valid = ", ".join(data)
        return {"status": "error", "error_message": f"Unknown region '{region}'. Valid regions: {valid}."}

    today = date.today().isoformat()
    upcoming = [e for e in data[region]["events"] if e["date"] >= today]
    if not upcoming:
        return {"status": "error", "error_message": f"No upcoming bank holidays are listed for {region}."}

    next_holiday = min(upcoming, key=lambda e: e["date"])
    return {
        "status": "success",
        "region": region,
        "title": next_holiday["title"],
        "date": next_holiday["date"],
        "source": source,
    }