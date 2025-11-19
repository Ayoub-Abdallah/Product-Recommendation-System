# Beauty Recommendation API Documentation

## Overview

The Beauty Recommendation System provides intelligent product recommendations based on structured user summaries. It supports multilingual responses (English, Arabic, French) and uses FAISS vector search combined with business rules for optimal recommendations.

## Features

- **Structured Summary Input**: Accept detailed user profiles including skin type, hair type, problems, budget, etc.
- **Multilingual Support**: Returns responses in English, Arabic, or French
- **Smart Matching**: Uses FAISS vector search + keyword fallback for robust matching
- **Business Rules**: Filters by budget, age range, gender, and other constraints
- **Localized Reasons**: Provides personalized explanations for each recommendation

## API Endpoints

### 1. Summary-Based Recommendation (NEW)

**Endpoint**: `POST /recommend/summary`

**Request Body**:
```json
{
  "summary": {
    "skin_type": "oily | dry | combination | normal | sensitive",
    "hair_type": "oily | dry | normal | curly | straight | wavy",
    "problem": "acne | wrinkles | dark_spots | hair_loss | frizz | dryness | etc",
    "category": "skin_care | hair_care | makeup",
    "product_type": "serum | cream | shampoo | conditioner | mask | etc",
    "budget": "low | medium | high",
    "age": "25 | 30-40 | 40+ | etc",
    "gender": "female | male | unisex",
    "concerns": ["anti_aging", "hydration", "brightening"],
    "language": "en | ar | fr"
  },
  "top_k": 3,
  "language": "en"
}
```

**Response**:
```json
{
  "recommendations": [
    {
      "id": "hind-001",
      "name": "Niacinamide Serum 10% + Zinc 1%",
      "price": 2500,
      "currency": "DA",
      "image": "https://example.com/product.jpg",
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

### 2. Conversation-Based Recommendation (Legacy)

**Endpoint**: `POST /recommend`

**Request Body**:
```json
{
  "conversation": [
    "I need something for my skin",
    "I have oily skin with acne"
  ]
}
```

### 3. Get Beauty Products

**Endpoint**: `GET /beauty/products`

Returns all beauty products in the catalog.

### 4. Get Statistics

**Endpoint**: `GET /stats`

Returns system statistics including product counts, categories, and index information.

### 5. Health Check

**Endpoint**: `GET /health`

Returns service health status.

## Summary Fields

### Required Fields
None - all fields are optional. The system will do its best with whatever information is provided.

### Optional Fields

| Field | Type | Description | Example Values |
|-------|------|-------------|----------------|
| `skin_type` | string | User's skin type | oily, dry, combination, normal, sensitive |
| `hair_type` | string | User's hair type | oily, dry, normal, curly, straight, wavy |
| `problem` | string | Primary concern | acne, wrinkles, dark_spots, hair_loss, frizz |
| `category` | string | Product category | skin_care, hair_care, makeup |
| `product_type` | string | Specific product type | serum, cream, shampoo, mask |
| `budget` | string | Budget constraint | low, medium, high |
| `age` | string/number | User's age | 25, "30-40", "40+" |
| `gender` | string | Gender preference | female, male, unisex |
| `concerns` | array | Additional concerns | ["anti_aging", "hydration"] |
| `language` | string | Preferred language | en, ar, fr |

## Business Rules

### 1. Budget Filtering
- **Low budget**: Excludes high-budget products
- **Medium budget**: Slight penalty for high-budget products
- **High budget**: No restrictions

### 2. Age Range Matching
- Products have target age ranges (e.g., "20-30", "30-40", "40+")
- Age mismatch results in a 30% score penalty
- Soft filter - doesn't exclude products

### 3. Gender Filtering
- "Unisex" products match all genders
- Gender mismatch results in a 20% score penalty
- Soft filter - doesn't exclude products

### 4. Stock Availability
- Out-of-stock products (stock ≤ 0) are always excluded

## Search Algorithm

### 1. Vector Search (Primary)
1. Convert summary to search query text
2. Generate embedding using sentence transformers
3. Perform FAISS similarity search
4. Apply keyword boost based on exact matches
5. Compute composite score

### 2. Keyword Search (Fallback)
1. Match skin/hair types against product attributes
2. Match problems against product tags
3. Match category preferences
4. Score based on exact matches

### 3. Score Composition
```
final_score = (
  similarity * 0.4 +
  popularity * 0.2 +
  stock_level * 0.1 +
  recency * 0.1 +
  personalization * 0.1 +
  seller_boost * 0.1
) * business_rule_penalties
```

## Language Support

### Response Languages
- **English (`en`)**: Default language
- **Arabic (`ar`)**: Full RTL support
- **French (`fr`)**: Complete translations

### Multilingual Fields
Each product includes:
- `name`, `name_ar`, `name_fr`
- `description`, `description_ar`, `description_fr`

### Localized Reasons
Recommendation reasons are generated in the requested language:
- **EN**: "Perfect for your oily skin type • Addresses your acne concern"
- **AR**: "مناسب لنوع بشرتك (oily) • يعالج مشكلة acne"
- **FR**: "Adapté à votre type de peau (oily) • Traite le problème de acne"

## Example Use Cases

### 1. Acne Treatment for Oily Skin
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "problem": "acne",
      "budget": "medium",
      "age": "25"
    },
    "top_k": 3,
    "language": "en"
  }'
```

