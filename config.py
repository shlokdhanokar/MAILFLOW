"""
MAILFLOW — Centralized Configuration
Reads all settings from environment variables via python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()


# ── Gmail Credentials ────────────────────────────────────────────────
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")

# ── MySQL Database ───────────────────────────────────────────────────
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "email_tickets"),
}

# ── Google Gemini API ────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ── Flask API ────────────────────────────────────────────────────────
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
FLASK_API_URL = f"http://{FLASK_HOST}:{FLASK_PORT}/predict"

# ── Classification Labels ───────────────────────────────────────────
CATEGORY_LABELS = [
    "Technical Issue",
    "Billing Issue",
    "Account Issue",
    "General Inquiry",
]

# ── Department Email Mappings ────────────────────────────────────────
DEPARTMENT_EMAILS = {
    "Technical Issue": "technical.mailflow@gmail.com",
    "Billing Issue": "payment.mailflow@gmail.com",
    "Account Issue": "auth.mailflow@gmail.com",
    "General Inquiry": "general.mailflow@gmail.com",
}

# ── BERT Model Path ─────────────────────────────────────────────────
BERT_MODEL_PATH = os.getenv("BERT_MODEL_PATH", "email_bert_model")
