# 🚀 Beauty & Health Recommendation API - Quick Reference

## 📍 Base URL
```
http://localhost:4708
```

---

## 🎯 Main Endpoints

### 1. Get Recommendations (POST /recommend)

**Purpose:** Get personalized beauty & health product recommendations

**URL:** `POST http://localhost:4708/recommend`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "summary": {
    "skin_type": "oily",
    "concerns": ["acne"],
    "budget": 2500
  },
  "top_k": 3,
  "language": "en"
}
```

**Example with cURL:**
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

**Example with Python:**
```python
import requests

url = "http://localhost:4708/recommend"
data = {
    "summary": {
        "skin_type": "oily",
        "concerns": ["acne"],
        "budget": 2500
    },
    "top_k": 3
}

response = requests.post(url, json=data)
print(response.json())
```

**Example with JavaScript:**
```javascript
fetch('http://localhost:4708/recommend', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    summary: {
      skin_type: 'oily',
      concerns: ['acne'],
      budget: 2500
    },
    top_k: 3
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": "beauty-005",
      "name": "Salicylic Acid 2% Acne Treatment",
      "price": 2200,
      "currency": "DA",
      "category": "skin_care",
      "subcategory": "treatment",
      "tags": ["acne", "oily_skin", "blackheads"],
      "description": "BHA treatment for acne-prone skin",
      "reason": "Perfect for your oily skin type • Addresses your acne concern • Within your budget (2200 DA)",
      "score": 0.949
    }
  ],
  "count": 1,
  "metadata": {
    "warnings": [],
    "budget_info": {
      "requested_budget": 2500,
      "products_in_budget": 8,
      "cheapest_available": 1500
    }
  }
}
```

---

### 2. Get All Products (GET /products)

**Purpose:** List all available products

**URL:** `GET http://localhost:4708/products`

**Example with cURL:**
```bash
curl http://localhost:4708/products
```

**Example with Python:**
```python
import requests

response = requests.get("http://localhost:4708/products")
products = response.json()
print(f"Total products: {len(products)}")
```

**Response:**
```json
[
  {
    "id": "beauty-001",
    "name": "Hyaluronic Acid Serum",
    "price": 2800,
    "category": "skin_care",
    "subcategory": "serum",
    "skin_type": ["dry", "normal"],
    "tags": ["hydration", "anti_aging"]
  }
]
```

---

### 3. Get Categories (GET /categories)

**Purpose:** Get all available categories and subcategories

**URL:** `GET http://localhost:4708/categories`

**Example with cURL:**
```bash
curl http://localhost:4708/categories
```

**Response:**
```json
{
  "skin_care": ["serum", "moisturizer", "cleanser", "treatment"],
  "hair_care": ["shampoo", "treatment"],
  "supplements": ["vitamins", "beauty_supplements"],
  "wellness": ["sleep_support", "digestive_health"],
  "makeup": ["foundation"]
}
```

---

### 4. Get Statistics (GET /stats)

**Purpose:** Get system statistics and index information

**URL:** `GET http://localhost:4708/stats`

**Example with cURL:**
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

---

### 5. Health Check (GET /health)

**Purpose:** Check if the API is running

**URL:** `GET http://localhost:4708/health`

**Example with cURL:**
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

---

## 📝 Summary Fields Reference

### All Fields are Optional

```json
{
  "summary": {
    // Skin & Hair Types
    "skin_type": "oily | dry | combination | normal | sensitive",
    "hair_type": "oily | dry | normal | curly | straight | wavy",
    
    // Categories
    "category": "skin_care | hair_care | makeup | supplements | wellness",
    "product_type": "serum | cream | shampoo | vitamin | etc",
    
    // Concerns (array)
    "concerns": ["acne", "wrinkles", "dark_spots", "hair_loss", "frizz"],
    
    // Budget
    "budget": 2500,              // Numeric (in DA)
    "budget": "low",             // Or categorical: "low" | "medium" | "high"
    
    // Demographics
    "age": "25",                 // String or number
    "gender": "female | male | unisex",
    
    // Language
    "language": "en | ar | fr"
  },
  "top_k": 3,                    // Number of recommendations (1-10)
  "language": "en"               // Response language
}
```

---

## 🎯 Common Use Cases

### 1. Simple Skin Care Recommendation
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "concerns": ["acne"]
    },
    "top_k": 3
  }'
```

### 2. Hair Care with Budget
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "hair_type": "dry",
      "category": "hair_care",
      "budget": "medium",
      "concerns": ["frizz"]
    },
    "top_k": 5
  }'
```

### 3. Anti-Aging Products
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "dry",
      "concerns": ["wrinkles", "fine_lines"],
      "budget": 4000,
      "age": "40+"
    },
    "top_k": 3
  }'
```

### 4. Supplements & Wellness
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "category": "supplements",
      "concerns": ["energy", "immunity"],
      "budget": "medium"
    },
    "top_k": 3
  }'
```

### 5. French Language Response
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "dry",
      "concerns": ["wrinkles"],
      "language": "fr"
    },
    "top_k": 3,
    "language": "fr"
  }'
```

---

## 🌐 Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI:** http://localhost:4708/docs
- **ReDoc:** http://localhost:4708/redoc

These provide:
- ✅ Interactive API testing
- ✅ Request/response examples
- ✅ Schema validation
- ✅ Try it out feature

---

## ⚠️ Budget Warnings

The API returns warnings when:

1. **Budget too low:**
```json
{
  "metadata": {
    "warnings": [
      {
        "type": "budget",
        "severity": "high",
        "message": "No products found within budget of 500.0 DA. Showing closest alternatives.",
        "suggestion": "Consider increasing budget to at least 1500 DA"
      }
    ]
  }
}
```

2. **Few results:**
```json
{
  "metadata": {
    "warnings": [
      {
        "type": "results",
        "severity": "medium",
        "message": "Only 1 products match your criteria.",
        "suggestion": "Try removing skin_type, hair_type, or category filters"
      }
    ]
  }
}
```

---

## 📊 Response Metadata

Every recommendation response includes:

```json
{
  "recommendations": [...],
  "count": 3,
  "metadata": {
    "warnings": [],
    "budget_info": {
      "requested_budget": 2500,
      "cheapest_available": 1500,
      "products_in_budget": 8,
      "products_over_budget": 7,
      "budget_type": "numeric",
      "most_expensive": 4200,
      "average_price": 2593.33
    },
    "search_info": {
      "total_candidates": 15,
      "after_filtering": 15
    }
  }
}
```

---

## 🔧 Testing the API

### Test with cURL
```bash
# Simple test
curl http://localhost:4708/health

# Full recommendation test
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

### Test with Python Script
Create `test_api.py`:
```python
import requests
import json

url = "http://localhost:4708/recommend"
data = {
    "summary": {
        "skin_type": "oily",
        "concerns": ["acne"],
        "budget": 2500
    },
    "top_k": 3
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
```

Run: `python test_api.py`

---

## 🚀 Quick Start

1. **Start the server:**
```bash
./start_server.sh
```

2. **Test the API:**
```bash
curl http://localhost:4708/health
```

3. **Get recommendations:**
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

4. **Open the web UI:**
```
http://localhost:4708
```

5. **View API docs:**
```
http://localhost:4708/docs
```

---

## 📞 Need Help?

- Check `/health` endpoint first
- Use `/docs` for interactive testing
- See `test_fix.py` for example usage
- Read `SUCCESS_SUMMARY.md` for complete info

**Server Status:** http://localhost:4708/health  
**API Docs:** http://localhost:4708/docs  
**Web UI:** http://localhost:4708
