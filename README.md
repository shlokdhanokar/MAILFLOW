<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/BERT-Transformers-FF6F00?style=for-the-badge&logo=huggingface" />
  <img src="https://img.shields.io/badge/Gemini-1.5_Flash-4285F4?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/MySQL-8.0+-00758F?style=for-the-badge&logo=mysql&logoColor=white" />
</p>

# ✉️ MAILFLOW — AI-Powered Email Support Agent

**MAILFLOW** is an intelligent, multi-agent email support system that automatically reads incoming customer emails, classifies them using a fine-tuned BERT model, forwards them to the correct department, and generates personalised AI replies using Google Gemini — all while logging every action to a MySQL database and a premium real-time dashboard.

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────┐
│  Gmail Inbox │────▶│ EmailFetcherAgent│────▶│ClassifierAgent│
│   (IMAP)     │     │  (fetch unread)  │     │  (BERT model) │
└──────────────┘     └──────────────────┘     └───────┬───────┘
                                                      │
                     ┌──────────────────┐             │
                     │  ForwardingAgent │◀────────────┤
                     │  (Flask API →    │             │
                     │   dept. email)   │             ▼
                     └──────────────────┘     ┌───────────────┐
                                              │ DatabaseAgent │
                     ┌──────────────────┐     │ (MySQL tickets│
                     │   ReplyAgent     │◀────│  + logs)      │
                     │ (Gemini AI reply │     └───────────────┘
                     │  → SMTP send)    │
                     └──────────────────┘
                              │
                     ┌────────▼─────────┐
                     │  📊 Dashboard    │
                     │  (Flask + HTML)  │
                     └──────────────────┘
```

**AgentCoordinator** orchestrates all five agents in sequence:
`Fetch → Classify → Store → Forward → Reply`

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **BERT Classification** | Fine-tuned BERT model classifies emails into 4 categories |
| 💬 **AI-Powered Replies** | Google Gemini 1.5 Flash generates empathetic, context-aware replies |
| 📬 **Auto-Forwarding** | Emails routed to the correct department automatically |
| 🎫 **Ticket System** | Unique ticket IDs generated and tracked in MySQL |
| 📊 **Premium Dashboard** | Real-time glassmorphism UI with charts and ticket management |
| 🔄 **Continuous Mode** | Optional polling mode for unattended operation |
| 📝 **Full Logging** | Every agent action logged to CSV + database |

---

## 📁 Project Structure

```
MAILFLOW/
├── main.py                  # CLI entry point
├── coordinator.py           # Agent orchestration logic
├── config.py                # Centralized config (reads .env)
├── deploy_flask.py          # Flask API + Dashboard server
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore
├── agents/
│   ├── __init__.py
│   ├── base.py              # Abstract Agent base class
│   ├── email_fetcher.py     # Gmail IMAP fetcher
│   ├── classifier.py        # BERT classification agent
│   ├── database.py          # MySQL ticket storage
│   ├── forwarder.py         # Department email forwarding
│   └── replier.py           # Gemini reply generation
├── templates/
│   └── dashboard.html       # Premium dashboard UI
└── static/
    └── css/
        └── style.css        # Dashboard styles
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **MySQL 8.0+** with a database named `email_tickets`
- **Fine-tuned BERT model** saved in `email_bert_model/` directory
- **Gmail App Password** ([How to create one](https://support.google.com/accounts/answer/185833))
- **Google Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the Repository

```bash
git clone https://github.com/shlokdhanokar/MAILFLOW.git
cd MAILFLOW
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials:

```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_APP_PASSWORD=your-app-password
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-db-password
DB_NAME=email_tickets
GEMINI_API_KEY=your-gemini-api-key
```

### 5. Set Up MySQL Database

```sql
CREATE DATABASE IF NOT EXISTS email_tickets;
```

> The application will automatically create the required tables on first run.

### 6. Place Your BERT Model

Ensure your fine-tuned BERT model files are in the `email_bert_model/` directory:

```
email_bert_model/
├── config.json
├── model.safetensors
├── tokenizer.json
├── tokenizer_config.json
└── vocab.txt
```

---

## 📖 Usage

### Run Once (Single Cycle)

```bash
python main.py
```

### Run in Continuous Mode

```bash
python main.py --continuous --interval 60
```

### Launch Dashboard

```bash
python deploy_flask.py
```

Then open **http://127.0.0.1:5000/dashboard** in your browser.

---

## 📊 Dashboard

The premium dashboard provides:

- **📈 Stats Cards** — Total tickets, category breakdown, reply rate
- **📊 Charts** — Bar chart for traffic, doughnut for category distribution
- **🎫 Ticket Table** — Searchable, filterable ticket logs
- **✏️ Compose** — Send emails directly from the dashboard
- **⚙️ Settings** — View department mappings and AI model configuration

---

## 🛡️ Security Notes

- **Never commit your `.env` file** — it's excluded via `.gitignore`
- Use [Gmail App Passwords](https://support.google.com/accounts/answer/185833), not your main password
- Rotate credentials if they were previously exposed in version control

---

## 📄 License

This project is provided for educational purposes. Feel free to modify and extend.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/shlokdhanokar">shlokdhanokar</a>
</p>
