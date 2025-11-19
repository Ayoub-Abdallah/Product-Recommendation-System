# 🎯 API Endpoint & Usage Guide

## 📍 Server Information
- **Base URL:** `http://localhost:4708`
- **Status:** ✅ Running
- **Documentation:** http://localhost:4708/docs
- **Web UI:** http://localhost:4708

---

## 🚀 Main Endpoint: POST /recommend

### Quick Example

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

### Response (Real Example from Your Server):
```json
{
  "recommendations": [
    {
      "id": "hind-003",
      "name": "Salicylic Acid 2% Acne Treatment",
      "price": 2200,
      "currency": "DA",
      "category": "skin_care",
      "subcategory": "treatment",
      "tags": ["acne", "oily_skin", "blackheads"],
      "description": "Unclogs pores, treats acne and prevents breakouts",
      "reason": "Perfect for your oily skin type • Within your budget (2200 DA)",
      "score": 1.261
    }
  ],
  "count": 3,
  "metadata": {
    "budget_info": {
      "requested_budget": 2500,
      "products_in_budget": 7,
      "cheapest_available": 1800
    }
  }
}
```

---

## 📝 All Available Endpoints

| Method | Endpoint | Purpose | Example |
|--------|----------|---------|---------|
| `POST` | `/recommend` | Get recommendations | See above |
| `GET` | `/products` | List all products | `curl http://localhost:4708/products` |
| `GET` | `/categories` | Get categories | `curl http://localhost:4708/categories` |
| `GET` | `/stats` | System statistics | `curl http://localhost:4708/stats` |
| `GET` | `/health` | Health check | `curl http://localhost:4708/health` |
| `GET` | `/` | Web UI | Open in browser |
| `GET` | `/docs` | API Documentation | Open in browser |

---

## 💡 Request Examples

### 1. Basic Skin Care
```json
{
  "summary": {
    "skin_type": "oily"
  },
  "top_k": 3
}
```

### 2. With Concerns
```json
{
  "summary": {
    "skin_type": "dry",
    "concerns": ["wrinkles", "fine_lines"]
  },
  "top_k": 5
}
```

### 3. With Budget (Numeric)
```json
{
  "summary": {
    "hair_type": "curly",
    "budget": 2000,
    "concerns": ["frizz"]
  },
  "top_k": 3
}
```

### 4. With Budget (Categorical)
```json
{
  "summary": {
    "category": "supplements",
    "budget": "medium"
  },
  "top_k": 3
}
```

### 5. Specific Category
```json
{
  "summary": {
    "category": "hair_care",
    "hair_type": "dry",
    "product_type": "shampoo"
  },
  "top_k": 2
}
```

### 6. Multi-language (French)
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

## 🔧 How to Call the API

### Option 1: cURL (Command Line)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {"skin_type": "oily"},
    "top_k": 3
  }'
```

### Option 2: Python
```python
import requests

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "summary": {"skin_type": "oily"},
        "top_k": 3
    }
)
print(response.json())
```

### Option 3: JavaScript/Node.js
```javascript
fetch('http://localhost:4708/recommend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    summary: {skin_type: 'oily'},
    top_k: 3
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### Option 4: Postman
1. Method: `POST`
2. URL: `http://localhost:4708/recommend`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "summary": {"skin_type": "oily"},
  "top_k": 3
}
```

---

## 📊 Summary Field Options

```javascript
{
  "summary": {
    // Skin & Hair Types
    "skin_type": "oily | dry | combination | normal | sensitive",
    "hair_type": "oily | dry | normal | curly | straight | wavy",
    
    // Categories
    "category": "skin_care | hair_care | makeup | supplements | wellness",
    
    // Concerns (array of strings)
    "concerns": ["acne", "wrinkles", "frizz", "energy"],
    
    // Budget (number or string)
    "budget": 2500,           // Numeric in DA
    "budget": "low",          // Or "medium" or "high"
    
    // Language
    "language": "en | ar | fr"
  },
  
  // Number of recommendations to return (1-10)
  "top_k": 3,
  
  // Response language
  "language": "en"
}
```

---

## ✅ Test Your Setup

Run these commands to verify everything works:

```bash
# 1. Check server health
curl http://localhost:4708/health

# 2. Get statistics
curl http://localhost:4708/stats

# 3. Get all products
curl http://localhost:4708/products

# 4. Get categories
curl http://localhost:4708/categories

# 5. Get recommendations
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

---

## 🌐 Interactive Testing

**Best way to test:** Open in your browser:
```
http://localhost:4708/docs
```

This gives you:
- ✅ Interactive API playground
- ✅ Auto-generated examples
- ✅ Schema validation
- ✅ "Try it out" button for each endpoint

---

## 📱 Complete Working Example

Save this as `test_api.py`:

```python
import requests
import json

# API endpoint
url = "http://localhost:4708/recommend"

# Request data
data = {
    "summary": {
        "skin_type": "oily",
        "concerns": ["acne"],
        "budget": 2500
    },
    "top_k": 3
}

# Make request
response = requests.post(url, json=data)

# Print response
if response.status_code == 200:
    result = response.json()
    print(f"✅ Got {result['count']} recommendations:\n")
    
    for i, product in enumerate(result['recommendations'], 1):
        print(f"{i}. {product['name']}")
        print(f"   💰 Price: {product['price']} {product['currency']}")
        print(f"   📦 Category: {product['category']} > {product['subcategory']}")
        print(f"   💡 Reason: {product['reason']}")
        print(f"   ⭐ Score: {product['score']:.3f}\n")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
```

Run: `python3 test_api.py`

---

## 🎯 Summary

**Main Endpoint:** `POST http://localhost:4708/recommend`

**Minimal Request:**
```json
{"summary": {"skin_type": "oily"}, "top_k": 3}
```

**Full Request:**
```json
{
  "summary": {
    "skin_type": "oily",
    "hair_type": "dry",
    "category": "skin_care",
    "concerns": ["acne", "wrinkles"],
    "budget": 2500,
    "language": "en"
  },
  "top_k": 5,
  "language": "en"
}
```

**📚 More Info:**
- Full docs: `API_QUICK_REFERENCE.md`
- Interactive: http://localhost:4708/docs
- Web UI: http://localhost:4708
