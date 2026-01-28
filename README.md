# ReadCast AI (MVP)

> **Turn your "Read Later" list into a personalized AI Podcast.**

## 1. Project Overview
ReadCast is an AI agent that ingests articles from various sources (WeChat, Twitter, Browser), analyzes them, and converts them into an engaging audio podcast format.

## 2. Tech Stack (MVP)
- **Backend:** Python 3.10+
- **Framework:** FastAPI
- **Database:** SQLite (local `readcast.db`)
- **AI/LLM:** OpenAI API / DeepSeek (via compatible endpoint)
- **TTS:** EdgeTTS (Free/MVP) or ElevenLabs (Premium)

## 3. Core Features (Phase 1)
1.  **Ingestion API:** Endpoint to receive URLs from extensions/shortcuts.
2.  **Parser:** Extract clean text from HTML.
3.  **Digest Engine:** LLM summarizes and connects multiple articles.
4.  **Audio Gen:** Generate simple TTS audio file.

## 4. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

## 5. API Endpoints
- `POST /api/v1/ingest`: Submit a URL.
- `POST /api/v1/generate-podcast`: Trigger podcast generation for unread items.
- `GET /api/v1/feed`: Get the RSS feed of generated podcasts.
