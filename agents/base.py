"""
MAILFLOW — Abstract Base Agent
Every agent in the system inherits from this class.
"""

import csv
import os
import logging
from abc import ABC, abstractmethod
from datetime import datetime


class Agent(ABC):
    """Abstract base class for all MAILFLOW agents."""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"Agent.{name}")
        self.logger.info(f"{name} Agent initialized")

    @abstractmethod
    def process(self, *args, **kwargs):
        """Process method to be implemented by all agents."""
        pass

    def log_action(self, action: str, status: str, details: dict = None) -> dict:
        """Log an action performed by the agent."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.name,
            "action": action,
            "status": status,
        }
        if details:
            log_entry["details"] = details

        self._log_to_csv(log_entry)
        return log_entry

    def _log_to_csv(self, log_entry: dict):
        """Persist a log entry to a per-agent CSV file."""
        csv_file = f"{self.name.lower()}_agent_logs.csv"
        file_exists = os.path.isfile(csv_file)

        log_entry_str = {k: str(v) for k, v in log_entry.items()}

        try:
            with open(csv_file, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=log_entry_str.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(log_entry_str)
        except Exception as e:
            self.logger.error(f"Failed to write to CSV: {e}")
