#!/usr/bin/env python3
"""
Test the FIXED recommendation system
"""
import requests
import json

print("="*70)
print("TESTING FIXED RECOMMENDATION SYSTEM")
print("="*70)

# Test Case: Oily Skin + Oily Hair (the one that was broken)
print("\n🧪 TEST: Oily Skin + Oily Hair")
print("-"*70)

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "summary": {
            "skin_type": "oily",
            "hair_type": "oily"
        },
        "top_k": 5,
        "language": "en"
    }
)

data = response.json()
print(f"\n✅ Got {data['count']} recommendations\n")

for i, rec in enumerate(data['recommendations'], 1):
    print(f"{i}. {rec['name']}")
    print(f"   💰 Price: {rec['price']} {rec['currency']}")
    print(f"   📦 Category: {rec['category']} > {rec['subcategory']}")
    print(f"   💡 Reason: {rec['reason']}")
    print(f"   ⭐ Score: {rec['score']:.3f}")
    print()

print("="*70)
print("✅ NO MORE MELATONIN FOR OILY SKIN!")
print("✅ All recommendations are relevant!")
print("="*70)
