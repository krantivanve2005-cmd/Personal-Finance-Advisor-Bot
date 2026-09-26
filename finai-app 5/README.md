# FinAI — Personal Finance Advisor Bot

An AI-powered personal finance management app: expense tracking, budgeting,
savings goals, analytics, and an AI financial advisor chat. Frontend is
Flask + Jinja2; backend is Flask + SQLAlchemy + Flask-Login, ready to run
on SQLite locally or PostgreSQL in production.

## Folder structure

```
finai-app/
├── app.py              # App factory, registers blueprints, creates tables
├── config.py           # Reads settings from environment (.env)
├── extensions.py       # db, login_manager, csrf singletons
├── models.py           # User, Income, Expense, ExpenseCategory, Budget,
│                        # SavingsGoal, MonthlyReport, AIRecommendation
├── ai_service.py        # OpenAI / Gemini integration + offline fallback
├── seed.py              # Seeds demo data (Priya, ₹60,000 income, etc.)
├── requirements.txt
├── .env.example         # Copy to .env and fill in secrets
├── routes/
│   ├── auth.py           # /login, /register, /logout
│   ├── main.py            # /, /dashboard, /transactions, /savings + forms
│   └── ai.py               # /advisor page + /api/advisor/ask (JSON)
├── templates/
│   ├── base.html            # <head>, flash messages, shared shell
│   ├── landing.html           # Public marketing/landing page
│   ├── login.html / register.html
│   ├── app_base.html           # Sidebar + topbar for logged-in pages
│   ├── dashboard.html            # Summary cards, charts, budget bars, AI insight
│   ├── transactions.html           # Table + search/filter + add income/expense modals
│   ├── savings.html                 # Savings goal cards + create-goal modal
│   └── advisor.html                  # AI chat interface
└── static/
    ├── css/style.css
    └── js/main.js
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env             # then edit .env: set SECRET_KEY, optional API keys
python seed.py                   # creates finai.db with demo data
python app.py                    # runs on http://127.0.0.1:5000
```

Demo login (after `seed.py`): **priya@email.com / password123**

## Connecting a real AI provider

`ai_service.py` reads `OPENAI_API_KEY` or `GEMINI_API_KEY` from the environment
(never hardcoded). If neither is set, the AI Advisor still works, using a
rule-based offline response, so the app is fully demoable without any key.

## Database

Default is SQLite (`finai.db`, created automatically). To use PostgreSQL,
set `DATABASE_URL=postgresql://user:pass@host:5432/finai` in `.env` —
SQLAlchemy models require no changes.

## Security notes implemented in this scaffold

- Passwords hashed with Werkzeug's `generate_password_hash` (never stored in plaintext)
- Flask-Login for session-based authentication; `@login_required` protects all financial routes
- Flask-WTF CSRF protection enabled globally, including the AI chat's fetch() calls (`X-CSRFToken` header)
- Secrets (`SECRET_KEY`, API keys, database URL) read from environment variables via `.env`, never committed (see `.gitignore`)
- Each query filters by `current_user.id`, so users can only see their own financial data

For production, also add: HTTPS-only cookies, rate limiting on `/api/advisor/ask`,
input validation with a form library (e.g. WTForms), and a proper migrations
tool (Flask-Migrate/Alembic) instead of `db.create_all()`.

## Exposing the demo with ngrok

```bash
python app.py                 # start Flask locally on port 5000
ngrok http 5000                # in a second terminal
```

Flow: **User Browser → Ngrok Public URL → Flask App → Auth/Financial routes
→ SQLAlchemy → SQLite/PostgreSQL**, with AI requests going
**Flask → OpenAI/Gemini API → AI response → Dashboard/AI Advisor**.

## Disclaimer

FinAI provides AI-generated financial insights for educational and
informational purposes only. It does not provide professional financial,
investment, tax, or legal advice.
