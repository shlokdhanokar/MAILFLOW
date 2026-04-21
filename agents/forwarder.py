"""
MAILFLOW — Forwarding Agent
Forwards classified emails to the appropriate department via the Flask API.
"""

import os
import sys
import json
import time
import subprocess

import requests

from .base import Agent
from config import FLASK_API_URL, FLASK_HOST, FLASK_PORT


class ForwardingAgent(Agent):
    """Agent responsible for forwarding emails to department mailboxes."""

    def __init__(self):
        super().__init__("Forwarder")
        self._ensure_flask_api_running()

    def _ensure_flask_api_running(self) -> bool:
        """Check if Flask API is reachable; start it if not."""
        try:
            response = requests.get(f"http://{FLASK_HOST}:{FLASK_PORT}/", timeout=2)
            if response.status_code == 200:
                self.logger.info("Flask API is already running.")
                return True
        except requests.exceptions.RequestException:
            self.logger.info("Starting Flask API…")
            return self._start_flask_api()

    def _start_flask_api(self) -> bool:
        """Launch deploy_flask.py as a background process."""
        try:
            script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "deploy_flask.py")

            if sys.platform == "win32":
                subprocess.Popen(
                    ["python", script],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )
            else:
                subprocess.Popen(
                    ["python", script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            # Wait for Flask to become responsive
            for _ in range(10):
                time.sleep(1)
                try:
                    r = requests.get(f"http://{FLASK_HOST}:{FLASK_PORT}/", timeout=1)
                    if r.status_code == 200:
                        self.logger.info("Flask API started successfully.")
                        self.log_action("start_flask_api", "success")
                        return True
                except requests.exceptions.RequestException:
                    continue

            self.logger.error("Flask API did not start within 10 seconds.")
            self.log_action("start_flask_api", "failed", {"error": "Timeout"})
            return False

        except Exception as e:
            self.logger.error(f"Error starting Flask API: {e}")
            self.log_action("start_flask_api", "failed", {"error": str(e)})
            return False

    def process(self, email_data: dict, classification_data: dict, ticket_id: str) -> dict:
        """Forward the email to the correct department via the Flask API."""
        try:
            payload = {
                "sender": email_data["sender"],
                "subject": email_data["subject"],
                "body": email_data["body"],
                "text": f"{email_data['subject']} {email_data['body']}",
                "category": classification_data["category"],
                "ticket_id": ticket_id,
            }

            self.logger.info(f"Sending payload to Flask API: {json.dumps(payload)}")
            response = requests.post(FLASK_API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()
                self.log_action("forward", "success", {
                    "message_id": email_data.get("message_id"),
                    "category": classification_data["category"],
                    "forwarded_to": result.get("forwarded_to", "unknown"),
                })
                return result

            self.log_action("forward", "failed", {
                "message_id": email_data.get("message_id"),
                "status_code": response.status_code,
                "response": response.text,
            })
            self.logger.error(
                f"Forward failed — status {response.status_code}: {response.text}"
            )
            return {"error": response.text}

        except Exception as e:
            self.log_action("forward", "failed", {
                "message_id": email_data.get("message_id"),
                "error": str(e),
            })
            self.logger.error(f"Error calling Flask API: {e}")
            return {"error": str(e)}
