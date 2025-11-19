# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd "/home/ayoub/hind_smart_agent_system/system/recommendation system"

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
# Option 1: Using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 5000

# Option 2: Using the Python script
python app.py
```

You should see:
```
📊 FAISS index: IndexFlatIP, 24 vectors
✅ Loaded 24 beauty products with FAISS index
✅ Beauty & Health recommender loaded with 24 products
INFO:     Uvicorn running on http://0.0.0.0:5000
```

### Step 3: Test the System

#### Option A: Web Interface (Easiest)
Open your browser and go to:
```
http://localhost:4708
```

Fill out the form with your preferences and click "Get Personalized Recommendations"

#### Option B: API Testing (Terminal)
```bash
# Test skincare recommendations
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "problem": "acne",
      "budget": 2500
    },
    "top_k": 3,
    "language": "en"
  }'

# Test supplements
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "problem": "hair loss",
      "category": "supplements"
    },
    "top_k": 3,
    "language": "en"
  }'
```

#### Option C: Python Test Script
```bash
source venv/bin/activate
python test_full_catalog.py
```

## 📱 Quick API Reference

### Main Endpoint: POST /recommend

**Request:**
```json
{
  "summary": {
    "skin_type": "oily|dry|combination|normal|sensitive",
    "hair_type": "oily|dry|normal|curly|straight|wavy",
    "category": "skin_care|hair_care|makeup|supplements|wellness",
    "problem": "any concern like acne, wrinkles, hair loss, etc",
    "budget": 2500 or "low|medium|high",
    "age": "25" or "30-40",
    "gender": "female|male|unisex"
  },
  "top_k": 5,
  "language": "en|ar|fr"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "name": "Product Name",
      "price": 2500,
      "currency": "DA",
      "category": "skin_care",
      "subcategory": "serum",
      "description": "...",
      "reason": "Why this product matches",
      "score": 1.189
    }
  ],
  "count": 1
}
```

### Other Endpoints

```bash
# Get all products
curl http://localhost:4708/products

# Get categories
curl http://localhost:4708/categories

# Health check
curl http://localhost:4708/health

# Get stats
curl http://localhost:4708/stats
```

## 🎯 Common Use Cases

### Use Case 1: Oily Acne-Prone Skin
```json
{
  "summary": {
    "skin_type": "oily",
    "problem": "acne",
    "budget": 2500
  },
  "top_k": 3,
  "language": "en"
}
```

**Expected Results:**
- Salicylic Acid 2% Acne Treatment
- Niacinamide Serum 10% + Zinc 1%
- Azelaic Acid 10% Suspension

### Use Case 2: Anti-Aging Routine
```json
{
  "summary": {
    "problem": "wrinkles",
    "age": "40+",
    "budget": "high"
  },
  "top_k": 5,
  "language": "en"
}
```

**Expected Results:**
- Retinol Night Cream 0.5%
- Collagen Peptides Powder
- Vitamin C Brightening Serum 15%
- Hyaluronic Acid Hydrating Serum

### Use Case 3: Hair Growth & Strength
```json
{
  "summary": {
    "problem": "hair loss",
    "category": "supplements"
  },
  "top_k": 3,
  "language": "en"
}
```

**Expected Results:**
- Biotin 10000 mcg Hair, Skin & Nails
- Collagen Peptides Powder

### Use Case 4: Low Budget Shopping
```json
{
  "summary": {
    "budget": 2000
  },
  "top_k": 5,
  "language": "en"
}
```

**Expected Results:**
- Vitamin D3 5000 IU (1800 DA)
- Glycolic Acid 7% Toning Solution (1900 DA)
- Gentle Foaming Cleanser (1800 DA)
- Melatonin 5mg Sleep Support (1500 DA)
- Biotin & Collagen Shampoo (1600 DA)

## 🐛 Troubleshooting

### Server won't start
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check if port is already in use
lsof -ti:5000
# If yes, kill it:
kill -9 $(lsof -ti:5000)
```

### No recommendations returned
- Check that at least one field in summary is filled
- Try broadening your criteria (remove some filters)
- Check budget is not too restrictive
- Try with just `{"summary": {}, "top_k": 5}`

### Price not showing
- Refresh the page (Ctrl+F5)
- Check browser console for errors
- Verify server is running the latest code

## 📊 System Info

- **Products**: 24 curated beauty & health products
- **Categories**: 5 (skincare, haircare, makeup, supplements, wellness)
- **Languages**: 3 (English, Arabic, French)
- **Price Range**: 1500 - 4200 DA
- **Tech Stack**: FastAPI, FAISS, Sentence Transformers

## 📚 Documentation

- **README.md** - Complete system documentation
- **SYSTEM_TRANSFORMATION.md** - Migration and changes guide
- **NUMERIC_BUDGET_GUIDE.md** - Budget feature documentation
- **test_full_catalog.py** - Comprehensive test examples

## ✨ Pro Tips

1. **Best Results**: Provide at least 2-3 criteria (e.g., skin_type + problem + budget)
2. **Budget**: Use numeric budgets for exact filtering, categorical for ranges
3. **Language**: Product names and reasons are translated in ar/fr
4. **Categories**: Use category filter to narrow down product type
5. **Top K**: Start with 3-5 results, increase if needed

## 🎉 You're Ready!

The system is now fully operational. Visit http://localhost:4708 to start getting personalized beauty and health product recommendations!

---

Need help? Check the full README.md for detailed documentation.
