# HowToSetup.md

## Requirements

- Python 3.10+
- pip

## Installation

1. Copy the project folder.
2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Copy the environment file:

```bash
cp .env.example .env              # Windows: copy .env.example .env
```

4. (Optional) Edit `.env` to change the admin password or business name.

5. Initialize the database:

```bash
python -m app.init_db
```

6. Start the server:

```bash
python main.py
```

7. Open http://localhost:8000

## First-time Admin Setup (required)

1. Visit http://localhost:8000/admin/login
2. Log in with the username and password from `.env` (default `admin` / `admin123`)
3. Go to **Settings** and enter:
   - **AI Base URL** — example: `https://api.groq.com/openai/v1`
   - **AI API Key** — your own key from the AI provider
   - **AI Model** — example: `openai/gpt-oss-20b`
   - **Business Name**
4. Click **Save Settings**
5. Go to **Knowledge** and add FAQs the AI should use

The AI Base URL, API Key, and Model are configured only from the Admin panel. They are stored in the database and take effect immediately.

## Change Admin Password

In **Admin → Settings**, use the **Change Admin Password** form.

## Render (demo hosting)

1. Push this folder to GitHub (the folder that contains `app/` and `main.py` must be the repo root).
2. On Render, create a Web Service from that repo.
3. Settings:
   - Python version: **3.12** (or use the included `runtime.txt`)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy, then open `/admin/login` and set the AI key in Settings.

Use `main:app`, not `app:app`.

## Production Notes

- Change `SECRET_KEY` and the admin password before going live
- Use a reverse proxy (Nginx) and HTTPS
- The SQLite database file (`ai_receptionist.db`) is created automatically
- Do not commit or share your real `.env` or API keys


| Provider | AI Base URL | Example Model |
|----------|-----------------------------|-------------------------|
| **Groq** | https://api.groq.com/openai/v1 | `openai/gpt-oss-20b` |
| **OpenAI** | https://api.openai.com/v1 | `gpt-4o-mini` |
| **OpenRouter** | https://openrouter.ai/api/v1 | `google/gemini-flash-1.5` |
| **Together AI** | https://api.together.xyz/v1 | Various open models |
| **Local (Ollama)** | http://localhost:11434/v1 | `llama3.2` |

