"""Unit tests for get_next_bank_holiday, with the GOV.UK feed replaced by fake data."""
import pytest

from service_desk import holidays

FAKE_DATA = {
    "england-and-wales": {"events": [
        {"title": "Long past holiday", "date": "2000-01-03"},
        {"title": "Far future holiday", "date": "2099-12-25"},
        {"title": "Nearer future holiday", "date": "2098-05-01"},
    ]},
    "scotland": {"events": [{"title": "Old holiday", "date": "2000-01-04"}]},
}


@pytest.fixture
def fake_feed(monkeypatch):
    """Replace load_bank_holidays so tests don't call GOV.UK or write the cache."""
    monkeypatch.setattr(holidays, "load_bank_holidays", lambda: (FAKE_DATA, "api"))


def test_returns_earliest_upcoming_holiday(fake_feed):
    result = holidays.get_next_bank_holiday()
    assert result["status"] == "success"
    assert result["title"] == "Nearer future holiday"
    assert result["source"] == "api"


def test_region_ignores_case_and_spaces(fake_feed):
    assert holidays.get_next_bank_holiday("  England-and-Wales ")["status"] == "success"


def test_unknown_region_lists_valid_regions(fake_feed):
    result = holidays.get_next_bank_holiday("wales")
    assert result["status"] == "error"
    assert "england-and-wales" in result["error_message"]


def test_no_upcoming_holidays(fake_feed):
    assert holidays.get_next_bank_holiday("scotland")["status"] == "error"


def test_feed_and_cache_both_unavailable(monkeypatch):
    def fail():
        raise RuntimeError("Could not connect.")

    monkeypatch.setattr(holidays, "load_bank_holidays", fail)
    result = holidays.get_next_bank_holiday()
    assert result["status"] == "error"
    assert "unavailable" in result["error_message"]
