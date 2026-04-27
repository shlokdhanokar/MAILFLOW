"""
MAILFLOW — BERT Email Classifier Training Script
Fine-tunes bert-base-uncased on sample email data for 4 support categories.
Saves the trained model to email_bert_model/
"""

import os
import torch
import random
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import BertTokenizer, BertForSequenceClassification, get_linear_schedule_with_warmup

# ── Configuration ────────────────────────────────────────────────────
MODEL_NAME = "bert-base-uncased"
OUTPUT_DIR = "email_bert_model"
NUM_LABELS = 4
EPOCHS = 6
BATCH_SIZE = 8
LEARNING_RATE = 2e-5
MAX_LENGTH = 128
SEED = 42

CATEGORY_LABELS = ["Technical Issue", "Billing Issue", "Account Issue", "General Inquiry"]

# ── Sample Training Data ─────────────────────────────────────────────
# Each entry: (text, label_index)
# 0 = Technical Issue, 1 = Billing Issue, 2 = Account Issue, 3 = General Inquiry

TRAINING_DATA = [
    # ── Technical Issue (0) ──────────────────────────────────
    ("My app keeps crashing whenever I try to upload a file larger than 5MB", 0),
    ("The website is showing a 500 internal server error on the checkout page", 0),
    ("I can't connect to the API endpoint, getting timeout errors consistently", 0),
    ("The software is extremely slow and takes minutes to load any page", 0),
    ("There's a bug in the search feature, it returns wrong results", 0),
    ("The mobile app freezes when I open the notifications tab", 0),
    ("Error message says database connection failed when I try to save", 0),
    ("The export to PDF feature is broken and generates blank documents", 0),
    ("Getting a 404 error when trying to access my project dashboard", 0),
    ("The integration with Slack stopped working after the last update", 0),
    ("My code deployment keeps failing with a build error", 0),
    ("The real-time sync feature is not updating data across devices", 0),
    ("Video calls drop after exactly 10 minutes every time", 0),
    ("The drag and drop feature doesn't work on Firefox browser", 0),
    ("Push notifications are not being delivered to my Android device", 0),
    ("The dark mode toggle breaks the layout of the settings page", 0),
    ("File uploads get stuck at 99% and never complete", 0),
    ("The calendar widget shows wrong dates and time zones", 0),
    ("Getting CORS errors when making API requests from my frontend", 0),
    ("The auto-save feature is not working and I lost my progress", 0),
    ("Server response time is very high, pages take 30 seconds to load", 0),
    ("The webhook endpoint is returning 403 forbidden errors", 0),
    ("Images are not rendering properly on the product page", 0),
    ("The search bar autocomplete suggestions are completely irrelevant", 0),
    ("SSL certificate error when accessing the admin panel", 0),

    # ── Billing Issue (1) ────────────────────────────────────
    ("I was charged twice for my monthly subscription this month", 1),
    ("Please process a refund for my last payment, the service didn't work", 1),
    ("My credit card was declined but the subscription shows as active", 1),
    ("I want to downgrade my plan from premium to basic", 1),
    ("The invoice I received has incorrect billing information", 1),
    ("I cancelled my subscription but was still charged", 1),
    ("Can you explain the extra charges on my latest bill?", 1),
    ("I need a receipt for my annual subscription payment for tax purposes", 1),
    ("The pricing on your website doesn't match what I was charged", 1),
    ("I'd like to upgrade my plan and want to know the prorated cost", 1),
    ("My free trial ended but I was charged without any notification", 1),
    ("I need to update my payment method to a different credit card", 1),
    ("The discount code I applied didn't reduce the total amount", 1),
    ("I was charged in USD but I should be billed in EUR", 1),
    ("Can I get a refund for the unused portion of my annual plan?", 1),
    ("My payment failed but the money was deducted from my account", 1),
    ("I need an itemized breakdown of all charges for this quarter", 1),
    ("The auto-renewal charged me even though I turned it off", 1),
    ("I want to switch from monthly to annual billing to save money", 1),
    ("There's a pending charge on my card that hasn't been processed", 1),
    ("I need to dispute a charge that I don't recognize on my statement", 1),
    ("Can you send me invoices for the last 6 months of payments?", 1),
    ("The student discount wasn't applied to my subscription", 1),
    ("I want to cancel my subscription and get a full refund", 1),
    ("My company needs to update the billing address on our account", 1),

    # ── Account Issue (2) ────────────────────────────────────
    ("I forgot my password and the reset email isn't arriving", 2),
    ("Someone hacked into my account and changed my email address", 2),
    ("I can't log in even though I'm using the correct credentials", 2),
    ("My account was locked after too many failed login attempts", 2),
    ("I want to change my username but can't find the option", 2),
    ("Two-factor authentication code is not being sent to my phone", 2),
    ("I need to merge two accounts that I accidentally created", 2),
    ("My account shows as suspended but I didn't violate any terms", 2),
    ("I want to delete my account and all associated data permanently", 2),
    ("The email verification link has expired, please send a new one", 2),
    ("I can't update my profile picture, it keeps reverting to the old one", 2),
    ("My account permissions were changed without my authorization", 2),
    ("I need to transfer ownership of my account to another person", 2),
    ("Single sign-on with Google is not working for my account", 2),
    ("My account settings keep resetting to defaults every time I log in", 2),
    ("I registered with the wrong email and need to change it", 2),
    ("My session keeps expiring every few minutes forcing me to re-login", 2),
    ("I can't access my account on the mobile app but web works fine", 2),
    ("The security questions I set up are not being accepted anymore", 2),
    ("I need to add another admin user to my organization account", 2),
    ("My profile information is not visible to other team members", 2),
    ("I want to enable two-factor authentication but the option is greyed out", 2),
    ("Password reset keeps saying my email is not registered", 2),
    ("I need to recover my account after losing access to my phone", 2),
    ("My login history shows suspicious access from unknown locations", 2),

    # ── General Inquiry (3) ───────────────────────────────────
    ("What are your business hours for customer support?", 3),
    ("Do you have any job openings in the engineering department?", 3),
    ("I'd like to learn more about your enterprise solutions", 3),
    ("Can you send me a product brochure or feature comparison?", 3),
    ("What programming languages does your platform support?", 3),
    ("I'm interested in becoming a partner or reseller", 3),
    ("Do you offer any educational discounts for students?", 3),
    ("What's the difference between your basic and premium plans?", 3),
    ("Can I schedule a demo with your sales team?", 3),
    ("How does your product compare to competitors?", 3),
    ("Is there a public roadmap for upcoming features?",3),
    ("Do you have an affiliate or referral program?", 3),
    ("What security certifications does your platform have?", 3),
    ("Can I use your service for a nonprofit organization?", 3),
    ("How many users can I add to a team account?", 3),
    ("Do you provide on-site training for enterprise customers?", 3),
    ("What are the system requirements for your desktop application?", 3),
    ("I want to give feedback on a feature I'd like to see added", 3),
    ("Does your API support webhooks for real-time notifications?", 3),
    ("Can I export my data if I decide to leave your platform?", 3),
    ("What is your uptime SLA for enterprise accounts?", 3),
    ("I have a question about your terms of service", 3),
    ("Do you support integration with Salesforce and HubSpot?", 3),
    ("How long does the onboarding process typically take?", 3),
    ("I'd like to submit a feature request for the mobile app", 3),
]


