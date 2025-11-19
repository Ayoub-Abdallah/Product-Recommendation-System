# 🎯 Intelligent Multi-Category Recommendation System

## 🌟 Overview

Transformed recommendation system that handles **complex user situations** across multiple product categories with intelligent medical and skin condition filtering.

**Version:** 3.0  
**Port:** 4708  
**Categories Supported:** 6+

---

## 📦 Product Categories

1. **Beauty & Skincare** (`beauty_skincare`)
   - Serums, Moisturizers, Cleansers, Treatments
   
2. **Health Supplements** (`health_supplements`)
   - Multivitamins, Vitamins, Beauty Supplements
   
3. **Sportswear** (`sportswear`)
   - Footwear, Activewear, Athletic gear
   
4. **Baby Care** (`baby_care`)
   - Skincare, Diaper care, Baby essentials
   
5. **Maternal Health** (`maternal_health`)
   - Prenatal vitamins, Nursing essentials
   
6. **Healthcare Devices** (`healthcare_devices`)
   - Monitoring devices, Diabetic supplies

---

## 🧠 Intelligence Features

### 1. Medical Safety Filtering
- ✅ Identifies safe products for medical conditions
- ❌ Excludes products with contraindications
- ⚕️ Flags products needing doctor consultation

**Example:** User with diabetes → Filters out high-sugar products

### 2. Skin Compatibility
- Matches products to skin types (dry, sensitive, oily, eczema-prone)
- Avoids incompatible formulations
- Supports complex combinations (dry + sensitive)

**Example:** Dry + Sensitive skin → Only fragrance-free, hypoallergenic products

### 3. Ingredient Avoidance
- Filters by what user wants to avoid (sugar, fragrance, allergens)
- Checks nutritional content for supplements
- Validates certifications

**Example:** Avoid sugar → Only sugar-free or low-sugar products

### 4. Smart Scoring
- Boosts products beneficial for user's conditions
- Prioritizes exact matches
- Considers stock availability

---

## 🔥 Complex Scenarios Handled

### Scenario 1: Diabetic with Anemia
```json
{
  "category": "health_supplements",
  "medical_conditions": ["diabetes", "anemia"],
  "needs": ["energy", "immunity"],
  "avoid": ["sugar"],
  "budget": 5000,
  "top_k": 3
}
```

**System Response:**
- ✅ Recommends: Sugar-Free Multivitamin for Diabetics (contains iron)
- ✅ Recommends: Iron + Vitamin C Supplement (low sugar)
- ❌ Filters out: Regular multivitamins with sugar
- ⚕️ Warnings: "Consult doctor if on blood thinners"

### Scenario 2: Dry + Sensitive Skin
```json
{
  "category": "beauty_skincare",
  "skin_conditions": ["dry", "sensitive"],
  "avoid": ["fragrance"],
  "preferences": ["hypoallergenic"],
  "budget": "medium"
}
```

**System Response:**
- ✅ Recommends: Fragrance-Free Moisturizer for Dry Sensitive Skin
- ❌ Filters out: Products with fragrance
- ❌ Filters out: Products for oily skin

### Scenario 3: Baby with Eczema
```json
{
  "category": "baby_care",
  "skin_conditions": ["eczema_prone", "sensitive"],
  "age": "newborn",
  "preferences": ["organic", "fragrance_free"]
}
```

**System Response:**
- ✅ Recommends: Organic Baby Lotion - Fragrance Free
- ✅ Certified: Hypoallergenic, Dermatologist-tested
- ✅ Safe for: Eczema, newborns

### Scenario 4: Diabetic Needing Athletic Shoes
```json
{
  "category": "sportswear",
  "medical_conditions": ["diabetes"],
  "needs": ["comfort", "support"]
}
```

**System Response:**
- ✅ Recommends: Wide-Fit Running Shoes (diabetic-friendly)
- ✅ Features: Extra cushioning, seamless interior
- ✅ Benefits: Prevents blisters, supports diabetic feet

### Scenario 5: Pregnant with Gestational Diabetes
```json
{
  "category": "maternal_health",
  "medical_conditions": ["pregnancy", "gestational_diabetes"],
  "avoid": ["sugar"]
}
```

**System Response:**
- ✅ Recommends: Prenatal DHA + Folic Acid (Sugar-Free)
- ✅ Safe for: Pregnancy, gestational diabetes
- ✅ Contains: Essential prenatal nutrients, zero sugar

---

## 🎯 API Endpoint

### POST /recommend

**Base URL:** `http://localhost:4708/recommend`

**Request Fields:**

```typescript
{
  category?: string,              // "beauty_skincare", "health_supplements", etc.
  needs?: string[],               // ["energy", "immunity", "hydration"]
  skin_conditions?: string[],     // ["dry", "sensitive", "eczema_prone"]
  medical_conditions?: string[],  // ["diabetes", "anemia", "pregnancy"]
  avoid?: string[],               // ["sugar", "fragrance", "allergens"]
  budget?: number | string,       // 5000 or "medium"
  age?: string,                   // "newborn", "25", "40+"
  preferences?: string[],         // ["organic", "hypoallergenic"]
  query?: string,                 // Natural language
  top_k?: number,                 // 1-10, default 5
  language?: string               // "en", "ar", "fr"
}
```

