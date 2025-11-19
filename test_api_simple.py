#!/usr/bin/env python3
"""
Simple API Test Script
Shows how to call the Beauty & Health Recommendation API
"""

import requests
import json

# API Configuration
BASE_URL = "http://localhost:4708"

def print_separator(title=""):
    print("\n" + "="*70)
    if title:
        print(f"  {title}")
        print("="*70)

def test_health():
    """Test 1: Check if API is running"""
    print_separator("TEST 1: Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"✅ Service: {data['service']}")
        print(f"✅ Products: {data['products_loaded']}")
        print(f"✅ Categories: {data['categories']}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_stats():
    """Test 2: Get system statistics"""
    print_separator("TEST 2: System Statistics")
    
    response = requests.get(f"{BASE_URL}/stats")
    if response.status_code == 200:
        data = response.json()
        print(f"📊 Total Products: {data['total_products']}")
        print(f"📊 Index Type: {data['index_type']}")
        print(f"\n📦 Products by Category:")
        for category, count in data['categories'].items():
            print(f"   - {category}: {count}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_recommend(summary, top_k=3):
    """Test 3: Get recommendations"""
    print_separator(f"TEST 3: Get Recommendations")
    
    print(f"📝 Request:")
    print(json.dumps({"summary": summary, "top_k": top_k}, indent=2))
    print()
    
    response = requests.post(
        f"{BASE_URL}/recommend",
        json={"summary": summary, "top_k": top_k}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Got {data['count']} recommendation(s)\n")
        
        for i, product in enumerate(data['recommendations'], 1):
            print(f"{i}. {product['name']}")
            print(f"   💰 Price: {product['price']} {product['currency']}")
            print(f"   📦 Category: {product['category']} > {product['subcategory']}")
            print(f"   🏷️  Tags: {', '.join(product['tags'][:5])}")
            print(f"   💡 Reason: {product['reason']}")
            print(f"   ⭐ Score: {product['score']:.3f}")
            print()
        
        # Show metadata
        if 'metadata' in data:
            metadata = data['metadata']
            if metadata.get('warnings'):
                print("⚠️  WARNINGS:")
                for warning in metadata['warnings']:
                    print(f"   - [{warning['severity'].upper()}] {warning['message']}")
                    if 'suggestion' in warning:
                        print(f"     💡 {warning['suggestion']}")
                print()
            
            if 'budget_info' in metadata:
                budget_info = metadata['budget_info']
                print("💰 Budget Info:")
                print(f"   - Requested: {budget_info.get('requested_budget', 'N/A')} DA")
                print(f"   - In Budget: {budget_info.get('products_in_budget', 0)} products")
                print(f"   - Cheapest: {budget_info.get('cheapest_available', 'N/A')} DA")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def main():
    """Run all tests"""
    print("\n" + "🌟 BEAUTY & HEALTH RECOMMENDATION API TEST" + "\n")
    
    try:
        # Test 1: Health check
        test_health()
        
        # Test 2: Statistics
        test_stats()
        
        # Test 3a: Simple recommendation
        test_recommend({
            "skin_type": "oily",
            "concerns": ["acne"]
        })
        
        # Test 3b: Recommendation with budget
        test_recommend({
            "skin_type": "dry",
            "concerns": ["wrinkles"],
            "budget": 3000
        })
        
        # Test 3c: Hair care
        test_recommend({
            "hair_type": "curly",
            "category": "hair_care",
            "concerns": ["frizz"],
            "budget": "medium"
        })
        
        # Test 3d: Supplements
        test_recommend({
            "category": "supplements",
            "concerns": ["energy", "immunity"]
        })
        
        print_separator("✅ ALL TESTS COMPLETED")
        print("\n💡 TIP: Open http://localhost:4708/docs for interactive API testing\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("💡 Make sure the server is running:")
        print("   ./start_server.sh\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")

if __name__ == "__main__":
    main()
