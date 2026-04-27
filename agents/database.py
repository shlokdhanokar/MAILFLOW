"""
MAILFLOW — Database Agent
Supports two backends:
  - MySQL: Full database server (local/production)
  - SQLite: File-based, zero-config (hosted/lightweight)
Set DB_MODE in .env to switch between them.
"""

import os
import sqlite3
from datetime import datetime

from .base import Agent
from config import DB_MODE, DB_CONFIG, SQLITE_PATH, DEPARTMENT_EMAILS


class DatabaseAgent(Agent):
    """Agent responsible for all database operations (MySQL or SQLite)."""

    def __init__(self):
        super().__init__("Database")
        self.mode = DB_MODE.lower()
        self.db = None
        self.cursor = None
        self.logger.info(f"Database mode: {self.mode.upper()}")

        if self.connect():
            self.drop_and_recreate_tables()

    # ── Connection ───────────────────────────────────────────────────

    def connect(self) -> bool:
        """Connect to the configured database."""
        try:
            if self.mode == "mysql":
                import mysql.connector
                self.db = mysql.connector.connect(**DB_CONFIG)
                self.cursor = self.db.cursor()
            else:
                self.db = sqlite3.connect(SQLITE_PATH, check_same_thread=False)
                self.cursor = self.db.cursor()

            self.log_action("connect", "success", {"mode": self.mode})
            self.logger.info(f"Connected to {self.mode.upper()} database.")
            return True
        except Exception as e:
            self.log_action("connect", "failed", {"error": str(e)})
            self.logger.error(f"Database connection failed: {e}")
            return False

    def disconnect(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        self.log_action("disconnect", "success")
        self.logger.info("Disconnected from database.")

    # ── Table Management ─────────────────────────────────────────────

    def drop_and_recreate_tables(self) -> bool:
        """Drop existing tables and recreate them."""
        try:
            self.cursor.execute("DROP TABLE IF EXISTS tickets")
            self.cursor.execute("DROP TABLE IF EXISTS agent_logs")
            self.db.commit()
            self.log_action("drop_tables", "success")
            self._create_tables()
            return True
        except Exception as e:
            self.log_action("drop_tables", "failed", {"error": str(e)})
            self.logger.error(f"Failed to drop tables: {e}")
            return False

    def _create_tables(self):
        """Create tables with syntax compatible with both MySQL and SQLite."""
        try:
            if self.mode == "mysql":
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tickets (
                        id            INT AUTO_INCREMENT PRIMARY KEY,
                        ticket_id     VARCHAR(20)  NOT NULL,
                        sender        VARCHAR(255) NOT NULL,
                        category      VARCHAR(50)  NOT NULL,
                        subject       TEXT         NOT NULL,
                        body          TEXT         NOT NULL,
                        status        VARCHAR(20)  DEFAULT 'new',
                        created_at    TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
                        forwarded_to  VARCHAR(255),
                        response_sent BOOLEAN      DEFAULT FALSE
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agent_logs (
                        id        INT AUTO_INCREMENT PRIMARY KEY,
                        agent     VARCHAR(50)  NOT NULL,
                        action    VARCHAR(50)  NOT NULL,
                        status    VARCHAR(20)  NOT NULL,
                        details   JSON,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            else:
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tickets (
                        id            INTEGER PRIMARY KEY AUTOINCREMENT,
                        ticket_id     TEXT NOT NULL,
                        sender        TEXT NOT NULL,
                        category      TEXT NOT NULL,
                        subject       TEXT NOT NULL,
                        body          TEXT NOT NULL,
                        status        TEXT DEFAULT 'new',
                        created_at    TEXT DEFAULT (datetime('now')),
                        forwarded_to  TEXT,
                        response_sent INTEGER DEFAULT 0
                    )
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agent_logs (
                        id        INTEGER PRIMARY KEY AUTOINCREMENT,
                        agent     TEXT NOT NULL,
                        action    TEXT NOT NULL,
                        status    TEXT NOT NULL,
                        details   TEXT,
                        timestamp TEXT DEFAULT (datetime('now'))
                    )
                """)

            self.db.commit()
            self.log_action("create_tables", "success")
        except Exception as e:
            self.log_action("create_tables", "failed", {"error": str(e)})
            self.logger.error(f"Failed to create tables: {e}")

    # ── Ticket Operations ────────────────────────────────────────────

    def process(self, email_data: dict, classification_data: dict) -> dict:
        """Store an email and its classification as a new ticket."""
        try:
            ticket_id = f"TICK-{datetime.now().strftime('%Y%m%d')}-{os.urandom(2).hex().upper()}"
            forwarded_to = DEPARTMENT_EMAILS.get(classification_data["category"], "")

            self.cursor.execute(
                "INSERT INTO tickets (ticket_id, sender, category, subject, body, forwarded_to) VALUES (?, ?, ?, ?, ?, ?)"
                if self.mode == "sqlite" else
                "INSERT INTO tickets (ticket_id, sender, category, subject, body, forwarded_to) VALUES (%s, %s, %s, %s, %s, %s)",
                (ticket_id, email_data["sender"], classification_data["category"],
                 email_data["subject"], email_data["body"], forwarded_to),
            )
            self.db.commit()
            db_id = self.cursor.lastrowid

            self.log_action("store", "success", {
                "ticket_id": ticket_id,
                "category": classification_data["category"],
            })
            return {"db_id": db_id, "ticket_id": ticket_id}

        except Exception as e:
            self.log_action("store", "failed", {"error": str(e)})
            self.logger.error(f"Error storing in database: {e}")
            return {"error": str(e)}

    def update_response_sent(self, db_id: int, sent: bool = True) -> bool:
        """Mark a ticket's reply as sent."""
        try:
            placeholder = "?" if self.mode == "sqlite" else "%s"
            self.cursor.execute(
                f"UPDATE tickets SET response_sent = {placeholder} WHERE id = {placeholder}",
                (1 if (self.mode == "sqlite" and sent) else sent, db_id),
            )
            self.db.commit()
            self.log_action("update_response_status", "success", {"db_id": db_id})
            return True
        except Exception as e:
            self.log_action("update_response_status", "failed", {"db_id": db_id, "error": str(e)})
            self.logger.error(f"Error updating response status: {e}")
            return False

    def get_all_tickets(self) -> list:
        """Retrieve all tickets."""
        try:
            self.cursor.execute(
                "SELECT id, ticket_id, sender, category, subject, status, "
                "created_at, forwarded_to, response_sent FROM tickets "
                "ORDER BY created_at DESC"
            )
            columns = [desc[0] for desc in self.cursor.description]
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"Error fetching tickets: {e}")
            return []

    def get_ticket_stats(self) -> dict:
        """Return aggregate statistics for the dashboard."""
        stats = {"total": 0, "categories": {}, "statuses": {}, "replied": 0}
        try:
            self.cursor.execute("SELECT COUNT(*) FROM tickets")
            stats["total"] = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT category, COUNT(*) FROM tickets GROUP BY category")
            stats["categories"] = dict(self.cursor.fetchall())

            self.cursor.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
            stats["statuses"] = dict(self.cursor.fetchall())

            self.cursor.execute("SELECT COUNT(*) FROM tickets WHERE response_sent = 1")
            stats["replied"] = self.cursor.fetchone()[0]
        except Exception as e:
            self.logger.error(f"Error fetching stats: {e}")
        return stats
