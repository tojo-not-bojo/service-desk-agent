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


import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

'''
1. Export the data. Create python_basics/step05_export.py. Paste in the tickets list and the SERVICES dict from step 4, then:

Create the data/ folder if it doesn’t exist: DATA_DIR.mkdir(exist_ok=True).
Write data/tickets.json and data/services.json with indent=2.
Run it once, then open both files in VS Code and look at them. What happened to None?

From here on, the files are the source of truth, and you won’t need the hard-coded lists again.
'''

# step05_export.py (paste tickets and SERVICES above this)
DATA_DIR.mkdir(exist_ok=True)

with open(DATA_DIR / "tickets.json", "w", encoding="utf-8") as f:
    json.dump(tickets, f, indent=2)

with open(DATA_DIR / "services.json", "w", encoding="utf-8") as f:
    json.dump(SERVICES, f, indent=2)


'''
2. Read it back. In a new file, python_basics/step05_json.py:

Load both files.
Print how many tickets there are, the type of tickets and the type of tickets[0].
Print whether ticket 1042’s assigned_to came back as None.
Print the list of service names.
'''

with open(DATA_DIR / "tickets.json", encoding="utf-8") as f:
    tickets = json.load(f)

with open(DATA_DIR / "services.json", encoding="utf-8") as f:
    services = json.load(f)

print(len(tickets), type(tickets), type(tickets[0]))   # 6 <class 'list'> <class 'dict'>
print(tickets[1]["assigned_to"] is None)               # True
print(list(services))                                  # ['Network', 'Hardware', 'Accounts']

'''
3. Nested data. Save this as data/ticket_history_1044.json:

json
{
  "ticket_id": 1044,
  "title": "Wi-Fi drops in office",
  "status": "open",
  "requester": {
    "name": "Jordan Lee",
    "email": "jordan.lee@example.com",
    "department": "Finance",
    "location": {"site": "Leeds", "floor": 3}
  },
  "tags": ["wifi", "intermittent", "office"],
  "updates": [
    {"timestamp": "2026-10-28T09:15:00", "author": "Jordan Lee", "note": "Wi-Fi keeps dropping every 10 minutes on floor 3."},
    {"timestamp": "2026-10-28T11:40:00", "author": "Priya", "note": "Access point AP-3B is restarting repeatedly."},
    {"timestamp": "2026-10-28T16:05:00", "author": "Priya", "note": "Firmware update scheduled for tomorrow morning."}
  ],
  "sla": {"priority": 2, "target_hours": 8, "breached": true}
}

Load it and print:

the requester’s name and department, as Jordan Lee (Finance)
the floor they’re on
how many updates there are
the note on the latest update
the distinct authors, in the order they first appear
whether the SLA is breached (check what true became)
the requester’s phone number, or No phone on record, without crashing
the resolution summary, or Not resolved yet, without crashing
'''

with open(DATA_DIR / "ticket_history_1044.json", encoding="utf-8") as f:
    history = json.load(f)

requester = history["requester"]
print(f"{requester['name']} ({requester['department']})")   # Jordan Lee (Finance)
print(requester["location"]["floor"])                       # 3
print(len(history["updates"]))                              # 3
print(history["updates"][-1]["note"])                       # Firmware update scheduled for tomorrow morning.

authors = []
for update in history["updates"]:
    if update["author"] not in authors:
        authors.append(update["author"])
print(authors)                                              # ['Jordan Lee', 'Priya']

print(history["sla"]["breached"])                           # True
print(requester.get("phone", "No phone on record"))         # No phone on record
print(history.get("resolution", {}).get("summary", "Not resolved yet"))   # Not resolved yet

'''
4. Update and save.

Append a new update: author Priya, timestamp 2026-10-29T08:30:00, note Firmware updated on AP-3B. Monitoring.
Set status to "monitoring".
Write the file back, then reload it and print the number of updates and the status.
Run the script twice. What goes wrong, and how would you prevent it?
'''

path = DATA_DIR / "ticket_history_1044.json"

with open(path, encoding="utf-8") as f:
    history = json.load(f)

new_update = {"timestamp": "2026-10-29T08:30:00", "author": "Priya", "note": "Firmware updated on AP-3B. Monitoring."}
history["updates"].append(new_update)
history["status"] = "monitoring"

with open(path, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2)

with open(path, encoding="utf-8") as f:
    reloaded = json.load(f)
print(len(reloaded["updates"]), reloaded["status"])   # 4 monitoring

'''
5. The string-keys trap.

Build tickets_by_id = {t["id"]: t for t in tickets}.
Convert it to a JSON string with json.dumps, then load it back with json.loads.
Try looking up 1044 in the result. What happens, and why?
Fix it.
'''

tickets_by_id = {t["id"]: t for t in tickets}
back = json.loads(json.dumps(tickets_by_id))

print(list(back)[:2])     # ['1041', '1042']: the keys are now strings
# back[1044]              # KeyError: 1044
print(back["1044"]["title"])                     # works, but awkward

fixed = {int(k): v for k, v in back.items()}     # convert the keys back to int
print(fixed[1044]["title"])                      # Wi-Fi drops in office

'''
6. A loader for the tools.

Write load_json(filename: str) -> list | dict, which loads any file from DATA_DIR. Give it a docstring.
Copy get_sla_hours, is_breached and get_ticket_status from step 4, and have them use tickets loaded with load_json("tickets.json").
Check that get_ticket_status(1044) gives the same result as before.
'''

def load_json(filename: str) -> list | dict:
    """Load and return the contents of a JSON file from the data folder.

    Args:
        filename: Name of the file inside data/, for example "tickets.json".

    Returns:
        The parsed JSON, usually a list of records or a dict.
    """
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}
TICKETS = load_json("tickets.json")
TICKETS_BY_ID = {t["id"]: t for t in TICKETS}

# get_sla_hours, is_breached and get_ticket_status: exactly as in step 4

print(get_ticket_status(1044))