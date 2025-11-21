#!/bin/bash
# Quick start script - just runs the server on port 4708

./venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 4708 --reload
