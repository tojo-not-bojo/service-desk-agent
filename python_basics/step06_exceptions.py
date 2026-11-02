from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


'''
Read a traceback. Add this code and run it. Which line failed, what’s the exception, and what does the message tell you?
python
   TICKETS_BY_ID = {1044: {"title": "Wi-Fi drops in office"}}

   def get_title(ticket_id):
       return TICKETS_BY_ID[ticket_id]["title"]

   print(get_title(9999))

Then delete it, or comment it out, so it doesn’t stop the rest of the file.
'''
TICKETS_BY_ID = {1044: {"title": "Wi-Fi drops in office"}}

def get_title(ticket_id):
    return TICKETS_BY_ID[ticket_id]["title"]

print(get_title(9999))
'''
A safer load_json. Rewrite load_json from step 5 so that:
a missing file raises FileNotFoundError with a message giving the full path and suggesting running step05_export.py
invalid JSON raises ValueError with the file name and the line where the problem is (a json.JSONDecodeError has .lineno and .msg attributes)
Create data/broken.json containing {"id": 1, "title": "Broken",}. The trailing comma is invalid JSON. Test with "missing.json" and "broken.json", catching each error so the script prints the message instead of crashing.
'''

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


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
        raise FileNotFoundError(
            f"Data file not found: {path}. Has step05_export.py been run?"
        ) from None
    except json.JSONDecodeError as e:
        raise ValueError(
            f"{filename} is not valid JSON (line {e.lineno}): {e.msg}"
        ) from e


for name in ["missing.json", "broken.json"]:
    try:
        load_json(name)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")

'''
parse_priority(value) -> int. It should accept values like 2 and " 3 " and return the int. For anything that isn’t a whole number from 1 to 4, raise ValueError with a clear message. Test it with 2, " 3 ", "abc", 7, None and 2.5.
'''

def parse_priority(value) -> int:
    """Convert a value such as 2 or " 3 " to a ticket priority from 1 to 4.

    Args:
        value: The raw priority, as an int or a string.

    Returns:
        The priority as an int.

    Raises:
        ValueError: If the value isn't a whole number from 1 to 4.
    """
    try:
        priority = int(str(value).strip())
    except ValueError:
        raise ValueError(
            f"Priority must be a whole number from 1 to 4, got {value!r}."
        ) from None

    if not 1 <= priority <= 4:
        raise ValueError(f"Priority must be from 1 to 4, got {priority}.")
    return priority


for test in [2, " 3 ", "abc", 7, None, 2.5]:
    try:
        print(f"{test!r} -> {parse_priority(test)}")
    except ValueError as e:
        print(f"{test!r} -> Error: {e}")

'''
A tool that doesn’t crash. Update get_ticket_status (load the tickets with load_json) so it also accepts IDs given as strings, like "1044". For anything that isn’t a number, return an error dict instead of crashing. Test it with 1044, "1044", "abc" and 9999.
'''

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}
TICKETS = load_json("tickets.json")
TICKETS_BY_ID = {t["id"]: t for t in TICKETS}

# get_sla_hours and is_breached: as in step 4


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


for test in [1044, "1044", "abc", 9999]:
    print(get_ticket_status(test))

'''
Keep a batch going. Process this list with parse_priority. Collect the valid priorities and the error messages, without stopping at the first failure. Use try/except/else, then print a summary.
python
   raw_values = [1, "2", "high", 4, None, " 3 ", 9]
'''

raw_values = [1, "2", "high", 4, None, " 3 ", 9]
valid = []
errors = []

for value in raw_values:
    try:
        priority = parse_priority(value)
    except ValueError as e:
        errors.append(str(e))
    else:
        valid.append(priority)

print(f"Valid: {valid}")
print(f"{len(errors)} errors:")
for message in errors:
    print(f"  - {message}")