**Response:**

```json
{
  "recommendations": [
    {
      "id": "supp-001",
      "name": "Sugar-Free Multivitamin for Diabetics",
      "price": 3500,
      "currency": "DA",
      "category": "health_supplements",
      "subcategory": "multivitamins",
      "tags": ["sugar_free", "diabetic_friendly"],
      "description": "Complete multivitamin...",
      "reason": "✅ Safe for diabetes, anemia • 💊 Beneficial for anemia",
      "score": 1.245,
      "stock": 80,
      "safety_notes": ["⚕️ Consult doctor if on blood thinners"]
    }
  ],
  "count": 3,
  "metadata": {
    "warnings": [
      {
        "type": "medical_consultation",
        "severity": "medium",
        "product": "Product Name",
        "message": "⚕️ Consult doctor: kidney_disease"
      }
    ],
    "constraints_applied": ["medical_safety", "ingredient_avoidance"],
    "filtered_out": {
      "medical_safety": 2,
      "skin_incompatibility": 0,
      "budget": 1
    }
  },
  "language": "en"
}
```

---

## 📋 Examples

### Example 1: cURL
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "category": "health_supplements",
    "medical_conditions": ["diabetes", "anemia"],
    "avoid": ["sugar"],
    "top_k": 3
  }'
```

### Example 2: Python
```python
import requests

response = requests.post("http://localhost:4708/recommend", json={
    "category": "health_supplements",
    "medical_conditions": ["diabetes", "anemia"],
    "needs": ["energy"],
    "avoid": ["sugar"],
    "top_k": 3
})

print(response.json())
```

### Example 3: Natural Language
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I have diabetes and anemia, need vitamins without sugar",
    "top_k": 5
  }'
```

---

## 🧪 Testing

Run comprehensive tests:

```bash
./venv/bin/python test_intelligent_system.py
```

Tests cover:
- ✅ Diabetic with anemia
- ✅ Dry + sensitive skin
- ✅ Baby with eczema
- ✅ Diabetic needing athletic shoes
- ✅ Pregnant with gestational diabetes
- ✅ Natural language queries

---

## 📊 System Stats

```bash
curl http://localhost:4708/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Intelligent Multi-Category Recommendation System",
  "version": "3.0",
  "products_loaded": 12,
  "categories": 6,
  "categories_list": [
    "beauty_skincare",
    "health_supplements",
    "sportswear",
    "baby_care",
    "healthcare_devices",
    "maternal_health"
  ]
}
```

---

## 🔍 Key Improvements Over v2.0

### Before (v2.0):
- ❌ Limited to beauty & skincare only
- ❌ Basic filtering (skin type only)
- ❌ No medical safety checks
- ❌ Simple scenarios only

### After (v3.0):
- ✅ 6+ product categories
- ✅ Intelligent medical safety filtering
- ✅ Complex constraint handling
- ✅ Skin + Medical + Nutritional filtering
- ✅ Safety warnings & doctor consultation alerts
- ✅ Natural language support
- ✅ Multi-language (EN, AR, FR)

---

## 🎓 How It Works

1. **Parse Request** → Extract constraints from user input
2. **Vector Search** → Find relevant products using FAISS
3. **Medical Safety Check** → Filter unsafe products
4. **Skin Compatibility** → Match skin conditions
5. **Ingredient Avoidance** → Remove unwanted ingredients
6. **Budget Filtering** → Match price range
7. **Smart Scoring** → Boost beneficial products
8. **Safety Warnings** → Generate consultation alerts
9. **Format Response** → Return recommendations + metadata

---

## 🚀 Quick Start

### 1. Start Server
```bash
./venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 4708
```

### 2. Test Health
```bash
curl http://localhost:4708/health
```

### 3. Get Recommendations
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "vitamins for diabetes and anemia", "top_k": 3}'
```

### 4. View API Docs
```
http://localhost:4708/docs
```

---

## 📚 Files

- `app.py` - Main FastAPI application
- `models/intelligent_recommender.py` - Core recommendation engine
- `data/products_catalog.json` - Multi-category product catalog (12 products)
- `test_intelligent_system.py` - Comprehensive test suite

---

## 🔜 Future Enhancements

- [ ] Expand catalog to 100+ products per category
- [ ] Add drug interaction checking
- [ ] Include allergy cross-reference database
- [ ] Support for multiple languages in product data
- [ ] Real-time stock updates
- [ ] User profile history
- [ ] Personalized recommendations based on past purchases

---

## ✅ Status

**System:** ✅ Operational  
**Port:** 4708  
**Products:** 12 (sample catalog)  
**Categories:** 6  
**FAISS Index:** IndexFlatIP  
**Test Coverage:** 6 complex scenarios  

**Ready for production with expanded catalog!** 🚀
