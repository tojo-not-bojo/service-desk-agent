"""Tools the service desk agent can call."""
from .data_loader import load_json

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}
TICKETS = load_json("tickets.json")
TICKETS_BY_ID = {t["id"]: t for t in TICKETS}
SERVICES = load_json("services.json")


def get_sla_hours(priority: int) -> int:
    """Return the SLA target in hours for a ticket priority (72 if unknown)."""
    return SLA_HOURS.get(priority, 72)


def is_breached(ticket: dict) -> bool:
    """Return True if the ticket is open and has been open longer than its SLA."""
    return ticket["status"] == "open" and ticket["hours_open"] > get_sla_hours(ticket["priority"])


def get_ticket_status(ticket_id: int) -> dict:
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
            open_ids = [t["id"] for t in tickets if t["service"] == name and t["status"] == "open"]
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
# and `SERVICES` now coming from load_json


if __name__ == "__main__":
    print(get_ticket_status(1044))
    print(get_ticket_status("abc"))
    print(get_service_details(" network "))
    print(get_service_details("Email"))