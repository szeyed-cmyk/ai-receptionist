# CLAUDE.md

## Project

FrontDesk AI — self-hosted AI receptionist. Customers chat, get answers from a knowledge base, and book appointments.

## Stack

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Jinja2
- OpenAI-compatible AI (Groq, OpenAI, etc.)

## Layout

```
app/            FastAPI application
templates/      HTML pages
database/       schema.sql and seed.sql (reference only)
main.py         entry point
requirements.txt
```

## Conventions

- AI Base URL, API Key, and Model are set in Admin → Settings and stored in the database.
- Do not hardcode API keys.
- Business hours, closed days, and holiday dates are set in Admin → Settings.
- Appointments are 60-minute slots. Overlap and duplicate phone numbers are rejected.
- SQLite file is created automatically on startup. The SQL files are for documentation.

## Do not

- Ship `.env` or `ai_receptionist.db` with real keys.
- Include `venv` or `__pycache__` in the release ZIP.
