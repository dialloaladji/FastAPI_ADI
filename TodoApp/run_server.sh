#!/bin/bash
# FastAPI Development Server Runner
# This script ensures the server restarts with clean Python cache

# Clear Python cache
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -r {} + 2>/dev/null

# Kill any existing uvicorn processes on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start the server with auto-reload
echo "Starting FastAPI server with auto-reload..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

