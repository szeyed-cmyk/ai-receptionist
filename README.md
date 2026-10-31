# AI Receptionist

Self-hosted AI Receptionist with a knowledge base, appointment booking, and admin dashboard.

Built for Vibe96-style distribution. The customer configures their own AI provider from the admin panel.

## Features

- Web chat interface
- Admin dashboard
- Knowledge base (FAQs the AI uses)
- Appointment booking with conflict detection (60-minute slots)
- AI settings configured from the Admin panel (Base URL, API Key, Model)
- Works with any OpenAI-compatible provider (Groq, OpenAI, OpenRouter, etc.)
- SQLite database (no external database required)

## Quick Start

```bash
cd ai-receptionist
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m app.init_db
python main.py
```

Open:
- Chat: http://localhost:8000
- Admin: http://localhost:8000/admin/login  
  Default login: `admin` / `admin123`

## Configure AI (required)

After starting the app:

1. Go to **Admin → Settings**
2. Enter:
   - **AI Base URL** (example: `https://api.groq.com/openai/v1`)
   - **AI API Key** (your own key)
   - **AI Model** (example: `openai/gpt-oss-20b`)
   - **Business Name**
3. Click **Save Settings**

The values are stored in the database. The chat will use them immediately. No API keys are required in the `.env` file.

## Project Structure

```
ai-receptionist/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── ai_service.py
│   └── routes.py
├── templates/
├── main.py
├── requirements.txt
├── .env.example
└── HowToSetup.md
```

## License

Single-site licence style — intended for sale on marketplaces such as Vibe96.
