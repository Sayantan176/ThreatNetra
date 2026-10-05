# 🛡️ Threat Intelligence Platform - Project Context

## Overview
An autonomous Cyber Threat Intelligence (CTI) monitoring platform that ingests raw telemetry from Telegram channels (via RSS-Bridge) and Bing News Search. It utilizes a configurable Large Language Model backend (Google Gemma 2 or Groq Qwen/LLaMA-3) to perform real-time triage, noise filtering, and strict scenario matching based on analyst-provided rules.

## Architecture & Tech Stack
* **Backend:** FastAPI, Python 3.12+ (Uvicorn ASGI)
* **Frontend:** Vanilla HTML5, JavaScript, Tailwind CSS (via CDN)
* **LLM Providers:**
  * Google GenAI SDK (`GEMINI_API_KEY`): Configured explicitly for native Gemma 2 (`gemma-2-27b-it`, `gemma-2-9b-it`).
  * Groq SDK (`GROQ_API_KEY`): Optimized for extreme speed/low-token cost using `qwen/qwen3.8-27b` and `allam-2-7b`.
* **Data Sources:**
  * **Telegram:** Parsed via active instances from `bridge.txt` (RSS-Bridge).
  * **OSINT:** Parsed via Bing News RSS URL queries.
* **RSS Parser:** Uses `feedparser` and `httpx` for async network calls.

## Core Services Layer
1. **`app/models.py`:**
   * Contains Pydantic `AnalyzeRequest` schema for request validation (validates source, provider, query, and scenario inputs).
2. **`app/services/fetcher.py`:**
   * Exposes `fetch_telegram(username)` and `fetch_bing(query)`.
   * Randomly load-balances Telegram RSS requests across active bridges to prevent rate-limiting.
   * Returns a parsed array of dictionaries and the exact target RSS URL.
3. **`app/services/analyzer.py`:**
   * Implements strict Prompt Engineering and Chain-of-Thought reasoning.
   * Forces the LLMs to internally generate `"reasoning"` before resolving `"is_scenario_match"` to a strict boolean, thereby preventing false-positive hallucination loops typically seen in smaller (<30B param) models.
   * Implements automated cascade fallbacks (e.g. catches `429` / `503` / `404` errors and shifts to alternate models automatically).
   * Generates mock fallback data if `.env` keys are missing.

## UI / Frontend Behaviors (`static/index.html`)
* **Continuous Polling:** Once "Start Monitoring" is clicked, JS `setInterval` routinely hits the `/api/v1/analyze` endpoint.
* **Light/Dark Mode:** Dynamic Tailwind CSS variables override, persisting state in `localStorage.theme`.
* **Popup Notifications:** Triggers sliding Toast notifications and OS-level Web Notifications exclusively when `scenario_matched` passes strict string validation.
* **State Persistence:** A `seenAlertTitles` JavaScript Set acts as an anti-spam cache to ensure an article never triggers duplicate alerts during a single session.
* **Alert Log Table:** Permanently logs verified alerts at the bottom of the dashboard.

## Production Status
* Fully containerized via `Dockerfile` and `docker-compose.yml`.
* Configured with `logging` instead of simple print statements.
* Protected via `.gitignore` and scaffolded via `.env.example`.
* Integrated CORS middleware inside `main.py` allowing detached frontend deployments.