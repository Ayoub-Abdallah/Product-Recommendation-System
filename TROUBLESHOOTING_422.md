# 🔧 Troubleshooting: 422 Unprocessable Content Error

## What Does 422 Mean?

**422 Unprocessable Content** = Your request body has validation errors.

The request reached the server, but the data format is incorrect.

---

## ✅ Correct Request Examples

### Example 1: Minimal Request (All fields optional)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Example 2: Search by Category
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "category": "health_supplements",
    "top_k": 3
  }'
```

### Example 3: Complex Query
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "category": "health_supplements",
    "medical_conditions": ["diabetes", "anemia"],
    "avoid": ["sugar"],
    "budget": 5000,
    "top_k": 3
  }'
```

### Example 4: Natural Language Query
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need vitamins for diabetes and anemia",
    "top_k": 5
  }'
```

---

## ❌ Common Errors That Cause 422

### Error 1: Missing Content-Type Header
```bash
# WRONG ❌
curl -X POST http://localhost:4708/recommend -d '{"category": "health_supplements"}'

# CORRECT ✅
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"category": "health_supplements"}'
```

### Error 2: Invalid JSON
```bash
# WRONG ❌ (missing quotes)
{"category": health_supplements}

# CORRECT ✅
{"category": "health_supplements"}
```

### Error 3: Invalid top_k Value
```bash
# WRONG ❌ (must be 1-10)
{"top_k": 0}
{"top_k": 15}

# CORRECT ✅
{"top_k": 5}
```

### Error 4: Wrong Data Type
```bash
# WRONG ❌ (needs, medical_conditions should be arrays)
{"needs": "energy"}
{"medical_conditions": "diabetes"}

# CORRECT ✅
{"needs": ["energy"]}
{"medical_conditions": ["diabetes"]}
```

---

## 🧪 Test Your Request

### Step 1: Check Server Health
```bash
curl http://localhost:4708/health
```
Should return: `{"status": "healthy", ...}`

### Step 2: Try Minimal Request
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Step 3: View API Documentation
Open in browser: **http://localhost:4708/docs**

This interactive documentation shows:
- All available fields
- Data types expected
- Example requests
- You can test requests directly!

---

## 📋 Valid Field Types

```typescript
{
  category?: string,                    // Optional
  needs?: string[],                     // Array of strings
  skin_conditions?: string[],           // Array of strings
  medical_conditions?: string[],        // Array of strings
  avoid?: string[],                     // Array of strings
  budget?: number | string,             // Number or "low"/"medium"/"high"
  age?: string,                         // Optional
  preferences?: string[],               // Array of strings
  query?: string,                       // Optional
  top_k?: number,                       // 1-10, default 5
  language?: string                     // "en", "ar", "fr", default "en"
}
```

**ALL fields are optional!** Even an empty `{}` is valid.

---

## 🔍 How to Debug

### 1. Check the Error Details
```bash
curl -v -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"your": "request"}'
```

The `-v` flag shows detailed error messages.

### 2. Use the Interactive Docs
Go to: http://localhost:4708/docs

- Click on POST /recommend
- Click "Try it out"
- Enter your request
- See validation errors immediately

### 3. Test with Python
```python
import requests
import json

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "category": "health_supplements",
        "top_k": 3
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

---

## ✅ Quick Fix Checklist

- [ ] Added `Content-Type: application/json` header?
- [ ] JSON is valid (use jsonlint.com to check)?
- [ ] Arrays are formatted as `["item1", "item2"]` not `"item"`?
- [ ] `top_k` is between 1-10?
- [ ] All field names spelled correctly?
- [ ] Server is running on port 4708?

---

## 💡 Pro Tip

Use the **interactive API docs** at http://localhost:4708/docs

It's the easiest way to:
- See all available fields
- Test requests
- See validation errors
- Get example responses

No need to write curl commands manually!
