#!/bin/bash
# Beauty & Health Recommendation System - Test Runner

echo "🧪 Beauty & Health Recommendation System - Test Suite"
echo "======================================================"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./start_server.sh first."
    exit 1
fi

# Run tests
echo "Running Test 1: Strict Filtering..."
echo "----------------------------------------------------"
./venv/bin/python test_fix.py
echo ""

echo "Running Test 2: Budget Warnings & Metadata..."
echo "----------------------------------------------------"
./venv/bin/python test_budget_warnings.py
echo ""

echo "Running Test 3: Full Catalog Test..."
echo "----------------------------------------------------"
./venv/bin/python test_full_catalog.py
echo ""

echo "======================================================"
echo "✅ All tests completed!"
echo "======================================================"
