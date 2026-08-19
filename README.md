# BankSwift — Full-Stack Banking Web App

A working banking application inspired by the Kotak Mahindra Bank app UI, built with **Django** (backend + server-rendered UI) and **SQLite/PostgreSQL**. Includes real money-transfer logic, transaction history, dashboard, and a rule-based chatbot assistant. Ready to deploy on **Render**.

## Features

- **User Authentication** — Register / Login / Logout (Django auth), each new user gets a demo account with ₹5,000 balance, a unique 14-digit account number, IFSC code, and UPI ID.
- **Transfer Money** — Send money to another BankSwift user by account number or username. Uses atomic DB transactions with row-level locking (`select_for_update`) so balances can never go negative or double-spend under concurrent requests.
- **Transaction History** — Full paginated history with Sent / Received filters, and a receipt-style detail page for every transaction.
- **Dashboard** — Kotak-style balance card, quick actions, recent transactions, and a mini summary.
- **Chatbot** — Rule-based "BankSwift Assistant" widget (bottom-right bubble) that answers balance, transfer, transaction, and account queries using the logged-in user's real data. Backed by a JSON API endpoint (`/api/chatbot/`) that's easy to swap for a real LLM later.
- **Kotak-style UI** — Maroon/red gradient theme, card-based layout, mobile responsive.

## Tech Stack

- Backend: Django 6 (Python)
- Database: SQLite locally, PostgreSQL on Render (via `dj-database-url`)
- Frontend: Django templates + vanilla CSS/JS (no build step needed — works everywhere, no Node required)
- Static files: WhiteNoise (serves static files directly from Django in production)
- Deployment: Render (`render.yaml` blueprint included)

## Project Structure

```
BankSwift/
├── accounts/          # User registration, login, profile, Profile model (account no., balance)
├── banking/           # Transfers, transaction history, chatbot API
├── bankswift/         # Django project settings/urls
├── templates/          # HTML templates (Kotak-style UI)
├── static/             # CSS + JS (chatbot widget)
├── requirements.txt
├── render.yaml         # Render blueprint (web service + free Postgres DB)
├── build.sh            # Render build script (migrate + collectstatic)
└── manage.py
```

## Run Locally

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate      # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. (Optional) Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```

4. Start the dev server:
   ```bash
   python manage.py runserver
   ```

5. Open **http://127.0.0.1:8000/accounts/register/** and create an account. Register a second account in an incognito window to test transfers between two users.

## Deploy on Render

**Option A — One-click Blueprint (recommended)**
1. Push this project to a GitHub repo.
2. On Render, click **New → Blueprint**, connect your repo. Render will read `render.yaml` and automatically create:
   - a free PostgreSQL database (`bankswift-db`)
   - a web service running `gunicorn bankswift.wsgi:application`
3. Render auto-generates `SECRET_KEY` and wires up `DATABASE_URL`. Click **Apply** and wait for the build to finish.
4. Once live, visit `https://<your-service>.onrender.com/accounts/register/`.

**Option B — Manual Web Service**
1. New → Web Service → connect repo.
2. Build command: `./build.sh`
3. Start command: `gunicorn bankswift.wsgi:application`
4. Add environment variables: `SECRET_KEY` (any random string), `DEBUG=False`.
5. Attach a PostgreSQL database and set `DATABASE_URL` (or leave unset to fall back to SQLite — not recommended for production since Render's disk is ephemeral on restarts).

## Notes on the Chatbot

The chatbot (`banking/chatbot.py`) is a lightweight rule/keyword-based assistant — no external API key needed, so it works out of the box on Render's free tier. It personalizes responses using the logged-in user's real balance and account details. If you'd like to upgrade it to a real LLM (e.g. Claude API), you only need to replace the `get_bot_response()` function in `banking/chatbot.py` with an API call — the frontend widget and `/api/chatbot/` endpoint don't need to change.

## Security Notes (demo app)

This is a learning/demo project, not production-grade banking software. Before using it for anything real, you'd want to add: OTP/2FA on login and transfers, rate limiting, password reset via email, audit logging, HTTPS enforcement, and a real KYC flow.
