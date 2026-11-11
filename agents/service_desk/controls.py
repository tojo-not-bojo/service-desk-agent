"""Controls applied to every tool call, whatever the model decides."""
import logging
from typing import Any

from google.adk.tools import BaseTool, ToolContext

logger = logging.getLogger(__name__)

ALLOWED_TOOLS = {"get_ticket_status", "get_service_details", "get_next_bank_holiday", "save_user_details"}
MAX_ARG_LENGTH = 200


def guard_tool_call(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext) -> dict | None:
    """Block tools that aren't on the allowlist, and string arguments over MAX_ARG_LENGTH.

    Returns None to let the call go ahead, or an error dict to use instead of the tool's result.
    """
    if tool.name not in ALLOWED_TOOLS:
        logger.warning("Blocked tool %s: not on the allowlist", tool.name)
        return {"status": "error", "error_message": f"The tool {tool.name} isn't available."}

    for name, value in args.items():
        if isinstance(value, str) and len(value) > MAX_ARG_LENGTH:
            logger.warning("Blocked tool %s: argument %s is %d characters", tool.name, name, len(value))
            return {"status": "error", "error_message": f"The {name} argument is too long (max {MAX_ARG_LENGTH} characters)."}

    return None


def log_tool_call(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict) -> dict | None:
    """Log each tool call without argument values: tool, argument names, status, user and invocation."""
    logger.info(
        "tool=%s args=%s status=%s user=%s invocation=%s",
        tool.name,
        sorted(args),
        tool_response.get("status"),
        tool_context.user_id,
        tool_context.invocation_id,
    )
    return None
