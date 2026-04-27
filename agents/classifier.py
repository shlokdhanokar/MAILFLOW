"""
MAILFLOW — Classification Agent
Supports two modes:
  - BERT: Local fine-tuned model (requires email_bert_model/ directory)
  - Gemini: Google Gemini API classification (lightweight, cloud-based)
Set CLASSIFIER_MODE in .env to switch between them.
"""

import json
from .base import Agent
from config import CATEGORY_LABELS, BERT_MODEL_PATH, CLASSIFIER_MODE, GEMINI_API_KEY


class ClassificationAgent(Agent):
    """Agent that classifies emails using either BERT or Gemini."""

    def __init__(self):
        super().__init__("Classifier")
        self.mode = CLASSIFIER_MODE.lower()
        self.logger.info(f"Classifier mode: {self.mode.upper()}")

        if self.mode == "bert":
            self._load_bert()
        elif self.mode == "gemini":
            self._load_gemini()
        else:
            raise ValueError(f"Unknown CLASSIFIER_MODE: {self.mode}. Use 'bert' or 'gemini'.")

    # ── BERT Setup ───────────────────────────────────────────────────

    def _load_bert(self):
        """Load the fine-tuned BERT model from disk."""
        import torch
        from transformers import BertTokenizer, BertForSequenceClassification

        try:
            self.tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_PATH)
            self.model = BertForSequenceClassification.from_pretrained(BERT_MODEL_PATH)
            self.model.eval()
            self.log_action("load_model", "success", {"mode": "bert"})
            self.logger.info("BERT model loaded successfully.")
        except Exception as e:
            self.log_action("load_model", "failed", {"error": str(e)})
            self.logger.error(f"Error loading BERT model: {e}")
            raise RuntimeError(f"Failed to load BERT model: {e}")

    def _classify_bert(self, text: str) -> dict:
        """Classify using the local BERT model."""
        import torch

        inputs = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=512,
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()

        category = CATEGORY_LABELS[predicted_class]
        confidence = torch.softmax(outputs.logits, dim=1)[0][predicted_class].item()

        return {"category": category, "confidence": confidence, "predicted_class_id": predicted_class}

    # ── Gemini Setup ─────────────────────────────────────────────────

    def _load_gemini(self):
        """Initialize the Gemini model for classification."""
        from google.generativeai import configure, GenerativeModel

        configure(api_key=GEMINI_API_KEY)
        self.gemini_model = GenerativeModel("gemini-1.5-flash")
        self.log_action("load_model", "success", {"mode": "gemini"})
        self.logger.info("Gemini classifier initialized.")

    def _classify_gemini(self, text: str) -> dict:
        """Classify using Google Gemini API."""
        prompt = (
            "You are an email classifier for a customer support system. "
            "Classify the following email into EXACTLY ONE of these categories:\n"
            "- Technical Issue\n- Billing Issue\n- Account Issue\n- General Inquiry\n\n"
            f"Email content:\n\"{text}\"\n\n"
            "Respond with ONLY a JSON object in this exact format (no markdown, no extra text):\n"
            '{"category": "<category name>", "confidence": <0.0 to 1.0>}'
        )

        response = self.gemini_model.generate_content(prompt)
        raw = response.text.strip()

        # Clean markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        result = json.loads(raw)
        category = result.get("category", "General Inquiry")
        confidence = float(result.get("confidence", 0.8))

        # Validate category
        if category not in CATEGORY_LABELS:
            category = "General Inquiry"

        return {"category": category, "confidence": confidence, "predicted_class_id": CATEGORY_LABELS.index(category)}

    # ── Public Interface ─────────────────────────────────────────────

    def process(self, email_data: dict) -> dict:
        """Classify the email using the configured mode."""
        try:
            text = f"{email_data['subject']} {email_data['body']}"

            if self.mode == "bert":
                result = self._classify_bert(text)
            else:
                result = self._classify_gemini(text)

            self.log_action("classify", "success", {
                "message_id": email_data.get("message_id"),
                "mode": self.mode,
                "category": result["category"],
                "confidence": f"{result['confidence']:.4f}",
            })
            return result

        except Exception as e:
            self.log_action("classify", "failed", {
                "message_id": email_data.get("message_id"),
                "error": str(e),
            })
            self.logger.error(f"Error classifying email: {e}")
            return {"category": "General Inquiry", "confidence": 0.0, "error": str(e)}
