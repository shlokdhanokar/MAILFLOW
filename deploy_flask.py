"""
MAILFLOW — Flask API & Dashboard Server
Serves the dashboard UI and provides API endpoints for:
  - Email classification & forwarding  (POST /predict)
  - Ticket listing                      (GET  /api/tickets)
  - Dashboard statistics                (GET  /api/stats)
"""

import os
import sys
import json
import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from flask import Flask, request, jsonify, render_template
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Ensure project root is on sys.path so config imports work
sys.path.insert(0, os.path.dirname(__file__))
from config import (
    EMAIL_ADDRESS,
    EMAIL_APP_PASSWORD,
    CATEGORY_LABELS,
    DEPARTMENT_EMAILS,
    BERT_MODEL_PATH,
    FLASK_HOST,
    FLASK_PORT,
)

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ── Load BERT Model ──────────────────────────────────────────────────
try:
    model = BertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
    tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_PATH)
    model.eval()
    logging.info("BERT model loaded successfully.")
except Exception as e:
    logging.warning(f"BERT model not found ({e}). Classification will use fallback.")
    model = None
    tokenizer = None

# ── Flask App ────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)

# SMTP config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ── Helper Functions ─────────────────────────────────────────────────

def classify_email(text: str) -> str:
    """Classify email text into a support category."""
    if model is None or tokenizer is None:
        return "General Inquiry"
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
        return CATEGORY_LABELS[predicted_class]
    except Exception as e:
        logging.error(f"Classification error: {e}")
        return "General Inquiry"


def send_email(recipient: str, subject: str, body: str, ticket_id: str = None) -> bool:
    """Send an email via Gmail SMTP."""
    if ticket_id:
        subject = f"{subject} [Ticket: {ticket_id}]"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        server.quit()
        logging.info(f"Email forwarded to {recipient}")
        return True
    except Exception as e:
        logging.error(f"Email forwarding failed: {e}")
        return False


# ── Routes ───────────────────────────────────────────────────────────

@app.route("/")
def home():
    return "MAILFLOW Flask API is running!", 200


@app.route("/dashboard")
def dashboard():
    """Serve the premium dashboard UI."""
    return render_template("dashboard.html")


@app.route("/predict", methods=["POST"])
def predict():
    """Classify an email and forward it to the correct department."""
    try:
        data = request.get_json()
        logging.info(f"Received data: {json.dumps(data)}")

        sender = data.get("sender", "")
        subject = data.get("subject", "")
        body = data.get("body", "")
        ticket_id = data.get("ticket_id", "")

        if not subject and not body:
            return jsonify({"error": "No content provided"}), 400

        category = data.get("category") or classify_email(f"{subject} {body}")

        recipient_email = DEPARTMENT_EMAILS.get(category)
        if not recipient_email:
            return jsonify({"error": "Invalid category"}), 500

        forward_subject = f"FWD: {subject} [Category: {category}]"
        forward_body = (
            f"---------- Forwarded message ----------\n"
            f"From: {sender}\n"
            f"Subject: {subject}\n"
            f"Ticket ID: {ticket_id}\n\n"
            f"{body}"
        )

        success = send_email(recipient_email, forward_subject, forward_body, ticket_id)

        if success:
            return jsonify({
                "category": category,
                "forwarded_to": recipient_email,
                "ticket_id": ticket_id,
                "status": "success",
            }), 200
        else:
            return jsonify({
                "category": category,
                "status": "failed",
                "error": "Failed to forward email",
            }), 500

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/tickets")
def api_tickets():
    """Return all tickets as JSON (consumed by dashboard)."""
    try:
        import mysql.connector
        from config import DB_CONFIG

        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, ticket_id, sender, category, subject, status, "
            "created_at, forwarded_to, response_sent "
            "FROM tickets ORDER BY created_at DESC"
        )
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        tickets = []
        for row in rows:
            ticket = dict(zip(columns, row))
            # Serialize datetime for JSON
            if isinstance(ticket.get("created_at"), datetime):
                ticket["created_at"] = ticket["created_at"].isoformat()
            tickets.append(ticket)
        cursor.close()
        db.close()
        return jsonify(tickets), 200
    except Exception as e:
        logging.error(f"Error fetching tickets: {e}")
        return jsonify([]), 200


@app.route("/api/stats")
def api_stats():
    """Return ticket statistics for the dashboard."""
    try:
        import mysql.connector
        from config import DB_CONFIG

        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        cursor.execute("SELECT COUNT(*) FROM tickets")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
        categories = dict(cursor.fetchall())

        cursor.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
        statuses = dict(cursor.fetchall())

        cursor.execute("SELECT COUNT(*) FROM tickets WHERE response_sent = TRUE")
        replied = cursor.fetchone()[0]

        cursor.close()
        db.close()

        return jsonify({
            "total": total,
            "categories": categories,
            "statuses": statuses,
            "replied": replied,
        }), 200
    except Exception as e:
        logging.error(f"Error fetching stats: {e}")
        return jsonify({"total": 0, "categories": {}, "statuses": {}, "replied": 0}), 200


# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logging.info(f"Starting MAILFLOW Flask API on {FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
