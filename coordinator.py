"""
MAILFLOW — Agent Coordinator
Orchestrates the full email-processing pipeline:
  Fetch → Classify → Store → Forward → Reply
"""

import csv
import os
import logging
from datetime import datetime

from agents import (
    EmailFetcherAgent,
    ClassificationAgent,
    DatabaseAgent,
    ForwardingAgent,
    ReplyAgent,
)


class AgentCoordinator:
    """Coordinates all agents to process emails end-to-end."""

    def __init__(self):
        self.logger = logging.getLogger("AgentCoordinator")
        self.logger.info("Initializing Agent Coordinator")

        # Instantiate agents
        self.email_agent = EmailFetcherAgent()
        self.classifier_agent = ClassificationAgent()
        self.database_agent = DatabaseAgent()
        self.forward_agent = ForwardingAgent()
        self.reply_agent = ReplyAgent()

        # Global processing log
        self.csv_file = "email_processing_logs.csv"
        if not os.path.isfile(self.csv_file):
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "email_id", "sender", "subject",
                    "category", "confidence", "ticket_id",
                    "forwarded", "replied", "status",
                ])

    # ── CSV Logging ──────────────────────────────────────────────────

    def _log_to_csv(self, data: dict):
        """Append a processing result row to the global CSV."""
        try:
            with open(self.csv_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    data.get("message_id", ""),
                    data.get("sender", ""),
                    data.get("subject", ""),
                    data.get("category", ""),
                    data.get("confidence", ""),
                    data.get("ticket_id", ""),
                    data.get("forwarded", False),
                    data.get("replied", False),
                    data.get("status", "unknown"),
                ])
        except Exception as e:
            self.logger.error(f"Failed to write to CSV: {e}")

    # ── Processing Pipeline ──────────────────────────────────────────

    def process_emails(self):
        """Run one cycle of the email-processing pipeline."""
        self.logger.info("Starting email processing cycle")

        # 1) Fetch
        emails = self.email_agent.process()
        if not emails:
            self.logger.info("No emails to process.")
            return

        self.logger.info(f"Processing {len(emails)} email(s)")

        # 2) Process each email
        for email_data in emails:
            try:
                self.logger.info(
                    f"Processing email from {email_data['sender']} — "
                    f"{email_data['subject']}"
                )

                # 3) Classify
                classification = self.classifier_agent.process(email_data)

                # 4) Store in database
                db_result = self.database_agent.process(email_data, classification)
                if "error" in db_result:
                    self.logger.error(f"Database error, skipping: {db_result['error']}")
                    continue

                ticket_id = db_result["ticket_id"]

                # 5) Forward to department
                forward_result = self.forward_agent.process(
                    email_data, classification, ticket_id
                )
                forwarded = "error" not in forward_result

                # 6) Reply to customer
                reply_result = self.reply_agent.process(
                    email_data, classification, ticket_id
                )
                replied = reply_result.get("success", False)

                # 7) Update reply status
                if replied:
                    self.database_agent.update_response_sent(db_result["db_id"], True)

                # Log results
                self._log_to_csv({
                    "message_id": email_data.get("message_id", ""),
                    "sender": email_data["sender"],
                    "subject": email_data["subject"],
                    "category": classification["category"],
                    "confidence": classification["confidence"],
                    "ticket_id": ticket_id,
                    "forwarded": forwarded,
                    "replied": replied,
                    "status": "success" if (forwarded and replied) else "partial",
                })

                self.logger.info(f"Successfully processed email: {ticket_id}")

            except Exception as e:
                self.logger.error(f"Error processing email: {e}")
                self._log_to_csv({
                    "message_id": email_data.get("message_id", ""),
                    "sender": email_data.get("sender", "unknown"),
                    "subject": email_data.get("subject", "unknown"),
                    "status": "error",
                })

    # ── Run Loop ─────────────────────────────────────────────────────

    def run(self, continuous: bool = False, interval: int = 300):
        """Run the pipeline once, or continuously on a timer."""
        import time

        try:
            if continuous:
                self.logger.info(
                    f"Continuous mode — checking every {interval}s"
                )
                while True:
                    self.process_emails()
                    self.logger.info(f"Sleeping for {interval}s")
                    time.sleep(interval)
            else:
                self.process_emails()
        except KeyboardInterrupt:
            self.logger.info("Gracefully shutting down")
        finally:
            self.cleanup()

    def cleanup(self):
        """Release all agent resources."""
        self.logger.info("Cleaning up resources")
        self.email_agent.disconnect()
        self.database_agent.disconnect()
