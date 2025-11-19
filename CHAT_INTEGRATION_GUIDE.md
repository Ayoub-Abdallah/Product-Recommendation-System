# Chat System Integration Guide

This guide explains how to integrate the Beauty Recommendation API with your chat system to provide intelligent product recommendations based on user conversations.

## Overview

The integration flow:
```
User Message → Extract Info → Build Summary → API Call → Display Products
```

## Integration Steps

### Step 1: Extract Information from Conversation

As the chat system interacts with the user, extract relevant information:

```python
class ConversationSummaryBuilder:
    def __init__(self):
        self.summary = {}
    
    def extract_skin_type(self, message):
        """Extract skin type from user message"""
        message_lower = message.lower()
        
        skin_types = {
            'oily': ['oily', 'greasy', 'shine', 'shiny'],
            'dry': ['dry', 'flaky', 'tight', 'dehydrated'],
            'combination': ['combination', 'combo', 'mixed'],
            'normal': ['normal', 'balanced'],
            'sensitive': ['sensitive', 'reactive', 'irritated']
        }
        
        for skin_type, keywords in skin_types.items():
            if any(keyword in message_lower for keyword in keywords):
                self.summary['skin_type'] = skin_type
                return skin_type
        
        return None
    
    def extract_problem(self, message):
        """Extract skin/hair problem from user message"""
        message_lower = message.lower()
        
        problems = {
            'acne': ['acne', 'pimples', 'breakout', 'spots'],
            'wrinkles': ['wrinkles', 'aging', 'fine lines', 'anti-aging'],
            'dark_spots': ['dark spots', 'hyperpigmentation', 'pigmentation', 'discoloration'],
            'dryness': ['dryness', 'dry', 'dehydrated', 'flaky'],
            'frizz': ['frizz', 'frizzy', 'flyaways'],
            'hair_loss': ['hair loss', 'thinning', 'falling'],
            'hydration': ['hydrate', 'moisture', 'hydration']
        }
        
        for problem, keywords in problems.items():
            if any(keyword in message_lower for keyword in keywords):
                self.summary['problem'] = problem
                return problem
        
        return None
    
    def extract_budget(self, message):
        """Extract budget from user message"""
        message_lower = message.lower()
        
        # Check for price mentions
        import re
        price_match = re.search(r'(\d+)\s*(da|dinar)', message_lower)
        if price_match:
            price = int(price_match.group(1))
            if price < 2000:
                self.summary['budget'] = 'low'
                return 'low'
            elif price < 4000:
                self.summary['budget'] = 'medium'
                return 'medium'
            else:
                self.summary['budget'] = 'high'
                return 'high'
        
        # Check for budget keywords
        if any(word in message_lower for word in ['cheap', 'affordable', 'budget']):
            self.summary['budget'] = 'low'
            return 'low'
        elif any(word in message_lower for word in ['expensive', 'premium', 'luxury']):
            self.summary['budget'] = 'high'
            return 'high'
        
        return None
    
    def extract_age(self, message):
        """Extract age from user message"""
        import re
        
        # Check for age mentions
        age_match = re.search(r'(\d+)\s*(years? old|y/?o)', message.lower())
        if age_match:
            age = age_match.group(1)
            self.summary['age'] = age
            return age
        
        return None
    
    def extract_category(self, message):
        """Extract product category from user message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['skin', 'face', 'facial']):
            self.summary['category'] = 'skin_care'
            return 'skin_care'
        elif any(word in message_lower for word in ['hair', 'scalp']):
            self.summary['category'] = 'hair_care'
            return 'hair_care'
        elif any(word in message_lower for word in ['makeup', 'cosmetic']):
            self.summary['category'] = 'makeup'
            return 'makeup'
        
        return None
    
    def process_message(self, message):
        """Process a user message and update summary"""
        self.extract_skin_type(message)
        self.extract_problem(message)
        self.extract_budget(message)
        self.extract_age(message)
        self.extract_category(message)
        
        return self.summary
    
    def get_summary(self):
        """Get the current summary"""
        return self.summary
```

### Step 2: Call the Recommendation API

Once you have enough information, call the API:

