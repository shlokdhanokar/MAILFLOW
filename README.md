<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/BERT-Transformers-FF6F00?style=for-the-badge&logo=huggingface" />
  <img src="https://img.shields.io/badge/Gemini-1.5_Flash-4285F4?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask" />
</p>

# MAILFLOW — AI-Powered Email Support Agent

**MAILFLOW** is an intelligent, multi-agent email support system that automatically reads incoming customer emails, classifies them, forwards them to the correct department, and generates personalised AI replies — all orchestrated by a coordinator and visualized on a premium React dashboard.

---

## Architecture

```
                          +-------------------+
                          | AgentCoordinator  |
                          +--------+----------+
                                   |
         +------------+------------+------------+------------+
         |            |            |            |            |
   +-----v----+ +-----v-----+ +---v----+ +----v-----+ +----v----+
   |  Email   | | Classifier| |Database| |Forwarder | | Replier |
   |  Fetcher | | BERT /    | | MySQL /| | Flask    | | Gemini  |
   |  (IMAP)  | | Gemini    | | SQLite | | API      | | AI      |
   +----------+ +-----------+ +--------+ +----------+ +---------+
```

**Pipeline:** `Fetch → Classify → Store → Forward → Reply`

---

## Two Running Modes

MAILFLOW supports two configurations to fit different deployment needs:

### Mode A: Local (Full Power)

Best for development, demos, and maximum accuracy.

| Component | Technology |
|-----------|------------|
| **Classifier** | Fine-tuned BERT model (local, 438MB) |
| **Database** | MySQL server |
| **Requirements** | Python, MySQL, BERT model files, GPU optional |

```env
CLASSIFIER_MODE=bert
DB_MODE=mysql
```

### Mode B: Hosted (Lightweight)

Best for cloud deployment (Render, Railway, etc.) — **no large model files needed**.

| Component | Technology |
|-----------|------------|
| **Classifier** | Google Gemini API (cloud-based) |
| **Database** | SQLite (file-based, zero config) |
| **Requirements** | Python + Gemini API key only |

```env
CLASSIFIER_MODE=gemini
DB_MODE=sqlite
```

> **Note:** Both modes use the same 5-agent architecture. Only the internals of the Classifier and Database agents change.

---

## Features

| Feature | Description |
|---------|-------------|
| **Dual Classifier** | Switch between local BERT and cloud Gemini with one env var |
| **AI-Powered Replies** | Google Gemini generates empathetic, context-aware customer replies |
| **Auto-Forwarding** | Emails routed to the correct department automatically |
| **Ticket System** | Unique ticket IDs tracked in MySQL or SQLite |
| **React Dashboard** | Premium dark-theme UI with Recharts, Framer Motion animations |
| **Continuous Mode** | Optional polling for unattended background operation |
| **Full Logging** | Every agent action logged to CSV + database |

---

## Project Structure

```
MAILFLOW/
├── main.py                  # CLI entry point
├── coordinator.py           # Agent orchestration
├── config.py                # Centralized config (reads .env)
├── deploy_flask.py          # Flask API + dashboard server
├── train_model.py           # BERT training script (Mode A only)
├── requirements.txt
├── .env.example
├── agents/
│   ├── base.py              # Abstract Agent base class
│   ├── email_fetcher.py     # Gmail IMAP fetcher
│   ├── classifier.py        # Dual-mode: BERT or Gemini
│   ├── database.py          # Dual-mode: MySQL or SQLite
│   ├── forwarder.py         # Department email forwarding
│   └── replier.py           # Gemini reply generation
├── frontend/                # React + Vite dashboard
│   ├── src/
│   │   ├── components/      # Sidebar, StatCard
│   │   ├── pages/           # Dashboard, Tickets, Compose, Settings
│   │   └── styles/          # Global CSS
│   └── package.json
├── templates/
│   └── dashboard.html       # Fallback HTML dashboard
└── static/css/
    └── style.css
```

---

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** (for React dashboard)
- **Gmail App Password** ([How to create one](https://support.google.com/accounts/answer/185833))
- **Google Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone & Install

```bash
git clone https://github.com/shlokdhanokar/MAILFLOW.git
cd MAILFLOW
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env` — at minimum you need:

```env
EMAIL_ADDRESS=your-support@gmail.com
EMAIL_APP_PASSWORD=your-app-password
GEMINI_API_KEY=your-gemini-key
CLASSIFIER_MODE=gemini    # or "bert" if you have the model
DB_MODE=sqlite            # or "mysql" if you have MySQL
```

### 3. (Mode A only) Train the BERT Model

```bash
python train_model.py
```

This downloads `bert-base-uncased`, fine-tunes it on 100 sample emails across 4 categories, and saves the model to `email_bert_model/`. Takes ~3 minutes on CPU.

### 4. (Mode A only) Set Up MySQL

```sql
CREATE DATABASE IF NOT EXISTS email_tickets;
```

Then update `.env`:
```env
CLASSIFIER_MODE=bert
DB_MODE=mysql
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=email_tickets
```

### 5. Run the Agent

```bash
# Single processing cycle
python main.py

# Continuous polling mode (checks every 60 seconds)
python main.py --continuous --interval 60
```

### 6. Run the React Dashboard

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Testing the System

1. Send an email to your configured Gmail address:
   - *Subject:* "I was charged twice this month"
   - *Body:* "Hi, please refund the duplicate charge on my card."

2. Run `python main.py`

3. Watch the terminal — the AI will:
   - Classify it as **Billing Issue**
   - Store a ticket (e.g., `TICK-20260427-A3F1`)
   - Forward it to `payment.mailflow@gmail.com`
   - Send an AI-generated reply to the sender

4. Check the dashboard to see the new ticket appear

---

## Security

- **Never commit `.env`** — it's in `.gitignore`
- Use [Gmail App Passwords](https://support.google.com/accounts/answer/185833), not your real password
- The BERT model directory (`email_bert_model/`) is gitignored (438MB)

---

## License

This project is provided for educational and portfolio purposes.

---

<p align="center">
  Built with care by <a href="https://github.com/shlokdhanokar">shlokdhanokar</a>
</p>
