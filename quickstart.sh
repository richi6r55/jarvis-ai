#!/bin/bash

# Quick start script for development
# Combines setup and start

echo "🚀 JARVIS AI - Quick Start"
echo "==========================="
echo ""

# Run setup if needed
if [ ! -d "venv" ]; then
    echo "First time setup..."
    bash setup.sh
    echo ""
fi

# Start the app
bash start.sh
