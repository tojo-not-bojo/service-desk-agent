"""Tools the service desk agent can call."""
from .data_loader import load_json
from google.adk.tools import ToolContext

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}
TICKETS = load_json("tickets.json")
TICKETS_BY_ID = {t["id"]: t for t in TICKETS}
SERVICES = load_json("services.json")
MAX_DETAIL_LENGTH = 40
USERS = load_json("users.json")


def can_view_ticket(user_id: str, ticket: dict) -> bool:
    """Return True if the user may see the ticket: service desk staff see all, others only their own."""
    user = USERS.get(user_id)
    if user is None:
        return False
    return user["role"] == "service_desk" or ticket["raised_by"] == user_id


def is_valid_detail(value: str) -> bool:
    """Return True if value is 1-40 characters of letters, spaces, hyphens and apostrophes."""
    return 0 < len(value) <= MAX_DETAIL_LENGTH and all(c.isalpha() or c in " '-" for c in value)


def save_user_details(name: str, team: str, tool_context: ToolContext) -> dict:
    """Save the user's name and team so they're remembered in future conversations.

    Only call this when the user has told you their name and team.

    Args:
        name: The user's first name.
        team: The team or department the user works in, for example "Finance".

    Returns:
        On success, a dict with "status": "success" and the saved name and team.
        If either value is invalid, a dict with "status": "error" and an error_message.
    """
    name = name.strip()
    team = team.strip()
    if not name or not team:
        return {"status": "error", "error_message": "Both a name and a team are needed."}
    
    if not is_valid_detail(name) or not is_valid_detail(team):
        return {
            "status": "error",
            "error_message": "Name and team must be 1-40 characters: letters, spaces, hyphens and apostrophes only.",
        }
    
    tool_context.state["user:name"] = name
    tool_context.state["user:team"] = team
    return {"status": "success", "name": name, "team": team}


def get_sla_hours(priority: int) -> int:
    """Return the SLA target in hours for a ticket priority (72 if unknown)."""
    return SLA_HOURS.get(priority, 72)


def is_breached(ticket: dict) -> bool:
    """Return True if the ticket is open and has been open longer than its SLA."""
    return ticket["status"] == "open" and ticket["hours_open"] > get_sla_hours(ticket["priority"])


def get_ticket_status(ticket_id: int, tool_context: ToolContext | None = None) -> dict:
    """Look up a service desk ticket and report its current status.

    Args:
        ticket_id: The numeric ticket ID, for example 1042.

    Returns:
        On success, a dict with "status": "success" plus the ticket's title,
        ticket_status, priority, assigned_to and sla_breached. On failure,
        a dict with "status": "error" and an error_message.
    """

    try:
        ticket_id = int(str(ticket_id).strip())
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Ticket ID must be a number, for example 1042. Got {ticket_id!r}.",
        }

    ticket = TICKETS_BY_ID.get(ticket_id)
    if ticket is None:
        return {"status": "error", "error_message": f"Ticket {ticket_id} not found."}

    if tool_context is None or not can_view_ticket(tool_context.user_id, ticket):
        return {
            "status": "error",
            "error_message": f"You can't view ticket {ticket_id}. You can only view tickets you raised.",
        }

    viewed = list(tool_context.state.get("viewed_tickets", []))
    if ticket_id not in viewed:
        viewed.append(ticket_id)
    tool_context.state["viewed_tickets"] = viewed

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "title": ticket["title"],
        "ticket_status": ticket["status"],
        "priority": ticket["priority"],
        "assigned_to": ticket["assigned_to"],
        "sla_breached": is_breached(ticket),
    }


def get_service_details(service_name: str) -> dict:
    """Get details about an IT service and its currently open tickets.

    Args:
        service_name: Name of the service, for example "Network". Not case-sensitive.

    Returns:
        On success, a dict with "status": "success" plus the service name,
        owner_team, support_hours, description and open_ticket_ids. If the
        service isn't known, a dict with "status": "error" and an
        error_message listing the valid service names.
    """
    for name, details in SERVICES.items():
        if name.lower() == service_name.strip().lower():
            open_ids = [t["id"] for t in TICKETS if t["service"] == name and t["status"] == "open"]
            return {
                "status": "success",
                "service": name,
                "owner_team": details["owner_team"],
                "support_hours": details["support_hours"],
                "description": details["description"],
                "open_ticket_ids": open_ids,
            }

    known = ", ".join(SERVICES)
    return {"status": "error", "error_message": f"No service called '{service_name}'. Known services: {known}."}


if __name__ == "__main__":
    print(get_ticket_status(1044))
    print(get_ticket_status("abc"))
    print(get_service_details(" network "))
    print(get_service_details("Email"))