# ── Dataset Class ─────────────────────────────────────────────────────
class EmailDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.encodings = tokenizer(
            texts, truncation=True, padding=True,
            max_length=max_length, return_tensors="pt"
        )
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item


# ── Training Function ─────────────────────────────────────────────────
def train():
    # Seed for reproducibility
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n{'='*55}")
    print(f"  MAILFLOW — BERT Email Classifier Training")
    print(f"{'='*55}")
    print(f"  Device:       {device}")
    print(f"  Base model:   {MODEL_NAME}")
    print(f"  Categories:   {NUM_LABELS} ({', '.join(CATEGORY_LABELS)})")
    print(f"  Train samples: {len(TRAINING_DATA)}")
    print(f"  Epochs:       {EPOCHS}")
    print(f"  Batch size:   {BATCH_SIZE}")
    print(f"{'='*55}\n")

    # Load tokenizer and model
    print("[1/4] Loading tokenizer and base model...")
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=NUM_LABELS
    )
    model.to(device)

    # Prepare data
    print("[2/4] Preparing dataset...")
    texts = [t[0] for t in TRAINING_DATA]
    labels = [t[1] for t in TRAINING_DATA]

    dataset = EmailDataset(texts, labels, tokenizer, MAX_LENGTH)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=0.01)
    total_steps = len(dataloader) * EPOCHS
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=int(0.1 * total_steps),
        num_training_steps=total_steps
    )

    # Training loop
    print("[3/4] Training...\n")
    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0
        correct = 0
        total = 0

        for batch in dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}

            outputs = model(**batch)
            loss = outputs.loss

            total_loss += loss.item()
            preds = torch.argmax(outputs.logits, dim=1)
            correct += (preds == batch["labels"]).sum().item()
            total += len(batch["labels"])

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        avg_loss = total_loss / len(dataloader)
        accuracy = correct / total * 100
        print(f"  Epoch {epoch+1}/{EPOCHS}  |  Loss: {avg_loss:.4f}  |  Accuracy: {accuracy:.1f}%")

    # Save model
    print(f"\n[4/4] Saving model to {OUTPUT_DIR}/...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    # Quick validation
    print("\n  Validating saved model...")
    test_model = BertForSequenceClassification.from_pretrained(OUTPUT_DIR)
    test_tokenizer = BertTokenizer.from_pretrained(OUTPUT_DIR)
    test_model.eval()

    test_texts = [
        "My app crashes when uploading files",
        "I was charged twice this month",
        "I can't log into my account",
        "What plans do you offer?",
    ]

    print("\n  Sample predictions:")
    for text in test_texts:
        inputs = test_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=MAX_LENGTH)
        with torch.no_grad():
            outputs = test_model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            conf = torch.softmax(outputs.logits, dim=1)[0][pred].item()
        print(f"    \"{text}\"")
        print(f"    → {CATEGORY_LABELS[pred]} ({conf:.1%} confidence)\n")

    print(f"{'='*55}")
    print(f"  ✅ Model saved to {OUTPUT_DIR}/")
    print(f"  You can now run: python main.py")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    train()
