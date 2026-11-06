"""A graph workflow: Python code routes each question to the right specialist agent."""
import re

from google.adk import Event, Workflow

from policy_qa.agent import root_agent as policy_qa_agent
from service_desk.agent import root_agent as service_desk_agent

TICKET_NUMBER = re.compile(r"\b\d{4}\b")
SERVICE_DESK_PHRASES = ("ticket", "bank holiday", "network", "hardware", "accounts")


def route_question(node_input: str) -> Event:
    """Route ticket, IT service and bank holiday questions to the service desk, the rest to policy."""
    text = node_input.lower()
    if TICKET_NUMBER.search(text) or any(p in text for p in SERVICE_DESK_PHRASES):
        return Event(output=node_input, route="service_desk")
    return Event(output=node_input, route="policy")


root_agent = Workflow(
    name="staff_workflow",
    edges=[
        ("START", route_question, {
            "service_desk": service_desk_agent.clone(update={"mode": "single_turn"}),
            "policy": policy_qa_agent.clone(update={"mode": "single_turn"}),
        }),
    ],
)
