# Numeric Budget Support - Feature Documentation

## Overview

The Beauty Recommendation API now supports **intelligent numeric budget handling** in addition to categorical budgets (low/medium/high). This allows for more precise and flexible budget-based recommendations.

---

## Budget Input Formats

### 1. Numeric Budget (NEW)

You can now specify exact budget amounts:

```json
{
  "summary": {
    "skin_type": "oily",
    "problem": "acne",
    "budget": 2500
  }
}
```

### 2. String with Numeric Value (NEW)

Natural language budget expressions:

```json
{
  "summary": {
    "budget": "2500 DA"
  }
}
```

```json
{
  "summary": {
    "budget": "around 3000"
  }
}
```

```json
{
  "summary": {
    "budget": "less than 2000 DA"
  }
}
```

### 3. Categorical Budget (Original)

Still supported for flexibility:

```json
{
  "summary": {
    "budget": "low"     // < 3000 DA
  }
}
```

```json
{
  "summary": {
    "budget": "medium"  // 3000-5000 DA
  }
}
```

```json
{
  "summary": {
    "budget": "high"    // > 5000 DA
  }
}
```

---

## How Numeric Budget Works

### Price Ratio Calculation

The system calculates a **price ratio** for each product:

```
price_ratio = product_price / budget
```

### Filtering & Scoring Rules

| Price Ratio | Behavior | Score Multiplier | Example (Budget: 2500 DA) |
|-------------|----------|------------------|---------------------------|
| > 1.5 | ❌ **Excluded** | 0 (filtered) | Products > 3750 DA |
| 1.2 - 1.5 | ⚠️ Heavy penalty | ×0.6 | Products 3000-3750 DA |
| 1.0 - 1.2 | ⚠️ Medium penalty | ×0.8 | Products 2500-3000 DA |
| 0.8 - 1.0 | ✅ **Within budget** | ×1.1 boost | Products 2000-2500 DA |
| 0.5 - 0.8 | ✅ Good value | ×1.05 boost | Products 1250-2000 DA |
| < 0.5 | ✅ Very affordable | No change | Products < 1250 DA |

### Examples

#### Example 1: Budget = 2500 DA

| Product | Price | Ratio | Result |
|---------|-------|-------|--------|
| Product A | 2400 DA | 0.96 | ✅ Included with boost (within budget) |
| Product B | 2700 DA | 1.08 | ✅ Included with penalty (slightly over) |
| Product C | 3200 DA | 1.28 | ✅ Included with heavy penalty |
| Product D | 4000 DA | 1.60 | ❌ Excluded (too expensive) |

#### Example 2: Budget = 1500 DA

| Product | Price | Ratio | Result |
|---------|-------|-------|--------|
| Product A | 1400 DA | 0.93 | ✅ Included with boost |
| Product B | 1800 DA | 1.20 | ✅ Included with penalty |
| Product C | 2500 DA | 1.67 | ❌ Excluded |

---

## Categorical Budget Mapping

When using categorical budgets, the system applies these rules:

### Low Budget
- **Hard Limit**: 3000 DA
- **Excludes**: Products marked as "high" budget
- **Penalties**: 30% penalty for "medium" budget products

### Medium Budget
- **Soft Limit**: 5000 DA (50% penalty above this)
- **Penalties**: 20% penalty for "high" budget products

### High Budget
- **No Limits**: All products considered
- **Boost**: 10% boost for "high" budget products

---

## Reason Generation

The system now includes budget information in recommendation reasons:

### Within Budget
```json
{
  "reason": "Perfect for your oily skin type • Within your budget (2400 DA)"
}
```

### Arabic
```json
{
  "reason": "مناسب لنوع بشرتك (oily) • ضمن ميزانيتك (2400 DA)"
}
```

### French
```json
{
  "reason": "Adapté à votre type de peau (oily) • Dans votre budget (2400 DA)"
}
```

### Close to Budget
```json
{
  "reason": "Addresses your acne concern • Close to your budget (2700 DA)"
}
```

---

## API Examples

### Example 1: Exact Budget
```bash
curl -X POST http://localhost:8000/recommend/summary \
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
```

### Example 2: Budget with Currency
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "hair_type": "dry",
      "problem": "frizz",
      "budget": "3000 DA"
    },
    "top_k": 3,
    "language": "en"
  }'
```

### Example 3: Natural Language Budget
```bash
curl -X POST http://localhost:8000/recommend/summary \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "problem": "hydration",
      "budget": "around 2800"
    },
    "top_k": 3,
    "language": "ar"
  }'
```

---

## Python Integration Examples

### Basic Usage
```python
import requests

response = requests.post('http://localhost:8000/recommend/summary', json={
    "summary": {
        "skin_type": "oily",
        "problem": "acne",
        "budget": 2500  # Numeric budget
    },
    "top_k": 3,
    "language": "en"
})

recommendations = response.json()['recommendations']
for product in recommendations:
    print(f"{product['name']} - {product['price']} DA")
    print(f"Reason: {product['reason']}\n")
```

### Dynamic Budget from User Input
```python
def get_recommendations_with_budget(user_budget):
    """Get recommendations based on user's budget"""
    
    # Parse user input
    budget_value = None
    
    if isinstance(user_budget, (int, float)):
        budget_value = user_budget
    elif isinstance(user_budget, str):
        # Extract numeric value from string
        import re
        match = re.search(r'(\d+)', user_budget)
        if match:
            budget_value = int(match.group(1))
    
    # Call API
    response = requests.post('http://localhost:8000/recommend/summary', json={
        "summary": {
            "budget": budget_value,
            "skin_type": "oily",
            "problem": "acne"
        },
        "top_k": 3
    })
    
    return response.json()

