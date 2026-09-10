# JARVIS AI Frontend

Modern React-based web interface for JARVIS AI

## Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on `http://localhost:3000`

## Features

- Real-time chat interface
- Dark/Light mode toggle
- Model usage indicator (Groq/Gemini)
- Response time tracking
- Responsive design (mobile, tablet, desktop)
- Message history

## File Structure

```
src/
├── App.js                 # Main app component
├── index.js              # Entry point
├── components/
│   ├── ChatInterface.js  # Main chat component
│   ├── Sidebar.js        # Navigation sidebar
│   └── Header.js         # Top header
└── index.css             # Global styles
```

## API Integration

Connects to backend at `http://localhost:8000`

Endpoints used:
- `POST /query` - Send chat query
- `GET /health` - Check backend health
- `GET /models` - Get available models

## Styling

Uses Tailwind CSS for styling. Configuration in `tailwind.config.js`
