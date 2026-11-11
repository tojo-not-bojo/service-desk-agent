# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

A learning project: going from Python basics to building, testing, deploying and monitoring AI agents with Google's Agent Development Kit (ADK). It contains two agents built around a fictional company:

- **service_desk**: an IT service desk assistant with tools for tickets, IT services and UK bank holidays.
- **policy_qa**: a question-and-answer agent over synthetic HR and IT policy documents (retrieval-augmented generation).

All data is synthetic. The repo is public and is part of my portfolio, so the commit history should show steady progress through the plan below.

## How to work with me

I'm learning, so the goal is for me to understand and write the code, not just to end up with working code.

- **Explain, then let me do it.** For each new step: a short, precise explanation of the concept, then exercises that I write and run myself. Include the solutions with the exercises, after the questions.
- **Don't write or edit my files unless I ask.** When I paste or point to code or an error, review it: say what's wrong, why, and how to fix it. Suggest improvements.
- **Explain commands the first time they appear**, briefly. Assume I may not have seen them before; I pick things up quickly, so keep explanations short.
- **Use examples.** I learn well from seeing things in action: basics first, then applied.
- **No comparisons to SQL.** I have a SQL background, but I don't want concepts explained through it.
- **Keep it practical.** Only the theory needed for the task in front of me.
- **Check current documentation.** ADK and Google Cloud's agent products change quickly and were renamed in 2026 (e.g. Agent Engine is now Agent Runtime). Verify commands, package names and APIs against current docs (adk.dev, docs.cloud.google.com) rather than memory.
- **Ask before running anything that changes things**: installing packages, deleting files, git operations, anything touching Google Cloud.
- **Never print, read out or copy the contents of any `.env` file.**

## Environment

- Windows, PowerShell, VS Code.
- Python 3.14 in a virtual environment at `.venv` (activate with `.venv\Scripts\Activate.ps1`).
- ADK Python 2.x (`google-adk`). Dependencies are in `requirements.txt` (`pip freeze > requirements.txt` after installing anything).
- Model: `gemini-3.5-flash-lite` via the Gemini API with an AI Studio key (free tier). The `gemini-flash-latest` alias was often overloaded (503 errors), so avoid it.
- Each agent folder has its own `.env` containing `GOOGLE_GENAI_USE_VERTEXAI=FALSE` and `GOOGLE_API_KEY=...`.
- `python_basics/list_models.py` lists the models the key can use; `python_basics/test_gemini.py` tests the key and connection without ADK.

### Running things

- Start the dev UI with `adk web --port 8000` and the terminal chat with `adk run <agent_folder>`, run from `agents/`.
- `adk web` stores sessions in `<agent_folder>/.adk/session.db` by default, so sessions and `user:` state survive restarts.
- Run package modules with `python -m <package>.<module>` from `agents/` (e.g. `python -m policy_qa.documents`). Running a file directly breaks relative imports.
- Restart `adk web` after changing agent code.

## Repo structure

```
service-desk-agent/
├── README.md
├── CLAUDE.md
├── requirements.txt
├── data/
│   ├── tickets.json, services.json, ticket_history_1044.json
│   └── policies/                  # synthetic policy documents (.md), one chunk per "## " section
├── python_basics/                 # Phase 1 exercises (step02 … step08) and API test scripts
└── agents/
    ├── service_desk/
    │   ├── __init__.py            # from . import agent
    │   ├── agent.py               # root_agent
    │   ├── tools.py               # get_ticket_status, get_service_details, save_user_details
    │   ├── holidays.py            # get_next_bank_holiday (GOV.UK feed with local cache)
    │   └── data_loader.py         # DATA_DIR, load_json
    └── policy_qa/
        ├── __init__.py            # "from . import agent" commented out until agent.py exists
        ├── documents.py           # load_chunks
        ├── search.py              # keyword_search, semantic_search, search_policies (in progress)
        └── agent.py               # not yet written
```

Planned later: `tests/`, `evals/`, `mcp_server/`, `infra/` (Terraform), `.github/workflows/`, `docs/`.

## Code conventions

