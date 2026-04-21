"""
MAILFLOW — Email Fetcher Agent
Connects to Gmail via IMAP and fetches unread emails.
"""

import imaplib
import email
from email.header import decode_header

from .base import Agent
from config import EMAIL_ADDRESS, EMAIL_APP_PASSWORD


class EmailFetcherAgent(Agent):
    """Agent responsible for fetching emails from Gmail."""

    def __init__(self):
        super().__init__("EmailFetcher")
        self.imap = None

    def connect(self) -> bool:
        """Connect to Gmail IMAP server."""
        try:
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.imap.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            self.imap.select("inbox")
            self.log_action("connect", "success")
            self.logger.info("Connected to Gmail.")
            return True
        except Exception as e:
            self.log_action("connect", "failed", {"error": str(e)})
            self.logger.error(f"Failed to connect to Gmail: {e}")
            return False

    def process(self) -> list:
        """Fetch unread emails from Gmail."""
        if not self.imap and not self.connect():
            return []

        try:
            status, messages = self.imap.search(None, "UNSEEN")
            email_ids = messages[0].split()

            if not email_ids:
                self.logger.info("No new emails found.")
                self.log_action("fetch", "success", {"count": 0})
                return []

            self.logger.info(f"{len(email_ids)} unread email(s) found.")
            self.log_action("fetch", "success", {"count": len(email_ids)})

            emails = []
            for mail_id in email_ids:
                try:
                    email_data = self._parse_email(mail_id)
                    if email_data:
                        emails.append(email_data)
                    self.log_action("process_email", "success", {"mail_id": mail_id.decode()})
                except Exception as e:
                    self.log_action("process_email", "failed", {
                        "mail_id": mail_id.decode(), "error": str(e)
                    })
                    self.logger.error(f"Error processing email ID {mail_id}: {e}")

            return emails

        except Exception as e:
            self.log_action("fetch", "failed", {"error": str(e)})
            self.logger.error(f"Error fetching emails: {e}")
            return []

    def _parse_email(self, mail_id) -> dict | None:
        """Parse a single email by its IMAP ID."""
        status, msg_data = self.imap.fetch(mail_id, "(RFC822)")

        for response_part in msg_data:
            if not isinstance(response_part, tuple):
                continue

            msg = email.message_from_bytes(response_part[1])

            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            # Extract body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            return {
                "mail_id": mail_id.decode(),
                "message_id": msg.get("Message-ID", f"generated-{mail_id.decode()}"),
                "sender": msg.get("From"),
                "subject": subject,
                "body": body,
                "date": msg.get("Date"),
            }

        return None

    def disconnect(self):
        """Close IMAP connection."""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
                self.log_action("disconnect", "success")
                self.logger.info("Disconnected from Gmail.")
            except Exception as e:
                self.log_action("disconnect", "failed", {"error": str(e)})
                self.logger.error(f"Error disconnecting from Gmail: {e}")
