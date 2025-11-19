# Quick Start Guide

## Setup and Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Beauty Products File
Make sure `data/beauty_products.json` exists with beauty product data.

### 3. Start the Server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✅ Loaded 10 products with FAISS ANN index
✅ Loaded 10 beauty products with FAISS index
✅ Beauty recommender loaded
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Test the API

#### Option A: Use the Test Script
```bash
python test_summary_api.py
```

#### Option B: Use curl
```bash
# Test health
curl http://localhost:8000/health

# Test recommendation
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "problem": "acne",
      "budget": "medium"
    },
    "top_k": 3,
    "language": "en"
  }'
```

#### Option C: Use Python
```python
import requests

response = requests.post('http://localhost:8000/recommend/summary', json={
    "summary": {
        "skin_type": "oily",
        "problem": "acne"
    },
    "top_k": 3,
    "language": "en"
})

print(response.json())
```

## API Examples

### Example 1: Oily Skin with Acne
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "problem": "acne",
      "budget": "medium",
      "age": "25",
      "gender": "female"
    },
    "top_k": 3,
    "language": "en"
  }'
```

### Example 2: Dry Skin (Arabic Response)
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "dry",
      "problem": "hydration"
    },
    "top_k": 2,
    "language": "ar"
  }'
```

### Example 3: Hair Care
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "hair_type": "curly",
      "problem": "frizz",
      "budget": "medium"
    },
    "top_k": 3,
    "language": "en"
  }'
```

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/stats` | GET | System statistics |
| `/recommend/summary` | POST | **NEW** Summary-based recommendations |
| `/recommend` | POST | Legacy conversation-based |
| `/beauty/products` | GET | All beauty products |
| `/products` | GET | All general products |

## Response Format

```json
{
  "recommendations": [
    {
      "id": "hind-001",
      "name": "Niacinamide Serum 10% + Zinc 1%",
      "price": 2500,
      "currency": "DA",
      "image": "https://example.com/image.jpg",
      "tags": ["oily_skin", "acne", "sebum_control"],
      "description": "Controls sebum production, reduces acne",
      "reason": "Perfect for your oily skin type • Addresses your acne concern",
      "score": 0.95,
      "category": "skin_care",
      "subcategory": "serum"
    }
  ],
  "count": 1,
  "language": "en"
}
```

## Summary Fields Reference

| Field | Type | Example Values |
|-------|------|----------------|
| `skin_type` | string | oily, dry, combination, normal, sensitive |
| `hair_type` | string | oily, dry, curly, straight, wavy |
| `problem` | string | acne, wrinkles, frizz, dryness |
| `category` | string | skin_care, hair_care, makeup |
| `budget` | string | low, medium, high |
| `age` | string/number | 25, "30-40", "40+" |
| `gender` | string | female, male, unisex |
| `language` | string | en, ar, fr |

All fields are **optional**. The API will work with whatever information you provide.

## Troubleshooting

### Beauty recommender not loading
```
⚠️ Beauty products file not found at data/beauty_products.json
```
**Solution**: Make sure `data/beauty_products.json` exists.

### Import errors
```
ImportError: cannot import name 'BeautyRecommender'
```
**Solution**: Make sure `models/beauty_recommender.py` exists.

### FAISS not found
```
ModuleNotFoundError: No module named 'faiss'
```
**Solution**: 
```bash
pip install faiss-cpu
# OR for GPU support
pip install faiss-gpu
```

### Server won't start
```
ERROR: Could not find a version that satisfies the requirement
```
**Solution**: 
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Next Steps

1. ✅ Start the server
2. ✅ Run test script to verify functionality
3. ✅ Integrate with your chat system
4. ✅ Add more products to the catalog
5. ✅ Customize business rules as needed

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
