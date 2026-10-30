tickets = [
    {"id": 1041, "title": "Laptop won't boot", "priority": 1, "status": "open", "hours_open": 5.0, "assigned_to": "Priya", "service": "Hardware"},
    {"id": 1042, "title": "VPN not connecting", "priority": 2, "status": "open", "hours_open": 5.5, "assigned_to": None, "service": "Network"},
    {"id": 1043, "title": "Password reset", "priority": 3, "status": "resolved", "hours_open": 1.0, "assigned_to": "Sam", "service": "Accounts"},
    {"id": 1044, "title": "Wi-Fi drops in office", "priority": 2, "status": "open", "hours_open": 12.0, "assigned_to": "Priya", "service": "Network"},
    {"id": 1045, "title": "New starter account", "priority": 4, "status": "open", "hours_open": 30.0, "assigned_to": None, "service": "Accounts"},
    {"id": 1046, "title": "Printer jam", "priority": 3, "status": "open", "hours_open": 26.0, "assigned_to": "Sam", "service": "Hardware"},
]

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}

SERVICES = {
    "Network": {"owner_team": "Infrastructure", "support_hours": "24/7", "description": "VPN, Wi-Fi and office connectivity"},
    "Hardware": {"owner_team": "End User Computing", "support_hours": "Mon-Fri 08:00-18:00", "description": "Laptops, printers and peripherals"},
    "Accounts": {"owner_team": "Identity & Access", "support_hours": "Mon-Fri 08:00-18:00", "description": "Logins, passwords and new starter accounts"},
}


'''
get_sla_hours(priority: int) -> int returns the SLA hours, defaulting to 72 for an unknown priority.
'''
def get_sla_hours(priority: int) -> int:
    """Return the SLA target in hours for a ticket priority.

    Args:
        priority: Ticket priority from 1 (most urgent) to 4.

    Returns:
        Hours allowed before the ticket breaches its SLA (72 if the priority is unknown).
    """
    return SLA_HOURS.get(priority, 72)

print(get_sla_hours(5))

'''
is_breached(ticket: dict) -> bool returns True if the ticket is open and over its SLA. Use get_sla_hours inside it.
'''
def is_breached(ticket: dict) -> bool:
    """Return True if the ticket is open and has been open longer than its SLA."""
    return ticket["status"] == "open" and ticket["hours_open"] > get_sla_hours(ticket["priority"])

'''
format_ticket(ticket: dict, show_assignee: bool = False) -> str returns a line like 1042: VPN not connecting | P2 | open. When show_assignee=True, it adds | Unassigned or | Priya to the end. It must return the string, not print it.
'''

'''
get_ticket_status(ticket_id: int) -> dict is a tool-style function.
If the ticket exists, return "status": "success" plus the title, the ticket’s status (use the key "ticket_status" so it doesn’t clash with "status"), the priority, the assignee and "sla_breached".
If it doesn’t exist, return an error dict.
Write a full Args/Returns docstring.
Test it with 1044 and 9999.
'''

'''
get_service_details(service_name: str) -> dict is also tool-style.
Matching: match the name case-insensitively and ignore extra spaces, so " network " finds Network.
On success: return the service’s details plus "open_ticket_ids", a list of the IDs of its open tickets.
On failure: return an error whose message lists the known services.
Test it with " network " and "Email".
'''

'''
Experiment. Run help(get_ticket_status). Then call get_sla_hours("2"), passing a string instead of an int. What happens, and why does it matter for an agent?
'''