### 2. Anti-Aging Serum (Arabic Response)
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "dry",
      "problem": "wrinkles",
      "product_type": "serum",
      "age": "40"
    },
    "top_k": 2,
    "language": "ar"
  }'
```

### 3. Hair Care for Curly Hair
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "hair_type": "curly",
      "problem": "frizz",
      "category": "hair_care"
    },
    "top_k": 3,
    "language": "en"
  }'
```

### 4. Minimal Summary (Problem Only)
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "problem": "hydration"
    },
    "top_k": 3,
    "language": "en"
  }'
```

## Testing

### Run the Test Suite
```bash
# Make sure the server is running
uvicorn app:app --reload

# In another terminal, run the test script
python test_summary_api.py
```

### Manual Testing with curl
```bash
# Health check
curl http://localhost:8000/health

# Get all beauty products
curl http://localhost:8000/beauty/products

# Get statistics
curl http://localhost:8000/stats

# Test recommendation
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{"summary": {"skin_type": "oily"}, "top_k": 3}'
```

## Error Handling

### 400 Bad Request
- Missing or invalid summary object
- Invalid `top_k` value (must be 1-5)

### 503 Service Unavailable
- Beauty products catalog not found
- Beauty recommender not initialized

### 500 Internal Server Error
- Error during recommendation generation
- Database or search errors

### Example Error Response
```json
{
  "detail": "Error generating recommendations: Invalid summary format"
}
```

## Performance Optimization

### FAISS Index
- **Small catalogs (<1000 products)**: Uses `IndexFlatIP` for exact search
- **Large catalogs (>1000 products)**: Uses `IndexIVFFlat` for fast approximate search
- Embeddings are L2-normalized for cosine similarity

### Search Strategy
1. Vector search retrieves top 5× candidates (e.g., 15 for top_k=3)
2. Keyword search provides fallback with up to 3× candidates
3. Business rules filter and re-rank results
4. Final top_k results returned

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

### Required Packages
- fastapi
- uvicorn
- pydantic
- sentence-transformers
- faiss-cpu (or faiss-gpu)
- numpy
- requests (for testing)

### Start the Server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Product Catalog Schema

Each product in `data/beauty_products.json` must include:

```json
{
  "id": "unique-id",
  "name": "Product Name",
  "name_ar": "اسم المنتج",
  "name_fr": "Nom du Produit",
  "price": 2500,
  "currency": "DA",
  "category": "skin_care",
  "subcategory": "serum",
  "image": "https://example.com/image.jpg",
  "tags": ["tag1", "tag2"],
  "skin_types": ["oily", "combination"],
  "hair_types": [],
  "problems_solved": ["acne", "oily_skin"],
  "age_range": ["20-30", "30-40"],
  "gender": ["female", "male", "unisex"],
  "budget": "medium",
  "description": "English description",
  "description_ar": "وصف بالعربية",
  "description_fr": "Description en français",
  "ingredients": ["ingredient1", "ingredient2"],
  "stock": 50,
  "popularity": 0.9,
  "recency": 0.8,
  "personal": 0.0,
  "seller_boost": 0.0
}
```

## Integration with Chat System

The chat system should:

1. Collect user information through conversation
2. Build a structured summary object
3. Send POST request to `/recommend/summary`
4. Display returned products with reasons

### Example Integration Flow
```
User: "I have oily skin and acne problems"
Chat System: [Extracts skin_type=oily, problem=acne]

User: "My budget is around 2500 DA"
Chat System: [Adds budget=medium]

Chat System: [Sends summary to API]
API: [Returns 3 products with reasons]
Chat System: [Displays products with images and reasons]
```

## License

MIT License - See LICENSE file for details.