```python
import requests

class RecommendationClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_recommendations(self, summary, top_k=3, language='en'):
        """Get product recommendations from API"""
        try:
            response = requests.post(
                f"{self.base_url}/recommend/summary",
                json={
                    "summary": summary,
                    "top_k": top_k,
                    "language": language
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("Cannot connect to recommendation service")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
```

### Step 3: Format and Display Results

Present the recommendations to the user:

```python
class ChatResponseFormatter:
    @staticmethod
    def format_recommendations(recommendations_data, language='en'):
        """Format recommendations for chat display"""
        if not recommendations_data:
            return "Sorry, I couldn't get recommendations right now."
        
        recommendations = recommendations_data.get('recommendations', [])
        count = recommendations_data.get('count', 0)
        
        if count == 0:
            return "I couldn't find products matching your criteria. Let me know if you'd like different suggestions!"
        
        # Build response
        if language == 'ar':
            response = f"وجدت {count} منتجات مناسبة لك:\n\n"
        elif language == 'fr':
            response = f"J'ai trouvé {count} produits pour vous:\n\n"
        else:
            response = f"I found {count} great product(s) for you:\n\n"
        
        for i, product in enumerate(recommendations, 1):
            response += f"{i}. **{product['name']}**\n"
            response += f"   💰 {product['price']} {product['currency']}\n"
            response += f"   💡 {product['reason']}\n"
            response += f"   🏷️ {', '.join(product['tags'][:3])}\n\n"
        
        return response
    
    @staticmethod
    def format_product_card(product):
        """Format a single product as a rich card"""
        return {
            'type': 'product_card',
            'id': product['id'],
            'name': product['name'],
            'price': f"{product['price']} {product['currency']}",
            'image': product.get('image', ''),
            'description': product.get('description', ''),
            'reason': product['reason'],
            'tags': product.get('tags', []),
            'action': {
                'label': 'View Details',
                'url': f"/products/{product['id']}"
            }
        }
```

### Step 4: Complete Integration Example

```python
class BeautyConsultantBot:
    def __init__(self, api_url="http://localhost:8000"):
        self.summary_builder = ConversationSummaryBuilder()
        self.recommendation_client = RecommendationClient(api_url)
        self.formatter = ChatResponseFormatter()
        self.language = 'en'  # Default language
        self.message_count = 0
    
    def process_message(self, user_message):
        """Process a user message and return response"""
        self.message_count += 1
        
        # Extract information
        self.summary_builder.process_message(user_message)
        summary = self.summary_builder.get_summary()
        
        # Detect language
        if any(arabic_char in user_message for arabic_char in 'أإآابتثجحخدذرزسشصضطظعغفقكلمنهويى'):
            self.language = 'ar'
        elif any(word in user_message.lower() for word in ['bonjour', 'merci', 'oui', 'non']):
            self.language = 'fr'
        
        # Generate response based on conversation state
        
        # If we have enough info (after a few messages), provide recommendations
        if self.message_count >= 2 and len(summary) >= 2:
            return self.provide_recommendations(summary)
        
        # Otherwise, ask clarifying questions
        return self.ask_clarifying_question(summary)
    
    def ask_clarifying_question(self, summary):
        """Ask for missing information"""
        if 'skin_type' not in summary and 'hair_type' not in summary:
            if self.language == 'ar':
                return "ما هو نوع بشرتك؟ (دهنية، جافة، مختلطة، عادية، حساسة)"
            elif self.language == 'fr':
                return "Quel est votre type de peau ? (grasse, sèche, mixte, normale, sensible)"
            else:
                return "What's your skin type? (oily, dry, combination, normal, sensitive)"
        
        if 'problem' not in summary:
            if self.language == 'ar':
                return "ما هي مشكلة البشرة أو الشعر التي تعانين منها؟"
            elif self.language == 'fr':
                return "Quel problème de peau ou de cheveux avez-vous ?"
            else:
                return "What skin or hair concern would you like to address?"
        
        if 'budget' not in summary:
            if self.language == 'ar':
                return "ما هي ميزانيتك التقريبية؟"
            elif self.language == 'fr':
                return "Quel est votre budget approximatif ?"
            else:
                return "What's your approximate budget?"
        
        # Have enough info, provide recommendations
        return self.provide_recommendations(summary)
    
    def provide_recommendations(self, summary):
        """Get and format recommendations"""
        # Call API
        recommendations_data = self.recommendation_client.get_recommendations(
            summary=summary,
            top_k=3,
            language=self.language
        )
        
        if not recommendations_data:
            return "Sorry, I'm having trouble accessing recommendations right now. Please try again."
        
        # Format response
        return self.formatter.format_recommendations(recommendations_data, self.language)

# Usage example
bot = BeautyConsultantBot()

# Simulate conversation
messages = [
    "Hi, I need help with my skin",
    "I have oily skin and acne problems",
    "My budget is around 2500 DA"
]

for message in messages:
    print(f"User: {message}")
    response = bot.process_message(message)
    print(f"Bot: {response}\n")
```

