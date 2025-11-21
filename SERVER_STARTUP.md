# Server Startup Guide

## 🚀 How to Start the Server

The server **MUST** run on port **4708** (not the default 8000).

### ✅ Correct Ways to Start:

**Option 1: Use the startup script (Recommended)**
```bash
./start_server.sh
```

**Option 2: Use the quick run script**
```bash
./run.sh
```

**Option 3: Manual command**
```bash
./venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 4708 --reload
```

OR with your activated venv:
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 4708 --reload
```

### ❌ Wrong (Will use port 8000):
```bash
python3 -m uvicorn app:app  # Missing --port 4708
python -m uvicorn app:app   # Missing --port 4708
```

---

## 🔍 Verify Server is Running

After starting, check:
```bash
curl http://localhost:4708/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "Intelligent Multi-Category Recommendation System",
  "version": "3.0"
}
```

---

## 📍 Important URLs

- **Health Check:** http://localhost:4708/health
- **API Docs:** http://localhost:4708/docs
- **Web UI:** http://localhost:4708/
- **Recommendations:** POST http://localhost:4708/recommend
- **Product Lookup:** GET http://localhost:4708/product/{id}
- **Product Search:** GET http://localhost:4708/product/search/{term}

---

## 🛠️ Flags Explained

- `--host 0.0.0.0` - Makes server accessible from network (not just localhost)
- `--port 4708` - **REQUIRED!** Sets the port to 4708 (default is 8000)
- `--reload` - Auto-reload on code changes (useful for development)

---

## 💡 Remember

**Always specify `--port 4708`** when starting the server!

All tests and documentation assume port 4708.
