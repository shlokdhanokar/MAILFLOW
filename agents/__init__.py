"""
MAILFLOW Agents Package
Each agent is responsible for a single concern in the email-processing pipeline.
"""

from .base import Agent
from .email_fetcher import EmailFetcherAgent
from .classifier import ClassificationAgent
from .database import DatabaseAgent
from .forwarder import ForwardingAgent
from .replier import ReplyAgent

__all__ = [
    "Agent",
    "EmailFetcherAgent",
    "ClassificationAgent",
    "DatabaseAgent",
    "ForwardingAgent",
    "ReplyAgent",
]
