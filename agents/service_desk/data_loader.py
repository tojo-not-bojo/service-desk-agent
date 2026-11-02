"""Helpers for loading the synthetic service desk data."""
import json
from pathlib import Path

# data_loader.py → service_desk/ (parents[0]) → agents/ (parents[1]) → repo root (parents[2])
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_json(filename: str) -> list | dict:
    """Load and return the contents of a JSON file from the data folder.

    Args:
        filename: Name of the file inside data/, for example "tickets.json".

    Returns:
        The parsed JSON, usually a list of records or a dict.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the file isn't valid JSON.
    """
    path = DATA_DIR / filename
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {path}") from None
    except json.JSONDecodeError as e:
        raise ValueError(f"{filename} is not valid JSON (line {e.lineno}): {e.msg}") from e