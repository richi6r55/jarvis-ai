#!/bin/bash

# JARVIS AI Setup Script
# Automatically sets up the project

echo "🚀 JARVIS AI Setup"
echo "=================="

# Check Python version
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi
python_version=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $python_version found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
echo "This may take a few minutes..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Check Node.js
echo ""
echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js not found. Frontend won't work without it."
    echo "Install from: https://nodejs.org/"
else
    node_version=$(node --version)
    echo "✓ Node.js $node_version found"
    
    # Install frontend dependencies
    if [ ! -d "frontend/node_modules" ]; then
        echo ""
        echo "Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
        echo "✓ Frontend dependencies installed"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your API keys:"
    echo "   1. Get GEMINI_API_KEY from https://aistudio.google.com/"
    echo "   2. Get GROQ_API_KEY from https://groq.com/ai/"
    echo "   3. (Optional) Get Twilio credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: bash start.sh"
echo ""
