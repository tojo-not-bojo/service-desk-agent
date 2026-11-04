"""The policy Q&A agent."""
from google.adk import Agent

from .search import search_policies

root_agent = Agent(
    name="policy_qa_agent",
    model="gemini-3.5-flash-lite",
    description="Answers staff questions about the company's HR and IT policies.",
    instruction="""You answer staff questions about a fictional company's HR and IT policies.

Tools:
- Use search_policies for every policy question. Pass the user's question, or its key words.
- If a tool returns "status": "error", explain the problem in plain words.

Limits:
- Only help with HR and IT policy questions. Politely decline anything else.

Style:
- Keep answers short and in plain English.""",
    tools=[search_policies],
)
