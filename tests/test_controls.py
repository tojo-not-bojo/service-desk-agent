"""Unit tests for the tool callbacks in service_desk.controls (step 17)."""
import logging
from types import SimpleNamespace

from service_desk.agent import root_agent
from service_desk.controls import ALLOWED_TOOLS, MAX_ARG_LENGTH, guard_tool_call, log_tool_call


def fake_tool(name: str) -> SimpleNamespace:
    """A stand-in for an ADK tool: the callbacks only read its name."""
    return SimpleNamespace(name=name)


# ---------- guard_tool_call (A14, A15) ----------

def test_allowed_tool_with_normal_args_goes_ahead(make_context):
    assert guard_tool_call(fake_tool("get_ticket_status"), {"ticket_id": 1041}, make_context()) is None


def test_tool_not_on_allowlist_is_blocked(make_context):
    result = guard_tool_call(fake_tool("close_ticket"), {"ticket_id": 1041}, make_context())
    assert result["status"] == "error"


def test_argument_over_limit_is_blocked(make_context):
    args = {"service_name": "x" * (MAX_ARG_LENGTH + 1)}
    assert guard_tool_call(fake_tool("get_service_details"), args, make_context())["status"] == "error"


def test_argument_at_limit_goes_ahead(make_context):
    args = {"service_name": "x" * MAX_ARG_LENGTH}
    assert guard_tool_call(fake_tool("get_service_details"), args, make_context()) is None


def test_allowlist_matches_agent_tools():
    assert {tool.__name__ for tool in root_agent.tools} == ALLOWED_TOOLS


def test_callbacks_are_attached_to_agent():
    assert root_agent.before_tool_callback is guard_tool_call
    assert root_agent.after_tool_callback is log_tool_call


# ---------- log_tool_call ----------

def test_log_has_argument_names_but_not_values(make_context, caplog):
    args = {"name": "Zoë", "team": "Finance"}
    with caplog.at_level(logging.INFO, logger="service_desk.controls"):
        result = log_tool_call(fake_tool("save_user_details"), args, make_context(), {"status": "success"})

    assert result is None                               # the tool's response is left unchanged
    assert "tool=save_user_details" in caplog.text
    assert "'name'" in caplog.text and "'team'" in caplog.text
    assert "Zoë" not in caplog.text and "Finance" not in caplog.text