## Example Conversations

### Example 1: Skin Care Consultation (English)

```
User: Hi, I need skincare advice
Bot: What's your skin type? (oily, dry, combination, normal, sensitive)

User: I have oily skin
Bot: What skin or hair concern would you like to address?

User: I'm struggling with acne and large pores
Bot: What's your approximate budget?

User: Around 2500 DA
Bot: I found 3 great products for you:

1. **Niacinamide Serum 10% + Zinc 1%**
   💰 2500 DA
   💡 Perfect for your oily skin type • Addresses your acne concern
   🏷️ oily_skin, acne, sebum_control

2. **Salicylic Acid BHA Exfoliant**
   💰 2200 DA
   💡 Great for treating acne and minimizing pores
   🏷️ acne, exfoliation, pores
```

### Example 2: Hair Care Consultation (Arabic)

```
User: أحتاج مساعدة للعناية بشعري
Bot: ما هو نوع شعرك؟

User: شعري مجعد وجاف
Bot: ما هي المشكلة التي تعانين منها؟

User: الهيشان والتجعد
Bot: وجدت 3 منتجات مناسبة لك:

1. **كريم تحديد التجعيد**
   💰 3000 DA
   💡 مثالي لنوع شعرك (curly) • يعالج مشكلة frizz
   🏷️ curly_hair, anti_frizz, definition
```

## Advanced Features

### Conditional Recommendations

```python
def smart_recommend(summary, conversation_history):
    """Smart recommendation based on context"""
    
    # If user mentioned specific product types
    if 'serum' in conversation_history:
        summary['product_type'] = 'serum'
    
    # If user seems price-sensitive
    if any(word in conversation_history for word in ['cheap', 'affordable', 'budget']):
        summary['budget'] = 'low'
    
    # If user mentioned age-related concerns
    if any(word in conversation_history for word in ['aging', 'wrinkles', 'mature']):
        summary['age'] = '40+'
    
    return summary
```

### Multi-Turn Refinement

```python
class RefinementHandler:
    def handle_refinement(self, user_feedback, previous_recommendations):
        """Handle user feedback to refine recommendations"""
        
        if "too expensive" in user_feedback.lower():
            # Adjust budget downward
            return {"budget": "low"}
        
        if "stronger" in user_feedback.lower():
            # User wants more intensive treatment
            return {"budget": "high"}
        
        if "sensitive" in user_feedback.lower():
            # User has sensitive skin
            return {"skin_type": "sensitive"}
        
        return {}
```

### Personalization Based on History

```python
class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.purchase_history = []
        self.viewed_products = []
        self.preferences = {}
    
    def update_from_interaction(self, summary, recommendations, selected_product):
        """Learn from user interactions"""
        
        # Store preferences
        if 'budget' in summary:
            self.preferences['budget'] = summary['budget']
        
        if selected_product:
            self.purchase_history.append(selected_product)
            
            # Update summary for future recommendations
            summary['personal'] = 1.0  # Boost for personalized recommendations
```

## Testing Your Integration

### Unit Tests