# Examples
recommendations = get_recommendations_with_budget(2500)
recommendations = get_recommendations_with_budget("3000 DA")
recommendations = get_recommendations_with_budget("around 2800")
```

### Budget Range Query
```python
def find_products_in_range(min_price, max_price):
    """Find products within a price range"""
    
    # Use the average as budget
    avg_budget = (min_price + max_price) / 2
    
    response = requests.post('http://localhost:8000/recommend/summary', json={
        "summary": {
            "budget": avg_budget
        },
        "top_k": 5
    })
    
    # Filter results to exact range
    recommendations = response.json()['recommendations']
    filtered = [
        p for p in recommendations 
        if min_price <= p['price'] <= max_price
    ]
    
    return filtered

# Find products between 2000 and 3000 DA
products = find_products_in_range(2000, 3000)
```

---

## Chat System Integration

### Extract Budget from Conversation

```python
import re

def extract_budget_from_message(message):
    """Extract budget from user message"""
    
    # Patterns to match
    patterns = [
        r'(\d+)\s*(?:DA|dinar|dinars)',
        r'around\s+(\d+)',
        r'about\s+(\d+)',
        r'budget\s+(?:is\s+)?(\d+)',
        r'(\d+)\s+(?:DA|dinars?)\s+budget',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            return int(match.group(1))
    
    # Check for categorical budget
    message_lower = message.lower()
    if any(word in message_lower for word in ['cheap', 'affordable', 'low budget']):
        return 'low'
    elif any(word in message_lower for word in ['expensive', 'premium', 'luxury']):
        return 'high'
    elif any(word in message_lower for word in ['medium', 'moderate', 'average']):
        return 'medium'
    
    return None

# Examples
extract_budget_from_message("My budget is 2500 DA")  # → 2500
extract_budget_from_message("I have around 3000 dinars")  # → 3000
extract_budget_from_message("Looking for something cheap")  # → 'low'
```

### Complete Chat Integration

```python
class BeautyConsultantBot:
    def __init__(self):
        self.summary = {}
    
    def process_message(self, message):
        # Extract budget
        budget = self.extract_budget_from_message(message)
        if budget:
            self.summary['budget'] = budget
        
        # Extract other info (skin type, problem, etc.)
        # ...
        
        # Get recommendations if we have enough info
        if len(self.summary) >= 2:
            return self.get_recommendations()
    
    def extract_budget_from_message(self, message):
        # Use the function above
        pass
    
    def get_recommendations(self):
        response = requests.post(
            'http://localhost:8000/recommend/summary',
            json={"summary": self.summary, "top_k": 3}
        )
        return response.json()

# Usage
bot = BeautyConsultantBot()
bot.process_message("I have oily skin")
bot.process_message("I struggle with acne")
recommendations = bot.process_message("My budget is 2500 DA")
```

---

## Testing

### Run the Test Suite
```bash
python test_numeric_budget.py
```

### Test Scenarios Included
1. ✅ Exact numeric budget (2500)
2. ✅ Budget with currency ("3000 DA")
3. ✅ Low budget (1500)
4. ✅ High budget (5000)
5. ✅ Budget range ("around 2800 DA")
6. ✅ Categorical budgets (low/medium/high)
7. ✅ Budget comparison tests
8. ✅ Multilingual responses with budget

---

## Benefits

### 1. More Precise Matching
- Products matched to exact budget amounts
- No need to guess category boundaries

### 2. Better User Experience
- Users can specify exact budget: "2500 DA"
- Natural language: "around 3000"
- Still works with categories: "low budget"

### 3. Smarter Recommendations
- Products slightly over budget included with penalties
- Products within budget get a boost
- Flexible filtering based on price ratio

### 4. Transparent Reasons
- Users see exactly how products fit their budget
- Clear price information in recommendations

---

## Best Practices

### 1. Always Include Budget When Possible
```python
# Good
summary = {"skin_type": "oily", "budget": 2500}

# Also good
summary = {"skin_type": "oily", "budget": "2500 DA"}

# Still works
summary = {"skin_type": "oily", "budget": "medium"}
```

### 2. Handle User Input Flexibly
```python
def parse_user_budget(user_input):
    """Handle various budget formats"""
    if isinstance(user_input, (int, float)):
        return user_input
    
    # Extract number from string
    import re
    match = re.search(r'(\d+)', str(user_input))
    if match:
        return int(match.group(1))
    
    # Fall back to categorical
    return user_input.lower()
```

### 3. Validate Budget Values
```python
def validate_budget(budget):
    """Ensure budget is reasonable"""
    if isinstance(budget, (int, float)):
        if budget < 500:
            return 500  # Minimum
        if budget > 50000:
            return 50000  # Maximum
    return budget
```

---

## Migration Guide

### From Categorical to Numeric

**Before:**
```python
summary = {"budget": "medium"}
```

**After:**
```python
# Option 1: Use exact amount
summary = {"budget": 3000}

# Option 2: Still use categorical
summary = {"budget": "medium"}  # Still works!

# Option 3: Convert category to approximate amount
budget_map = {"low": 2000, "medium": 3500, "high": 6000}
summary = {"budget": budget_map.get(user_choice, 3000)}
```

---

## Summary

✅ **Numeric budgets supported**: 2500, 3000, etc.
✅ **String budgets parsed**: "2500 DA", "around 3000"
✅ **Categorical budgets still work**: "low", "medium", "high"
✅ **Smart filtering**: Price ratio-based
✅ **Transparent reasons**: Shows budget fit
✅ **Multilingual**: Works in en/ar/fr

The numeric budget feature makes recommendations more precise and user-friendly while maintaining backward compatibility with categorical budgets! 🎉
