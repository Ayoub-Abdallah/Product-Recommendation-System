# 📘 HOW TO SEND VALID API REQUESTS

## 🚀 Quick Start

### Method 1: Using Python (RECOMMENDED)

```python
import requests

# Simple request
response = requests.post(
    "http://localhost:4708/recommend",
    json={"category": "health_supplements", "top_k": 3}
)

print(response.json())
```

**Run the working examples:**
```bash
./venv/bin/python api_examples.py
```

---

### Method 2: Using cURL

```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"category": "health_supplements", "top_k": 3}'
```

**Important for cURL:**
- ✅ Must include `-H "Content-Type: application/json"`
- ✅ Use single quotes around JSON: `'{"key": "value"}'`
- ✅ Escape quotes if using double quotes: `"{\"key\": \"value\"}"`

---

### Method 3: Using Postman/Insomnia

1. **Method:** POST
2. **URL:** `http://localhost:4708/recommend`
3. **Headers:** `Content-Type: application/json`
4. **Body (raw JSON):**
```json
{
  "category": "health_supplements",
  "top_k": 3
}
```

---

### Method 4: Interactive API Docs (EASIEST!)

Open in browser: **http://localhost:4708/docs**

1. Click on **POST /recommend**
2. Click **"Try it out"**
3. Edit the request body
4. Click **"Execute"**
5. See the response immediately!

---

## ✅ Valid Request Examples

### Example 1: Empty Request (All Optional!)
```python
import requests
response = requests.post("http://localhost:4708/recommend", json={})
```

```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

### Example 2: Simple Category Search
```python
requests.post("http://localhost:4708/recommend", json={
    "category": "health_supplements",
    "top_k": 3
})
```

```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "category": "health_supplements",
    "top_k": 3
  }'
```

---

### Example 3: Complex Medical Query
```python
requests.post("http://localhost:4708/recommend", json={
    "category": "health_supplements",
    "medical_conditions": ["diabetes", "anemia"],
    "avoid": ["sugar"],
    "budget": 5000,
    "top_k": 3
})
```

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

---

### Example 4: Natural Language Query
```python
requests.post("http://localhost:4708/recommend", json={
    "query": "I need vitamins for diabetes and anemia",
    "top_k": 5
})
```

```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need vitamins for diabetes and anemia",
    "top_k": 5
  }'
```

---

### Example 5: Get Product by ID
```python
response = requests.get("http://localhost:4708/product/supp-001")
```

```bash
curl http://localhost:4708/product/supp-001
```

---

### Example 6: Search Products
```python
response = requests.get("http://localhost:4708/product/search/vitamin")
```

```bash
curl http://localhost:4708/product/search/vitamin
```

---

## 📋 Available Fields (ALL OPTIONAL)

```python
{
    "category": "health_supplements",           # Product category
    "needs": ["energy", "immunity"],            # User needs
    "skin_conditions": ["dry", "sensitive"],    # Skin types
    "medical_conditions": ["diabetes"],         # Medical constraints
    "avoid": ["sugar", "fragrance"],            # Things to avoid
    "budget": 5000,                            # Max price or "low"/"medium"/"high"
    "age": "newborn",                          # Age group
    "preferences": ["organic"],                 # Must-have features
    "query": "natural language query",          # Free-form text
    "top_k": 3,                                # Number of results (1-10)
    "language": "en"                           # Response language (en/ar/fr)
}
```

---

## ❌ Common Mistakes

### Mistake 1: Missing Content-Type
```bash
# WRONG ❌
curl -X POST http://localhost:4708/recommend -d '{"category": "health"}'

# CORRECT ✅
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"category": "health_supplements"}'
```

### Mistake 2: String Instead of Array
```python
# WRONG ❌
{"needs": "energy"}

# CORRECT ✅
{"needs": ["energy"]}
```

### Mistake 3: Invalid top_k
```python
# WRONG ❌
{"top_k": 0}      # Must be >= 1
{"top_k": 15}     # Must be <= 10

# CORRECT ✅
{"top_k": 5}
```

---

## 🧪 Test Your Setup

### Quick Test:
```bash
# Test 1: Server health
curl http://localhost:4708/health

# Test 2: Simple request
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{}'

# Test 3: Get product
curl http://localhost:4708/product/supp-001
```

### Run All Examples:
```bash
./venv/bin/python api_examples.py
```

---

## 📚 Resources

- **Interactive Docs:** http://localhost:4708/docs (Try requests live!)
- **Example Code:** `api_examples.py` (Working Python examples)
- **Troubleshooting:** `TROUBLESHOOTING_422.md`
- **Product IDs:** Check `data/products_catalog.json`

---

## 💡 Pro Tips

1. **Use the interactive docs** (http://localhost:4708/docs) - It's the easiest way!
2. **Use Python's requests library** - Simpler than cURL
3. **All fields are optional** - Even `{}` is a valid request
4. **Arrays must be arrays** - Use `["item"]` not `"item"`
5. **Check examples** - Run `api_examples.py` to see working code

---

## ✅ Summary

**Python (BEST):**
```python
import requests
response = requests.post("http://localhost:4708/recommend", 
    json={"category": "health_supplements", "top_k": 3})
print(response.json())
```

**cURL:**
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{"category": "health_supplements", "top_k": 3}'
```

**Browser:**
Open: http://localhost:4708/docs and click "Try it out"

**That's it!** 🚀
