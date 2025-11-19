# 🎯 API DOCUMENTATION - Beauty & Health Recommendation System

## Main Endpoint: POST /recommend

**URL:** `http://localhost:4708/recommend`

**Method:** POST

**Content-Type:** application/json

---

## REQUEST BODY - ALL AVAILABLE FIELDS

```json
{
  "summary": {
    // ⚠️ At least ONE field must be provided
    
    "skin_type": "oily" | "dry" | "combination" | "normal" | "sensitive",
    "hair_type": "oily" | "dry" | "normal" | "curly" | "straight" | "wavy",
    "category": "skin_care" | "hair_care" | "makeup" | "supplements" | "wellness",
    "product_type": "serum" | "cream" | "shampoo" | "vitamin" | etc,
    "problem": "acne" | "wrinkles" | "hair_loss" | "frizz" | "dark_spots" | etc,
    "concerns": ["anti_aging", "hydration", "acne"],
    "budget": 2500 OR "low" | "medium" | "high",
    "age": "25" | "30-40" | "40+",
    "gender": "female" | "male" | "unisex"
  },
  "top_k": 5,
  "language": "en" | "ar" | "fr"
}
```

---

## ⚠️ THE FIX - WHAT WAS WRONG

**YOU WERE RIGHT!** The system was showing **Melatonin** for oily skin/hair which is COMPLETELY WRONG!

**The Problem:** Weak filtering - products without skin/hair type restrictions were included

**The Fix:** Added **STRICT filtering**:
- ✅ If you select "oily skin" → ONLY products FOR oily skin
- ✅ If you select "oily hair" → ONLY products FOR oily hair  
- ✅ If you select both → Mix of products matching each type
- ✅ Melatonin, supplements with no skin/hair type → EXCLUDED when you specify skin/hair type

---

## 📝 CORRECT EXAMPLES

### Example 1: Oily Skin Products
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {"skin_type": "oily"},
    "top_k": 3
  }'
```

**Expected Results:**
- Niacinamide Serum 10% + Zinc 1%
- Salicylic Acid 2% Acne Treatment
- Matte Foundation SPF 30
- (NO Melatonin, NO random supplements)

### Example 2: Oily Hair Products
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {"hair_type": "oily"},
    "top_k": 3
  }'
```

**Expected Results:**
- Hair care products for oily hair
- (NO skincare, NO melatonin)

### Example 3: Supplements (Without skin/hair filter)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {"category": "supplements"},
    "top_k": 3
  }'
```

**Expected Results:**
- Biotin, Collagen, Vitamins, etc.

---

## 🔧 TEST THE FIX NOW

```bash
# This should NO LONGER show Melatonin!
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "hair_type": "oily"
    },
    "top_k": 5
  }'
```

---

**Apologies for the terrible recommendations - it's now FIXED!**
