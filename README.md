# JARVIS AI - Open Source Personal Assistant

🤖 A powerful, free, open-source AI assistant with PC control, browser automation, smart home integration, and Twilio support.

**Features:**
- ⚡ Dual LLM Architecture (Groq for fast responses, Gemini for complex tasks)
- 🎮 PC & Browser Control
- 🏠 Smart Home Integration
- 📱 Twilio Voice & SMS
- 🎨 Modern Web Interface
- 💰 100% Free (Gemini + Groq Free APIs)
- 🔒 Privacy-Focused (runs locally)

## Quick Start

### Docker (Easiest)
```bash
git clone https://github.com/richi6r55/jarvis-ai.git
cd jarvis-ai
bash docker-start.sh
```

### Manual Setup
```bash
git clone https://github.com/richi6r55/jarvis-ai.git
cd jarvis-ai
pip install -r requirements.txt
cd frontend && npm install && cd ..
copy .env.example .env
# Edit .env with API keys
python backend/main.py  # Terminal 1
cd frontend && npm start  # Terminal 2
```

## Get API Keys (FREE)

1. **Google Gemini**: https://aistudio.google.com/
2. **Groq**: https://groq.com/ai/

## Access

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Documentation

- [Setup Guide](README.md)
- [Docker Guide](DOCKER.md)
- [Testing Guide](TESTING.md)
- [Deployment Guide](DEPLOYMENT.md)

## License

MIT License
