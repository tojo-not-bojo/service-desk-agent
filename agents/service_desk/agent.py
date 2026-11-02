"""The service desk agent."""
from google.adk import Agent

root_agent = Agent(
    name="service_desk_agent",
    model="gemini-flash-latest",
    description="Answers staff questions about IT service desk tickets and services.",
    instruction="You are a helpful IT service desk assistant for staff.",
)