'''
Where modules live.
Import math three ways: import math, from math import sqrt and import math as m. Print the square root of 16 using each.
Print json.__file__ and requests.__file__. Which one is inside your .venv, and why?
'''

import json
import math
import math as m
from math import sqrt

import requests

print(math.sqrt(16), sqrt(16), m.sqrt(16))   # 4.0 4.0 4.0
print(json.__file__)       # C:\...\Python3xx\Lib\json\__init__.py
print(requests.__file__)   # C:\...\service-desk-agent\.venv\Lib\site-packages\requests\__init__.py

'''
Write a class. Create a Ticket class with:
__init__(self, ticket_id, title, priority, status="open", hours_open=0.0)
sla_hours(), which uses the SLA_HOURS dict
is_breached()
add_hours(hours), which increases hours_open
to_dict(), which returns the ticket as a dict like the ones in tickets.json
Then:
Create Ticket(1042, "VPN not connecting", 2, hours_open=5.5) and Ticket(1046, "Printer jam", 3, hours_open=26.0), and print is_breached() for each.
Add 3 hours to the VPN ticket, then print its hours and is_breached() again.
'''

SLA_HOURS = {1: 4, 2: 8, 3: 24, 4: 72}


class Ticket:
    """A single service desk ticket."""

    def __init__(self, ticket_id: int, title: str, priority: int,
                 status: str = "open", hours_open: float = 0.0):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = status
        self.hours_open = hours_open

    def sla_hours(self) -> int:
        """Return the SLA target in hours for this ticket's priority."""
        return SLA_HOURS.get(self.priority, 72)

    def is_breached(self) -> bool:
        """Return True if the ticket is open and past its SLA."""
        return self.status == "open" and self.hours_open > self.sla_hours()

    def add_hours(self, hours: float) -> None:
        """Increase the time this ticket has been open."""
        self.hours_open += hours

    def to_dict(self) -> dict:
        """Return the ticket as a plain dict, matching the format of tickets.json."""
        return {
            "id": self.ticket_id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "hours_open": self.hours_open,
        }


vpn = Ticket(1042, "VPN not connecting", 2, hours_open=5.5)
printer = Ticket(1046, "Printer jam", 3, hours_open=26.0)
print(vpn.is_breached(), printer.is_breached())   # False True

vpn.add_hours(3)
print(vpn.hours_open, vpn.is_breached())          # 8.5 True
print(vpn.to_dict())

'''
Async timing. Write async def fake_api_call(name, seconds) that waits with await asyncio.sleep(seconds), then returns f"{name} done".
Time three 1-second calls run one after another with await.
Time the same three calls with asyncio.gather.
Then call fake_api_call("oops", 1) without await and print the result. What do you get?
time.perf_counter() gives a precise timestamp for measuring how long something takes.
'''

import asyncio
import time


async def fake_api_call(name: str, seconds: float) -> str:
    """Pretend to call an API that takes `seconds` to respond."""
    await asyncio.sleep(seconds)
    return f"{name} done"


async def run_sequential() -> None:
    start = time.perf_counter()
    for name in ["tickets", "services", "holidays"]:
        print(await fake_api_call(name, 1))
    print(f"Sequential: {time.perf_counter() - start:.1f}s")


async def run_concurrent() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        fake_api_call("tickets", 1),
        fake_api_call("services", 1),
        fake_api_call("holidays", 1),
    )
    print(results)
    print(f"Concurrent: {time.perf_counter() - start:.1f}s")


asyncio.run(run_sequential())
asyncio.run(run_concurrent())
print(fake_api_call("oops", 1))

'''
Make the tools a package. This is the Phase 1 outcome. Create the folder agents/service_desk/ with three files:
__init__.py: leave it empty for now.
data_loader.py: DATA_DIR and the load_json function from step 6. Here DATA_DIR needs to be Path(__file__).resolve().parents[2] / "data"; work out why.
tools.py: SLA_HOURS, the loaded data, get_sla_hours, is_breached, get_ticket_status (the step 6 version) and get_service_details (from step 4). Import load_json with from .data_loader import load_json. Add a __main__ block that tests both tools.
Then run it two ways and compare what happens:
python agents/service_desk/tools.py, from the repo root
cd agents, then python -m service_desk.tools
'''