```python
import unittest

class TestChatIntegration(unittest.TestCase):
    def setUp(self):
        self.bot = BeautyConsultantBot()
    
    def test_skin_type_extraction(self):
        message = "I have oily skin"
        self.bot.process_message(message)
        summary = self.bot.summary_builder.get_summary()
        self.assertEqual(summary['skin_type'], 'oily')
    
    def test_problem_extraction(self):
        message = "I'm struggling with acne"
        self.bot.process_message(message)
        summary = self.bot.summary_builder.get_summary()
        self.assertEqual(summary['problem'], 'acne')
    
    def test_budget_extraction(self):
        message = "My budget is 2500 DA"
        self.bot.process_message(message)
        summary = self.bot.summary_builder.get_summary()
        self.assertEqual(summary['budget'], 'medium')
```

### Integration Tests

```python
def test_full_conversation():
    """Test complete conversation flow"""
    bot = BeautyConsultantBot()
    
    # Simulate conversation
    bot.process_message("I have oily skin")
    bot.process_message("I have acne")
    response = bot.process_message("Budget is 2500 DA")
    
    # Should contain recommendations
    assert "found" in response.lower()
    assert "DA" in response
```

## Error Handling

```python
class RobustRecommendationClient:
    def get_recommendations_with_fallback(self, summary, top_k=3):
        """Get recommendations with graceful fallback"""
        try:
            # Try API call
            result = self.get_recommendations(summary, top_k)
            
            if result and result.get('count', 0) > 0:
                return result
            
            # Fallback: Relax constraints
            fallback_summary = {
                'problem': summary.get('problem'),
                'category': summary.get('category')
            }
            
            result = self.get_recommendations(fallback_summary, top_k)
            
            if result:
                return result
            
            # Last resort: Generic recommendations
            return self.get_generic_recommendations()
            
        except Exception as e:
            print(f"Error: {e}")
            return self.get_generic_recommendations()
    
    def get_generic_recommendations(self):
        """Return generic fallback recommendations"""
        return {
            "recommendations": [
                {
                    "name": "Multi-Purpose Beauty Set",
                    "price": 3000,
                    "currency": "DA",
                    "reason": "Popular choice for general skincare"
                }
            ],
            "count": 1
        }
```

## Best Practices

1. **Progressive Information Gathering**
   - Don't ask all questions at once
   - Build summary gradually from conversation

2. **Validate Extractions**
   - Confirm extracted information with user
   - "Just to confirm, you have oily skin, correct?"

3. **Handle Ambiguity**
   - If uncertain, ask clarifying questions
   - Provide options: "Do you mean dry skin or dry hair?"

4. **Respect Privacy**
   - Don't store sensitive information unnecessarily
   - Follow data protection regulations

5. **Graceful Degradation**
   - Provide recommendations even with minimal information
   - Use fallbacks when API is unavailable

6. **Cultural Sensitivity**
   - Adapt language and recommendations to culture
   - Respect local beauty standards and preferences

## Performance Optimization

```python
# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_recommendations(summary_hash, top_k):
    """Cache recommendations to reduce API calls"""
    return recommendation_client.get_recommendations(summary, top_k)

# Async for better performance
import asyncio
import aiohttp

async def get_recommendations_async(summary):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}/recommend/summary",
            json={"summary": summary}
        ) as response:
            return await response.json()
```

## Monitoring and Analytics

```python
class AnalyticsTracker:
    def track_recommendation_request(self, summary, results):
        """Track recommendation requests for analytics"""
        event = {
            'timestamp': datetime.now(),
            'summary': summary,
            'result_count': results.get('count', 0),
            'language': results.get('language', 'en')
        }
        # Send to analytics system
        self.log_event(event)
    
    def track_user_selection(self, product_id, position):
        """Track which products users select"""
        event = {
            'timestamp': datetime.now(),
            'product_id': product_id,
            'position': position,
            'action': 'selected'
        }
        self.log_event(event)
```

## Conclusion

This integration guide provides everything you need to connect your chat system with the Beauty Recommendation API. The key is to:

1. Extract information naturally from conversation
2. Build a comprehensive summary
3. Call the API with the summary
4. Format and present results beautifully

For more details, see:
- [API Documentation](API_DOCUMENTATION.md)
- [Quick Start Guide](QUICKSTART.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
