"""
MAILFLOW — Reply Agent
Generates personalised responses using Google Gemini and sends them via SMTP.
"""

import re
import smtplib
from email.mime.text import MIMEText

from google.generativeai import configure, GenerativeModel

from .base import Agent
from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD, GEMINI_API_KEY

# Configure Gemini once at module load
configure(api_key=GEMINI_API_KEY)


class ReplyAgent(Agent):
    """Agent responsible for generating and sending AI-powered replies."""

    def __init__(self):
        super().__init__("Replier")
        self.gemini_model = GenerativeModel("gemini-1.5-flash")

    # ── Reply Generation ─────────────────────────────────────────────

    def generate_reply(self, email_data: dict, classification_data: dict, ticket_id: str) -> str:
        """Generate a professional reply using Gemini."""
        try:
            prompt = (
                "As a professional customer support assistant, write a personalized "
                "reply to this customer email.\n\n"
                f"Category: {classification_data['category']}\n"
                f"Ticket ID: {ticket_id}\n"
                f"Subject: \"{email_data['subject']}\"\n\n"
                f"Customer's message:\n{email_data['body']}\n\n"
                "Your reply should:\n"
                f"1. Acknowledge their specific issue\n"
                f"2. Confirm that a support ticket ({ticket_id}) has been created\n"
                f"3. Explain that their request has been forwarded to the "
                f"{classification_data['category']} team\n"
                "4. Set expectations about when they'll hear back (1-2 business days)\n"
                "5. Thank them for their patience\n"
                "6. Sign off professionally as the Customer Support Team\n\n"
                "Keep your response concise, empathetic, and professional."
            )

            response = self.gemini_model.generate_content(prompt)
            reply_text = response.text.strip()

            self.log_action("generate_reply", "success", {
                "message_id": email_data.get("message_id"),
                "ticket_id": ticket_id,
            })
            return reply_text

        except Exception as e:
            self.log_action("generate_reply", "failed", {
                "message_id": email_data.get("message_id"),
                "error": str(e),
            })
            self.logger.error(f"Error generating reply: {e}")

            # Fallback template
            return (
                f"Thank you for contacting our support team.\n\n"
                f"We've received your message and created ticket #{ticket_id} "
                f"for your {classification_data['category']}.\n\n"
                f"A member of our team will review your request and get back "
                f"to you within 1-2 business days.\n\n"
                f"Best regards,\nCustomer Support Team"
            )

    # ── Email Sending ────────────────────────────────────────────────

    def send_reply(self, email_data: dict, reply_text: str, ticket_id: str) -> bool:
        """Send the generated reply to the customer via SMTP."""
        try:
            sender = email_data["sender"]
            match = re.search(r"<(.+?)>", sender)
            recipient_email = match.group(1) if match else sender

            msg = MIMEText(reply_text)
            msg["Subject"] = f"Re: {email_data['subject']} [Ticket: {ticket_id}]"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = recipient_email
            msg["In-Reply-To"] = email_data.get("message_id", "")
            msg["References"] = email_data.get("message_id", "")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())

            self.log_action("send_reply", "success", {
                "message_id": email_data.get("message_id"),
                "recipient": recipient_email,
                "ticket_id": ticket_id,
            })
            self.logger.info(f"Replied to {recipient_email} — ticket #{ticket_id}")
            return True

        except Exception as e:
            self.log_action("send_reply", "failed", {
                "message_id": email_data.get("message_id"),
                "error": str(e),
            })
            self.logger.error(f"Failed to send reply: {e}")
            return False

    # ── Process (orchestrator interface) ─────────────────────────────

    def process(self, email_data: dict, classification_data: dict, ticket_id: str) -> dict:
        """Generate and send a reply — returns success flag and reply text."""
        reply_text = self.generate_reply(email_data, classification_data, ticket_id)
        success = self.send_reply(email_data, reply_text, ticket_id)
        return {"success": success, "reply_text": reply_text}
