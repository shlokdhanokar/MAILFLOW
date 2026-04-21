"""
MAILFLOW — Classification Agent
Uses a fine-tuned BERT model to categorize incoming emails.
"""

import torch
from transformers import BertTokenizer, BertForSequenceClassification

from .base import Agent
from config import CATEGORY_LABELS, BERT_MODEL_PATH


class ClassificationAgent(Agent):
    """Agent responsible for classifying emails into support categories."""

    def __init__(self):
        super().__init__("Classifier")
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        """Load the BERT classification model from disk."""
        try:
            self.tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_PATH)
            self.model = BertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
            self.model.eval()
            self.log_action("load_model", "success")
            self.logger.info("BERT model loaded successfully.")
        except Exception as e:
            self.log_action("load_model", "failed", {"error": str(e)})
            self.logger.error(f"Error loading BERT model: {e}")
            raise RuntimeError(f"Failed to load BERT model: {e}")

    def process(self, email_data: dict) -> dict:
        """Classify the email content into a support category."""
        try:
            text = f"{email_data['subject']} {email_data['body']}"

            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )

            with torch.no_grad():
                outputs = self.model(**inputs)
                predicted_class = torch.argmax(outputs.logits, dim=1).item()

            category = CATEGORY_LABELS[predicted_class]
            confidence = torch.softmax(outputs.logits, dim=1)[0][predicted_class].item()

            result = {
                "category": category,
                "confidence": confidence,
                "predicted_class_id": predicted_class,
            }

            self.log_action("classify", "success", {
                "message_id": email_data.get("message_id"),
                "category": category,
                "confidence": f"{confidence:.4f}",
            })

            return result

        except Exception as e:
            self.log_action("classify", "failed", {
                "message_id": email_data.get("message_id"),
                "error": str(e),
            })
            self.logger.error(f"Error classifying email: {e}")
            return {"category": "General Inquiry", "confidence": 0.0, "error": str(e)}
