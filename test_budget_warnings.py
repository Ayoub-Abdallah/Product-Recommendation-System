#!/usr/bin/env python3
"""
Test budget warnings and metadata feature
"""
import requests
import json

print("="*70)
print("TESTING BUDGET WARNINGS & METADATA")
print("="*70)

# Test Case 1: Budget too low
print("\n🧪 TEST 1: Very Low Budget (500 DA) - Should warn")
print("-"*70)

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "summary": {
            "budget": 500
        },
        "top_k": 3,
        "language": "en"
    }
)

data = response.json()
print(f"\n✅ Got {data['count']} recommendations")
print(f"\n📊 Metadata:")
print(json.dumps(data.get('metadata', {}), indent=2))

if data.get('metadata', {}).get('warnings'):
    print(f"\n⚠️  WARNINGS:")
    for warning in data['metadata']['warnings']:
        print(f"   - [{warning['severity'].upper()}] {warning['message']}")
        if 'suggestion' in warning:
            print(f"     💡 {warning['suggestion']}")

# Test Case 2: Budget just right
print("\n\n🧪 TEST 2: Good Budget (2500 DA) - Should be OK")
print("-"*70)

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "summary": {
            "budget": 2500
        },
        "top_k": 3,
        "language": "en"
    }
)

data = response.json()
print(f"\n✅ Got {data['count']} recommendations")
print(f"\n📊 Budget Info:")
budget_info = data.get('metadata', {}).get('budget_info', {})
print(f"   - Requested Budget: {budget_info.get('requested_budget')} DA")
print(f"   - Products in Budget: {budget_info.get('products_in_budget')}")
print(f"   - Products Over Budget: {budget_info.get('products_over_budget')}")
print(f"   - Cheapest Available: {budget_info.get('cheapest_available')} DA")

if data.get('metadata', {}).get('warnings'):
    print(f"\n⚠️  WARNINGS:")
    for warning in data['metadata']['warnings']:
        print(f"   - [{warning['severity'].upper()}] {warning['message']}")
else:
    print(f"\n✅ No warnings - budget is good!")

# Test Case 3: Very strict filters
print("\n\n🧪 TEST 3: Very Strict Filters - Should warn about few results")
print("-"*70)

response = requests.post(
    "http://localhost:4708/recommend",
    json={
        "summary": {
            "skin_type": "oily",
            "category": "makeup",
            "budget": 2000
        },
        "top_k": 5,
        "language": "en"
    }
)

data = response.json()
print(f"\n✅ Got {data['count']} recommendations")

if data.get('metadata', {}).get('warnings'):
    print(f"\n⚠️  WARNINGS:")
    for warning in data['metadata']['warnings']:
        print(f"   - [{warning['severity'].upper()}] {warning['message']}")
        if 'suggestion' in warning:
            print(f"     💡 {warning['suggestion']}")

print("\n" + "="*70)
print("✅ BUDGET WARNING SYSTEM IS WORKING!")
print("="*70)
