"""Shared test helpers. pytest loads this file automatically for every test in this folder."""
from types import SimpleNamespace

import pytest


@pytest.fixture
def make_context():
    """Return a function that builds a stand-in ToolContext for a given user.

    The tools only use .user_id, .state and .invocation_id, so a simple object
    with those attributes is enough. A real ToolContext needs a whole ADK session.
    """
    def _make(user_id: str = "user", state: dict | None = None) -> SimpleNamespace:
        return SimpleNamespace(
            user_id=user_id,
            state={} if state is None else state,
            invocation_id="test-invocation",
        )
    return _make
