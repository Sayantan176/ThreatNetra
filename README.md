# Threat Netra / FinePrint Unified Platform

A unified, full-stack intelligence application offering two distinct tools under one roof:
1. **Threat Netra (OSINT Feed Analyzer)**: Autonomous Cyber Threat Intelligence (CTI) monitoring platform that parses Telegram and Bing News RSS feeds for real-time scenario matching.
2. **FinePrint**: An evidence-first AI analyst for consumer contracts that parses, highlights, and calculates financial costs from PDFs.

## Setup & Run

1. **Clone & Environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   Copy `.env.example` to `.env` and fill out your keys:
   - `GROQ_API_KEY`: For fast inference on both platforms.
   - `OPEN_ROUTER_GEMMA`: For Gemma 4 routing (optional).
   - `URL_API`: VirusTotal API Key for scanning extracted malicious URLs.

4. **Start the Unified Server**
   ```bash
   $env:PYTHONPATH="src"
   python server.py
   ```
   *Then visit **http://127.0.0.1:8000** in your browser to access the Unified Hub.*

---

## 🛡️ Tool 1: Threat Netra (OSINT Feed Analyzer)

An autonomous OSINT monitoring dashboard built for speed and precision.
- **Data Ingestion**: Parses Telegram (via RSS-Bridge) and Bing News.
- **AI Triage**: Uses strict Prompt Engineering to ensure the LLM explicitly matches news feeds against your Custom Alert Scenarios.
- **VirusTotal Integration**: Automatically extracts URLs shared in chatter and allows 1-click scanning against the VirusTotal DB.
- **Desktop Alerts**: Triggers OS-level notifications and in-browser toasts the second a threat scenario is matched.

## 📄 Tool 2: FinePrint

An AI legal assistant that strictly adheres to **Evidence Over Confidence**.
- **Quote Verification**: Every finding (cancellation fees, auto-renewal) carries an exact quote, page, and clause number. The system will discard unverified LLM hallucinations.
- **Deterministic Math**: The AI extracts terms; Python's `decimal` module safely computes the financial costs (never trusting the LLM to do arithmetic).
- **Compare Mode**: Upload two contracts side-by-side to find exactly what changed in the new version.
