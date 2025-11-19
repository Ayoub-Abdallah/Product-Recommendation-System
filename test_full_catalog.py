#!/usr/bin/env python3
"""
Test the expanded beauty & health product catalog
"""
import requests
import json

def test_recommendations():
    print("="*70)
    print("TESTING BEAUTY & HEALTH PRODUCT RECOMMENDATION SYSTEM")
    print("="*70)
    
    url = "http://localhost:4708/recommend"
    
    test_cases = [
        {
            "name": "Skincare - Oily Skin with Acne (Budget 2500 DA)",
            "payload": {
                "summary": {
                    "skin_type": "oily",
                    "problem": "acne",
                    "budget": 2500
                },
                "top_k": 3,
                "language": "en"
            }
        },
        {
            "name": "Hair Care - Dry Curly Hair",
            "payload": {
                "summary": {
                    "hair_type": "curly",
                    "problem": "frizz",
                    "category": "hair_care"
                },
                "top_k": 3,
                "language": "en"
            }
        },
        {
            "name": "Supplements - Hair Growth & Beauty",
            "payload": {
                "summary": {
                    "problem": "hair loss",
                    "category": "supplements"
                },
                "top_k": 3,
                "language": "en"
            }
        },
        {
            "name": "Wellness - Sleep Support",
            "payload": {
                "summary": {
                    "problem": "insomnia",
                    "category": "wellness"
                },
                "top_k": 2,
                "language": "en"
            }
        },
        {
            "name": "Makeup - Oily Skin Foundation",
            "payload": {
                "summary": {
                    "skin_type": "oily",
                    "category": "makeup"
                },
                "top_k": 2,
                "language": "en"
            }
        },
        {
            "name": "Anti-Aging - All Categories (Budget: High)",
            "payload": {
                "summary": {
                    "problem": "wrinkles",
                    "budget": "high",
                    "age": "40+"
                },
                "top_k": 5,
                "language": "en"
            }
        },
        {
            "name": "Budget Test - Low Budget Products",
            "payload": {
                "summary": {
                    "budget": 2000
                },
                "top_k": 5,
                "language": "en"
            }
        },
        {
            "name": "French Language Test",
            "payload": {
                "summary": {
                    "skin_type": "dry",
                    "problem": "wrinkles"
                },
                "top_k": 3,
                "language": "fr"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(test_cases)}: {test_case['name']}")
        print(f"{'='*70}")
        
        try:
            response = requests.post(url, json=test_case['payload'])
            response.raise_for_status()
            
            data = response.json()
            recommendations = data.get('recommendations', [])
            
            if recommendations:
                print(f"\n✅ Found {len(recommendations)} recommendation(s)\n")
                
                for j, rec in enumerate(recommendations, 1):
                    print(f"{j}. {rec['name']}")
                    print(f"   💰 Price: {rec.get('price', 'N/A')} {rec.get('currency', 'DA')}")
                    print(f"   📦 Category: {rec.get('category', 'N/A')} > {rec.get('subcategory', 'N/A')}")
                    print(f"   ⭐ Score: {rec['score']:.3f}")
                    print(f"   💡 Reason: {rec['reason'][:100]}...")
                    if rec.get('tags'):
                        print(f"   🏷️  Tags: {', '.join(rec['tags'][:5])}")
                    print()
            else:
                print("❌ No recommendations found")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Detail: {error_detail}")
                except:
                    print(f"   Response: {e.response.text[:200]}")
    
    # Test the products endpoint
    print(f"\n{'='*70}")
    print("TESTING PRODUCTS ENDPOINT")
    print(f"{'='*70}")
    
    try:
        response = requests.get("http://localhost:4708/products")
        response.raise_for_status()
        products = response.json()
        print(f"✅ Total products available: {len(products)}")
        
        # Count by category
        categories = {}
        for product in products:
            cat = product.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\nProducts by category:")
        for cat, count in sorted(categories.items()):
            print(f"   - {cat}: {count} products")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test categories endpoint
    print(f"\n{'='*70}")
    print("TESTING CATEGORIES ENDPOINT")
    print(f"{'='*70}")
    
    try:
        response = requests.get("http://localhost:4708/categories")
        response.raise_for_status()
        categories = response.json()
        print(f"✅ Available categories:\n")
        for cat, subcats in sorted(categories.items()):
            print(f"   {cat}:")
            for subcat in sorted(subcats):
                print(f"      - {subcat}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test health endpoint
    print(f"\n{'='*70}")
    print("TESTING HEALTH CHECK ENDPOINT")
    print(f"{'='*70}")
    
    try:
        response = requests.get("http://localhost:4708/health")
        response.raise_for_status()
        health = response.json()
        print(f"✅ System Status:")
        for key, value in health.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print(f"\n{'='*70}")
    print("ALL TESTS COMPLETE!")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    test_recommendations()
