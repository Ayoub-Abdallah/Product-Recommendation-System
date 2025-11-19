# 🎯 Budget Warnings & Metadata Feature

## Overview

The recommendation API now returns **metadata** with every response, including:
- **Warnings** when budget is too low or filters are too strict
- **Budget information** showing price statistics
- **Search information** about candidates and filtering

## Response Format

```json
{
  "recommendations": [...],
  "count": 3,
  "language": "en",
  "metadata": {
    "warnings": [
      {
        "type": "budget",
        "severity": "high",
        "message": "No products found within budget of 500 DA. Showing closest alternatives.",
        "suggestion": "Consider increasing budget to at least 1500 DA"
      }
    ],
    "budget_info": {
      "requested_budget": 500,
      "cheapest_available": 1500,
      "most_expensive": 4200,
      "average_price": 2593.33,
      "products_in_budget": 0,
      "products_over_budget": 15,
      "budget_type": "numeric"
    },
    "search_info": {
      "total_candidates": 15,
      "after_filtering": 15
    }
  }
}
```

## Metadata Fields

### `warnings` Array
Contains warning objects with:
- **`type`**: Type of warning (`budget`, `filtering`)
- **`severity`**: `high`, `medium`, or `low`
- **`message`**: Human-readable warning message
- **`suggestion`**: Actionable suggestion to improve results

### `budget_info` Object
- **`requested_budget`**: The budget user specified
- **`cheapest_available`**: Price of cheapest matching product
- **`most_expensive`**: Price of most expensive matching product
- **`average_price`**: Average price of all candidates
- **`products_in_budget`**: Number of products within budget
- **`products_over_budget`**: Number of products exceeding budget
- **`budget_type`**: `numeric` or `categorical`

### `search_info` Object
- **`total_candidates`**: Total products considered
- **`after_filtering`**: Products remaining after filters

## Warning Types

### 1. Budget Too Low (HIGH Severity)
**Trigger:** No products found within specified budget

**Example:**
```json
{
  "type": "budget",
  "severity": "high",
  "message": "No products found within budget of 500 DA. Showing closest alternatives.",
  "suggestion": "Consider increasing budget to at least 1500 DA"
}
```

**What happens:** System still returns recommendations but warns they're over budget

### 2. Some Products Over Budget (MEDIUM Severity)
**Trigger:** Some products exceeded budget by >50%

**Example:**
```json
{
  "type": "budget",
  "severity": "medium",
  "message": "5 products were too far over budget (>50% more).",
  "suggestion": "Cheapest available product: 1800 DA"
}
```

### 3. Too Few Results (MEDIUM Severity)
**Trigger:** Very few products match strict criteria

**Example:**
```json
{
  "type": "filtering",
  "severity": "medium",
  "message": "Only 1 products match your criteria. Consider relaxing some filters.",
  "suggestion": "Try removing skin_type, hair_type, or category filters for more results"
}
```

## Examples

### Example 1: Budget 500 DA (Too Low)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {"budget": 500},
    "top_k": 3
  }'
```

**Result:**
- ✅ Returns recommendations (cheapest available)
- ⚠️  Warning: Budget too low
- 💡 Suggestion: Increase to at least 1500 DA
- 📊 Shows: 0 products in budget, 15 over budget

### Example 2: Budget 2500 DA (Good)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {"budget": 2500},
    "top_k": 3
  }'
```

**Result:**
- ✅ Returns recommendations
- ✅ Many products in budget
- 📊 Shows: 8 products in budget, 7 over budget

### Example 3: Very Strict Filters
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "category": "makeup",
      "budget": 2000
    },
    "top_k": 5
  }'
```

**Result:**
- ✅ Returns 1 recommendation
- ⚠️  Warning: Only 1 product matches
- 💡 Suggestion: Relax some filters

## Using Metadata in Your App

### JavaScript Example
```javascript
const response = await fetch('http://localhost:4708/recommend', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    summary: {budget: 500},
    top_k: 3
  })
});

const data = await response.json();

// Display recommendations
data.recommendations.forEach(rec => {
  console.log(rec.name, rec.price);
});

// Show warnings
if (data.metadata.warnings.length > 0) {
  data.metadata.warnings.forEach(warning => {
    if (warning.severity === 'high') {
      alert(warning.message + '\n\n' + warning.suggestion);
    } else {
      console.warn(warning.message);
    }
  });
}

// Display budget info
const budget = data.metadata.budget_info;
console.log(`Budget: ${budget.requested_budget} DA`);
console.log(`Products in budget: ${budget.products_in_budget}`);
console.log(`Cheapest: ${budget.cheapest_available} DA`);
```

### Python Example
```python
import requests

response = requests.post('http://localhost:4708/recommend', json={
    'summary': {'budget': 500},
    'top_k': 3
})

data = response.json()

# Show recommendations
for rec in data['recommendations']:
    print(f"{rec['name']}: {rec['price']} DA")

# Show warnings
for warning in data['metadata']['warnings']:
    if warning['severity'] == 'high':
        print(f"⚠️  {warning['message']}")
        print(f"💡 {warning['suggestion']}")

# Budget info
budget_info = data['metadata']['budget_info']
print(f"\nBudget Analysis:")
print(f"  Requested: {budget_info['requested_budget']} DA")
print(f"  In Budget: {budget_info['products_in_budget']} products")
print(f"  Cheapest Available: {budget_info['cheapest_available']} DA")
```

## Benefits

1. **Better UX**: Users know why they got certain results
2. **Transparency**: Clear information about budget constraints
3. **Actionable**: Suggestions help users adjust their search
4. **Still Works**: System never fails, always returns something with context
5. **Data-Driven**: Apps can make intelligent UI decisions based on metadata

## UI Recommendations

### Show Budget Warning
```html
<!-- High severity - show modal or prominent alert -->
<div class="alert alert-warning">
  ⚠️ No products within your budget of 500 DA
  <br>💡 Consider increasing to at least 1500 DA
</div>

<!-- Medium severity - show inline -->
<div class="info-box">
  ℹ️ Some products are slightly over budget
</div>
```

### Budget Slider with Info
```html
<input type="range" min="1500" max="5000" value="2500">
<p>Budget: 2500 DA</p>
<small>
  ✅ 8 products available | 💰 Cheapest: 1500 DA
</small>
```

### Filter Warning
```html
<div class="filters-warning">
  ⚠️ Only 1 product matches. Try removing some filters.
</div>
```

---

**Feature Added:** November 18, 2025  
**Status:** ✅ Working and tested
