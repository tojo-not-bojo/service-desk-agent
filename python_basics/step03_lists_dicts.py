
'''

# lists

services = ["Network", "Hardware", "Accounts"]

services[0]           # "Network": positions start at 0
services[-1]          # "Accounts": negative positions count from the end
services[0:2]         # ["Network", "Hardware"]: a slice; the end position is excluded
services.append("Email")   # add an item to the end
len(services)         # 4
"Email" in services   # True
sorted(services)      # a new, sorted copy; services.sort() sorts the list itself instead


# dictionaries

ticket = {"id": 1042, "title": "VPN not connecting", "priority": 2}

ticket["title"]                    # "VPN not connecting"
ticket["status"] = "open"          # add a key, or update it if it already exists
ticket["owner"]                    # KeyError: crashes if the key doesn't exist
ticket.get("owner")                # None: no crash
ticket.get("owner", "Unassigned")  # use a default instead of None
"title" in ticket                  # True: `in` checks the keys

for key, value in ticket.items():  # loop over key/value pairs
    print(f"{key} = {value}")

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}
SLA_HOURS[2]   # 8


#list of dicts is a table

tickets = [
    {"id": 1041, "status": "open", "hours_open": 5.0},
    {"id": 1042, "status": "resolved", "hours_open": 1.0},
]



SQL	Python
SELECT * FROM tickets	for t in tickets:
WHERE status = 'open'	if t["status"] == "open":
SELECT id FROM tickets WHERE …	[t["id"] for t in tickets if …]
COUNT(*)	len(...)
ORDER BY hours_open DESC	sorted(tickets, key=lambda t: t["hours_open"], reverse=True)
TOP 3	[:3]
GROUP BY	build up a dict of totals in a loop
Look up by primary key	a dict keyed by ID


#group by

counts = {}
for t in tickets:
    s = t["status"]
    counts[s] = counts.get(s, 0) + 1   # start at 0 if this group hasn't been seen yet
# {"open": 1, "resolved": 1}

'''
  
tickets = [
    {"id": 1041, "title": "Laptop won't boot", "priority": 1, "status": "open", "hours_open": 5.0, "assigned_to": "Priya", "service": "Hardware"},
    {"id": 1042, "title": "VPN not connecting", "priority": 2, "status": "open", "hours_open": 5.5, "assigned_to": None, "service": "Network"},
    {"id": 1043, "title": "Password reset", "priority": 3, "status": "resolved", "hours_open": 1.0, "assigned_to": "Sam", "service": "Accounts"},
    {"id": 1044, "title": "Wi-Fi drops in office", "priority": 2, "status": "open", "hours_open": 12.0, "assigned_to": "Priya", "service": "Network"},
    {"id": 1045, "title": "New starter account", "priority": 4, "status": "open", "hours_open": 30.0, "assigned_to": None, "service": "Accounts"},
    {"id": 1046, "title": "Printer jam", "priority": 3, "status": "open", "hours_open": 26.0, "assigned_to": "Sam", "service": "Hardware"},
]

'''
List basics. Create services = ["Network", "Hardware", "Accounts"].
Print the first and last items.
Append "Email", then print the length.
Print whether "Printing" is in the list.
Print the list sorted.
'''
services = ["Network", "Hardware", "Accounts"]
print(services[0], services[-1])      # Network Accounts
services.append("Email")
print(len(services))                  # 4
print("Printing" in services)         # False
print(sorted(services))               # ['Accounts', 'Email', 'Hardware', 'Network']

'''
SLA lookup. Create the SLA_HOURS dict.
Print the SLA for priority 2.
Print the SLA for priority 5, using a default of 72 so it doesn’t crash.
Loop over the dict and print each line as P1: 4h.
'''

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}
print(SLA_HOURS[2])           # 8
print(SLA_HOURS.get(5, 72))   # 72
for priority, hours in SLA_HOURS.items():
    print(f"P{priority}: {hours}h")
    
'''
Table basics.
Print how many tickets there are, the title of the first ticket and the ID of the last.
Get the IDs of all open tickets twice: once with a for loop and .append(), once with a list comprehension.
With a list comprehension, get the IDs of tickets that are open and unassigned.
'''

'''
Breach flag.
For every ticket, add a "breached" key: True if the ticket is open and hours_open is over its SLA, otherwise False.
For each open ticket, print a line like 1041: P1, 5.0h of 4h -> BREACHED.
Then print the list of breached IDs.
'''

'''
GROUP BY. For open tickets only, print the number of tickets and the total hours per service, like Hardware: 2 open, 31.0h total.
'''

'''
ORDER BY / TOP. Print the 3 open tickets that have been open longest, longest first, like 1045: New starter account (30.0h).
'''

'''
Primary-key lookup.
Build tickets_by_id, a dict mapping each ID to its ticket. A dict comprehension looks like {key: value for t in tickets}.
Look up 1043 and print Ticket 1043: Password reset (resolved).
Look up 9999 and print Ticket 9999 not found, without crashing.
'''