- **Tools are plain functions** with type hints and Google-style docstrings (`Args:`, `Returns:`). The model only sees the name, type hints and docstring, so write docstrings for a reader who can't see the code.
- **Tools return a dict with a `"status"` key** (`"success"` or `"error"`). Error messages say what went wrong and, where possible, list valid options so the model can retry.
- **Expected problems** (bad input, not found) return an error dict. **Unexpected failures** (network, bugs) raise, so ADK 2.0's retry handling can see them. Never use a broad `except Exception:` inside a tool.
- **Don't expose internal settings as tool parameters** (e.g. URLs), and never let the model choose whose data a tool touches (no `user_id` parameters).
- **State:** tools take `tool_context: ToolContext` to read and write state. Update lists and dicts by reading, copying and assigning back. Prefixes: none = session, `user:` = all of a user's sessions, `app:` = all users, `temp:` = current turn only. Use `{key?}` in instructions for keys that may not exist.
- **Paths** are built from the file's location: `Path(__file__).resolve().parents[n]`, never relative to the working directory.
- **Files** are opened with `encoding="utf-8"`. JSON keys come back as strings.
- **Create files in VS Code**, not with `echo` in PowerShell (encoding problems).

## Rules

- **Synthetic data only.** No real company, client or personal data anywhere in the repo.
- **No employer, client or internal system names** in anything committed. Keep everything generic.
- **No secrets in Git.** `.gitignore` must cover `.venv/`, `.env`, `__pycache__/`, `.adk/`, `*.db`, `data/*_cache.json` and `data/*_embeddings.json`. Check `git status` before every commit.
- **Google Cloud (from Phase 4):** budget alerts on, least-privilege service accounts, and clean up deployed resources after each exercise.
- **Commit and push at the end of every step**, with a message like `Step 13: …`.

## Progress

### Phase 1: Python foundations (done)

1. Setup: terminal, venv, pip, VS Code, Git, GitHub, `.env` and `.gitignore`
2. Core syntax
3. Lists and dictionaries
4. Functions, type hints, docstrings, tool-style return values
5. JSON files and nested data
6. Error handling
7. Calling APIs with `requests` (GOV.UK bank holidays, Open-Meteo)
8. Reading code: imports, modules, classes, async; tools moved into a package

### Phase 2: Building agents with ADK (in progress)

9. What an agent is (done)
10. First agent, instructions, `adk web` (done)
11. Tools: ticket, service and bank holiday tools wired in (done)
12. Sessions and state: `save_user_details` (`user:` state) and `viewed_tickets` (session state) (done; still confirming `viewed_tickets` appears in state)
13. **Policy Q&A, part 1 (current):** synthetic policy documents, chunking, keyword search, semantic search with embeddings, `search_policies` tool, basic agent. Currently on chunking: `load_chunks()` returned 0 chunks; checking the folder location, file extensions and leading spaces in the files.
14. Policy Q&A, part 2: answering only from sources, citations, saying "I don't know" (e.g. a score threshold), fixing the parental-leave false match
15. Multiple agents: triage routing vs one agent with several tools vs an ADK 2.0 graph workflow
16. Agents CLI: scaffold a project with Google's Agents CLI (RAG template) and compare it with this repo

### Phase 3: Making agents safe and testable

17. Controls: input validation, permission checks in code, unsupported actions, safe logging
18. Attack testing: prompt injection, other users' data, bad arguments, instructions hidden in tool results and documents
19. Evaluation: ~20 test cases with `adk eval`, pytest unit tests for tools, answer-quality scoring for policy Q&A, results before and after a change

### Phase 4: Platform engineering

20. Google Cloud hands-on: projects, APIs, IAM, least-privilege service accounts, budget alert
21. Deploy to Agent Runtime, call it remotely, check its identity, clean up
22. Observability: Cloud Logging and Trace, export to BigQuery, queries for latency, errors, tool failures and cost
23. Model endpoint: point the agent at a non-default model endpoint (gateway-style setup)
24. CI/CD: GitHub Actions running tests and evals before deploy; Terraform refresher
25. MCP: a small MCP server over synthetic data, connected to the agent

### Phase 5: Wrap-up

26. Portfolio README: setup, diagrams, evaluation results, limitations
27. Questions to ask a platform team about their agent standards and templates
28. Practise explaining the agent's execution path, security boundaries and evaluation evidence

**Priorities if time runs short:** Phases 1–2 and steps 20–22 are essential; Phase 3 is strongly recommended; steps 23–25 are stretch goals.
