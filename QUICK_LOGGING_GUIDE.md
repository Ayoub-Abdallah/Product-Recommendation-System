# Quick Reference: Testing the Logging System

## 🚀 Quick Start

```bash
# Terminal 1: Start the server
./start_server.sh

# Terminal 2: Run the logging test
python test_logging.py
```

**Watch Terminal 1** to see all the detailed logs appear as the tests run!

## 📋 What You'll See

Each API call will show in the server console like this:

```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:30:45
================================================================================
Endpoint: [METHOD] [PATH]
[Parameters...]
================================================================================

[✅/⚠️/❌] RESPONSE: [Summary]
================================================================================
```

## 🧪 Manual Testing

### Test 1: Recommendation with Logging
```bash
curl -X POST "http://localhost:4708/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "health_supplements",
    "medical_conditions": ["diabetes"],
    "needs": ["energy"],
    "top_k": 3
  }'
```

**Expected Log:**
```
📥 INCOMING API CALL - [timestamp]
Endpoint: POST /recommend
  - Category: health_supplements
  - Medical Conditions: ['diabetes']
  - Needs: ['energy']
  ...
✅ RESPONSE: 3 recommendations returned
```

### Test 2: Product Lookup with Logging
```bash
# Successful lookup
curl "http://localhost:4708/product/supp-001"

# Not found (404)
curl "http://localhost:4708/product/xyz-999"
```

**Expected Logs:**
```
📥 INCOMING API CALL - [timestamp]
Endpoint: GET /product/supp-001
Product ID: supp-001
✅ RESPONSE: Product 'Sugar-Free Multivitamin for Diabetics' found

📥 INCOMING API CALL - [timestamp]
Endpoint: GET /product/xyz-999
Product ID: xyz-999
⚠️  RESPONSE: Product with ID 'xyz-999' not found (404)
```

### Test 3: Product Search with Logging
```bash
# Products found
curl "http://localhost:4708/product/search/vitamin"

# No products found
curl "http://localhost:4708/product/search/nonexistent"
```

**Expected Logs:**
```
📥 INCOMING API CALL - [timestamp]
Endpoint: GET /product/search/vitamin
Search Term: vitamin
✅ RESPONSE: 2 products found matching 'vitamin'

📥 INCOMING API CALL - [timestamp]
Endpoint: GET /product/search/nonexistent
Search Term: nonexistent
⚠️  RESPONSE: No products found matching 'nonexistent'
```

## 🐍 Python Test Examples

```python
import requests

BASE_URL = "http://localhost:4708"

# Test /recommend
requests.post(f"{BASE_URL}/recommend", json={
    "category": "health_supplements",
    "needs": ["energy"],
    "top_k": 3
})

# Test /product/{id}
requests.get(f"{BASE_URL}/product/supp-001")

# Test /product/search/{term}
requests.get(f"{BASE_URL}/product/search/baby")
```

## 📊 Log Symbols

| Symbol | Meaning |
|--------|---------|
| 📥 | Incoming API request |
| ✅ | Successful response |
| ⚠️  | Warning (not found, no results) |
| ❌ | Error occurred |

## 🔍 Filtering Logs

If server is logging to a file:

```bash
# Only show incoming requests
tail -f logs/api.log | grep "📥"

# Only show errors
tail -f logs/api.log | grep "❌"

# Only show /recommend calls
tail -f logs/api.log | grep "POST /recommend"

# Show all searches
tail -f logs/api.log | grep "Search Term:"
```

## ✅ Verification Checklist

After running `test_logging.py`, verify you see:

- [ ] Multiple "📥 INCOMING API CALL" headers
- [ ] Timestamps for each request
- [ ] Endpoint paths (POST /recommend, GET /product/..., etc.)
- [ ] Request parameters logged
- [ ] Response summaries (✅ or ⚠️)
- [ ] Clear visual separators (====)

## 📚 Full Documentation

For complete details, see:
- **`API_LOGGING_DOCUMENTATION.md`** - Complete logging guide
- **`LOGGING_IMPLEMENTATION_SUMMARY.md`** - Implementation details

## 🎯 Key Points

✅ **All endpoints have logging** (recommend, product lookup, search)  
✅ **Automatic** - no configuration needed  
✅ **Clear format** - easy to read and filter  
✅ **Timestamps** - track when requests happen  
✅ **Error tracking** - see what went wrong  
✅ **Production-ready** - works in development and production  

## ⚡ That's It!

The logging system is ready to use. Just start the server and make API calls - all requests and responses will be logged automatically! 🎉
