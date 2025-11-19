# 📖 API Endpoint Summary

## 🎯 Quick Answer: How to Call the API

### Main Endpoint
```
POST http://localhost:4708/recommend
```

### Minimal Request
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

### Full Request Example
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "concerns": ["acne"],
      "budget": 2500
    },
    "top_k": 3
  }'
```

---

## 📚 All Available Endpoints

### 1. **POST /recommend** - Get Recommendations ⭐ MAIN ENDPOINT
**URL:** `http://localhost:4708/recommend`

**Request:**
```json
{
  "summary": {
    "skin_type": "oily | dry | combination | normal | sensitive",
    "hair_type": "oily | dry | normal | curly | straight | wavy",
    "category": "skin_care | hair_care | makeup | supplements | wellness",
    "concerns": ["acne", "wrinkles", "frizz", "energy"],
    "budget": 2500,  // or "low" | "medium" | "high"
    "language": "en | ar | fr"
  },
  "top_k": 3
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": "hind-003",
      "name": "Salicylic Acid 2% Acne Treatment",
      "price": 2200,
      "currency": "DA",
      "category": "skin_care",
      "tags": ["acne", "oily_skin"],
      "reason": "Perfect for your oily skin type",
      "score": 1.146
    }
  ],
  "count": 3,
  "metadata": {
    "budget_info": {...},
    "warnings": [...]
  }
}
```

### 2. **GET /products** - List All Products
**URL:** `http://localhost:4708/products`

```bash
curl http://localhost:4708/products
```

### 3. **GET /categories** - Get Categories
**URL:** `http://localhost:4708/categories`

```bash
curl http://localhost:4708/categories
```

### 4. **GET /stats** - System Statistics
**URL:** `http://localhost:4708/stats`

```bash
curl http://localhost:4708/stats
```

**Response:**
```json
{
  "total_products": 24,
  "in_stock": 24,
  "categories": {
    "skin_care": 11,
    "hair_care": 4,
    "supplements": 5,
    "wellness": 2,
    "makeup": 2
  },
  "index_type": "IndexFlatIP"
}
```

### 5. **GET /health** - Health Check
**URL:** `http://localhost:4708/health`

```bash
curl http://localhost:4708/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Beauty & Health Recommendation System",
  "products_loaded": 24,
  "categories": 5
}
```

### 6. **GET /** - Web UI
**URL:** `http://localhost:4708`

Open in browser for interactive web interface.

### 7. **GET /docs** - Interactive API Documentation
**URL:** `http://localhost:4708/docs`

Open in browser for Swagger UI with "Try it out" feature.

---

## 💻 How to Call from Different Languages

### cURL (Command Line)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "summary": {"skin_type": "oily", "concerns": ["acne"]},
        "top_k": 3
    }
)
print(response.json())
```

### JavaScript (Fetch)
```javascript
fetch('http://localhost:4708/recommend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    summary: {skin_type: 'oily', concerns: ['acne']},
    top_k: 3
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### Node.js (Axios)
```javascript
const axios = require('axios');

axios.post('http://localhost:4708/recommend', {
  summary: {skin_type: 'oily', concerns: ['acne']},
  top_k: 3
})
.then(response => console.log(response.data));
```

---

## 🧪 Test the API

### Option 1: Run Test Script
```bash
./venv/bin/python test_api_simple.py
```

### Option 2: Manual Test
```bash
# 1. Check health
curl http://localhost:4708/health

# 2. Get recommendations
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

### Option 3: Interactive Docs
Open in browser:
```
http://localhost:4708/docs
```

---

## 📊 Summary Field Reference

| Field | Type | Options | Example |
|-------|------|---------|---------|
| `skin_type` | string | oily, dry, combination, normal, sensitive | `"oily"` |
| `hair_type` | string | oily, dry, normal, curly, straight, wavy | `"curly"` |
| `category` | string | skin_care, hair_care, makeup, supplements, wellness | `"skin_care"` |
| `concerns` | array | acne, wrinkles, frizz, energy, etc. | `["acne", "dark_spots"]` |
| `budget` | number/string | 2500 or "low", "medium", "high" | `2500` or `"medium"` |
| `language` | string | en, ar, fr | `"en"` |
| `top_k` | number | 1-10 | `3` |

---

## 🎯 Common Use Cases

### 1. Oily Skin with Acne
```json
{
  "summary": {
    "skin_type": "oily",
    "concerns": ["acne"],
    "budget": 2500
  },
  "top_k": 3
}
```

### 2. Dry Skin Anti-Aging
```json
{
  "summary": {
    "skin_type": "dry",
    "concerns": ["wrinkles", "fine_lines"],
    "budget": 3000
  },
  "top_k": 5
}
```

### 3. Curly Hair Care
```json
{
  "summary": {
    "hair_type": "curly",
    "category": "hair_care",
    "concerns": ["frizz"],
    "budget": "medium"
  },
  "top_k": 3
}
```

### 4. Supplements for Energy
```json
{
  "summary": {
    "category": "supplements",
    "concerns": ["energy", "immunity"]
  },
  "top_k": 3
}
```

### 5. French Language
```json
{
  "summary": {
    "skin_type": "dry",
    "concerns": ["wrinkles"],
    "language": "fr"
  },
  "top_k": 3,
  "language": "fr"
}
```

---

## ✅ Verify Setup

Run these commands:

```bash
# 1. Check if server is running
curl http://localhost:4708/health

# 2. Get system stats
curl http://localhost:4708/stats

# 3. Test recommendation
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

---

## 🔗 Quick Links

- **Web UI:** http://localhost:4708
- **API Docs:** http://localhost:4708/docs
- **Health Check:** http://localhost:4708/health
- **Statistics:** http://localhost:4708/stats

---

## 📚 More Resources

- `HOW_TO_CALL_API.md` - Detailed guide with examples
- `API_QUICK_REFERENCE.md` - Complete API reference
- `test_api_simple.py` - Ready-to-run test script
- `SUCCESS_SUMMARY.md` - System overview

---

## 🚀 That's It!

The simplest way to get started:

```bash
# Start the server
./start_server.sh

# Test it
curl http://localhost:4708/health

# Get recommendations
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

**Or open in browser:**
- Web UI: http://localhost:4708
- API Docs: http://localhost:4708/docs
