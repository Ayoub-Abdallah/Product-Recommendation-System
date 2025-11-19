#!/bin/bash

# Beauty Recommendation API Startup Script

echo "=========================================="
echo "Beauty Recommendation API"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Checking dependencies..."
if ! pip show fastapi &> /dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    pip install faiss-cpu python-multipart pytest
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Check if beauty products file exists
if [ ! -f "data/beauty_products.json" ]; then
    echo ""
    echo "⚠️  WARNING: data/beauty_products.json not found!"
    echo "   Beauty recommender will not be available."
    echo "   Please make sure the file exists before starting."
    read -p "Continue anyway? (y/n): " continue
    if [ "$continue" != "y" ]; then
        echo "Exiting..."
        exit 1
    fi
else
    echo "✅ Beauty products file found"
fi

# Start the server
echo ""
echo "=========================================="
echo "Starting FastAPI server..."
echo "=========================================="
echo ""
echo "Server will be available at:"
echo "  📍 http://localhost:4708"
echo "  📍 http://localhost:4708/docs (API Documentation)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

./venv/bin/python -m uvicorn app:app --reload --host 0.0.0.0 --port 4708
