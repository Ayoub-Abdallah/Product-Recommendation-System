#!/usr/bin/env python3
"""
Test script to verify price display in recommendations
"""
import requests
import json

# Test the new summary-based recommendation endpoint
def test_summary_recommendation():
    print("=" * 60)
    print("Testing Summary-Based Recommendation with Price Display")
    print("=" * 60)
    
    url = "http://localhost:4708/recommend/summary"
    
    # Test case 1: Budget 2500 DA
    test_cases = [
        {
            "name": "Budget 2500 DA - Oily Skin",
            "payload": {
                "summary": {
                    "skin_type": "oily",
                    "budget": 2500,
                    "problem": "acne"
                },
                "top_k": 3,
                "language": "en"
            }
        },
        {
            "name": "Budget 'low' - Dry Skin",
            "payload": {
                "summary": {
                    "skin_type": "dry",
                    "budget": "low",
                    "problem": "wrinkles"
                },
                "top_k": 3,
                "language": "en"
            }
        },
        {
            "name": "Budget 5000 DA - All Products",
            "payload": {
                "summary": {
                    "budget": 5000
                },
                "top_k": 5,
                "language": "en"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test_case['name']}")
        print(f"{'='*60}")
        
        try:
            response = requests.post(url, json=test_case['payload'])
            response.raise_for_status()
            
            data = response.json()
            recommendations = data.get('recommendations', [])
            
            print(f"\n✅ Found {len(recommendations)} recommendations\n")
            
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec['name']}")
                print(f"   Price: {rec.get('price', 'N/A')} {rec.get('currency', 'DA')}")
                print(f"   Category: {rec.get('category', 'N/A')} > {rec.get('subcategory', 'N/A')}")
                print(f"   Score: {rec['score']:.3f}")
                print(f"   Reason: {rec['reason'][:80]}...")
                print()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    print(f"   Detail: {error_detail}")
                except:
                    print(f"   Response: {e.response.text}")
            
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_summary_recommendation()
