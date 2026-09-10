# JARVIS AI

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18+-blue)

🤖 **Open-source AI Personal Assistant with Dual LLM Architecture**

### ⚡ Features

- 🧠 **Dual LLM System**
  - Groq (Ultra-fast responses) 
  - Google Gemini (Complex reasoning)
  - Automatic routing based on query complexity

- 🎮 **PC & Browser Control**
  - Mouse & keyboard automation
  - Application launching
  - Website navigation and interaction

- 🏠 **Smart Home Integration**
  - Control lights, thermostats, devices
  - Home Assistant compatible
  - Voice automation support

- 📞 **Communication**
  - Twilio SMS integration
  - Voice calls
  - Message handling

- 🎨 **Modern Web Interface**
  - Real-time chat
  - Dark/Light mode
  - Responsive design
  - Model usage tracking

- 💰 **100% Free**
  - Gemini Free API
  - Groq Free API
  - No hidden costs

- 🔒 **Privacy-First**
  - Runs locally
  - No data sharing
  - Open-source code

### 🚀 Quick Start

#### Option 1: Docker (Easiest)
```bash
git clone https://github.com/richi6r55/jarvis-ai.git
cd jarvis-ai
bash docker-start.sh
```

#### Option 2: Manual Setup (Windows)
```bash
git clone https://github.com/richi6r55/jarvis-ai.git
cd jarvis-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with API keys
python backend/main.py  # Terminal 1
cd frontend && npm start  # Terminal 2
```

#### Option 3: Manual Setup (Linux/Mac)
```bash
git clone https://github.com/richi6r55/jarvis-ai.git
cd jarvis-ai
bash setup.sh
nano .env  # Edit with API keys
bash start.sh
```

### 📋 Get API Keys (Free)

1. **Google Gemini** (Free)
   - Go to https://aistudio.google.com/
   - Click "Get API Key"
   - Copy your key

2. **Groq** (Free)
   - Go to https://groq.com/ai/
   - Sign up
   - Get API key

### 🌐 Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 📊 Architecture

```
┌─────────────────────────────────┐
│    JARVIS Web Interface (React)  │
├─────────────────────────────────┤
│    FastAPI Backend (Python)      │
├─────────────────────────────────┤
│  ┌──────────────────────────┐   │
│  │  Dual LLM Router         │   │
│  │  ├─ Groq (Fast)          │   │
│  │  └─ Gemini (Complex)     │   │
│  └──────────────────────────┘   │
├─────────────────────────────────┤
│  ┌──────────────────────────┐   │
│  │  Action Modules          │   │
│  │  ├─ PC Control           │   │
│  │  ├─ Browser              │   │
│  │  ├─ Smart Home           │   │
│  │  └─ Twilio              │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

### 💬 Example Queries

**Simple Queries (Uses Groq - ⚡ Fast)**
```
"What is the weather?"
"Tell me a joke"
"What time is it?"
```

**Complex Queries (Uses Gemini - 🧠 Smart)**
```
"Analyze this code for security issues"
"Help me write a complex essay"
"Create a detailed project plan"
```

**Actions**
```
"Open Chrome and go to Google"
"Turn on the living room lights"
"Send SMS to Mom: I'm on my way"
```

### 📚 Documentation

- [Setup Guide](README.md) - Detailed setup instructions
- [Docker Guide](DOCKER.md) - Docker deployment
- [Testing Guide](TESTING.md) - Run tests and check health
- [Deployment Guide](DEPLOYMENT.md) - Production deployment
- [API Documentation](http://localhost:8000/docs) - Interactive API docs

### 🧪 Testing

```bash
# Check health
curl http://localhost:8000/health

# Run test query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}'

# Run integration tests
bash tests/test_api.sh
```

### ⚙️ Configuration

Edit `.env` file:
```env
# Required
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Optional
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE=

HOME_ASSISTANT_URL=http://localhost:8123
HOME_ASSISTANT_TOKEN=
```

### 🔧 Troubleshooting

**"Module not found" error**
```bash
pip install -r requirements.txt
```

**Port already in use**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**API keys not working**
- Verify keys are correctly pasted in .env
- Restart the backend: `python backend/main.py`
- Check health endpoint: `curl http://localhost:8000/health`

### 📈 Rate Limits

- **Groq**: 30 requests/minute
- **Gemini**: 60 requests/minute, 1500/day
- System automatically handles limits with intelligent retry

### 🤝 Contributing

Contributions welcome! Areas to improve:
- [ ] Mobile app (React Native)
- [ ] More LLM providers
- [ ] Local LLM fallback (Ollama)
- [ ] Voice output (TTS)
- [ ] Database persistence
- [ ] Advanced smart home features

### 📜 License

MIT License - See [LICENSE](LICENSE) file

### ⭐ Support

If you find this useful, please:
- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest features
- 📢 Share with others

### 📞 Get Help

- 🐛 [Report Issues](https://github.com/richi6r55/jarvis-ai/issues)
- 💬 [Discussions](https://github.com/richi6r55/jarvis-ai/discussions)
- 📖 [Documentation](https://github.com/richi6r55/jarvis-ai/wiki)

---

**Made with ❤️ for the open-source community**
