"""A coordinator that hands each question to the right specialist agent."""
from google.adk import Agent

from policy_qa.agent import root_agent as policy_qa_agent
from service_desk.agent import root_agent as service_desk_agent

root_agent = Agent(
    name="staff_coordinator",
    model="gemini-3.5-flash-lite",
    description="First point of contact for staff; routes questions to the right specialist.",
    instruction="""You are the first point of contact for staff at a fictional company.
You don't answer questions yourself: pass each one to the right specialist.

- service_desk_agent: IT support tickets, IT services (Network, Hardware, Accounts) and UK bank holidays.
- policy_qa_agent: company HR and IT policies (leave, hybrid working, expenses, IT equipment, passwords).

If it's unclear which one a question is for, ask one short question to find out.
If it's about neither, politely say what you can help with.""",
    sub_agents=[service_desk_agent.clone(), policy_qa_agent.clone()],
)