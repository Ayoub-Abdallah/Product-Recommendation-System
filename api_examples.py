#!/usr/bin/env python3
"""
Valid API Request Examples - Working Code
Run this to see how to properly send requests to the API
"""

import requests
import json

BASE_URL = "http://localhost:4708"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def example_1_minimal_request():
    """Example 1: Minimal request (all fields optional)"""
    print_section("EXAMPLE 1: Minimal Request (Empty Body)")
    
    print("Request:")
    print("  POST /recommend")
    print("  Body: {}")
    print()
    
    response = requests.post(
        f"{BASE_URL}/recommend",
        json={}  # Empty body is valid!
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Got {data['count']} recommendations")
        for rec in data['recommendations'][:2]:
            print(f"  - {rec['name']} ({rec['price']} DA)")
    else:
        print(f"❌ Error: {response.text}")

def example_2_simple_category():
    """Example 2: Simple category search"""
    print_section("EXAMPLE 2: Search by Category")
    
    request_data = {
        "category": "health_supplements",
        "top_k": 3
    }
    
    print("Request:")
    print(json.dumps(request_data, indent=2))
    print()
    
    response = requests.post(
        f"{BASE_URL}/recommend",
        json=request_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Got {data['count']} recommendations")
        for i, rec in enumerate(data['recommendations'], 1):
            print(f"\n{i}. {rec['name']}")
            print(f"   Price: {rec['price']} DA")
            print(f"   Reason: {rec['reason']}")
    else:
        print(f"❌ Error: {response.text}")

def example_3_medical_conditions():
    """Example 3: Complex query with medical conditions"""
    print_section("EXAMPLE 3: Diabetic with Anemia")
    
    request_data = {
        "category": "health_supplements",
        "medical_conditions": ["diabetes", "anemia"],
        "needs": ["energy", "immunity"],
        "avoid": ["sugar"],
        "budget": 5000,
        "top_k": 3
    }
    
    print("Request:")
    print(json.dumps(request_data, indent=2))
    print()
    
    response = requests.post(
        f"{BASE_URL}/recommend",
        json=request_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Got {data['count']} recommendations\n")
        
        for i, rec in enumerate(data['recommendations'], 1):
            print(f"{i}. {rec['name']}")
            print(f"   💰 Price: {rec['price']} DA")
            print(f"   💡 Reason: {rec['reason']}")
            if rec.get('safety_notes'):
                print(f"   ⚕️  Safety: {', '.join(rec['safety_notes'])}")
            print()
        
        # Show metadata
        metadata = data.get('metadata', {})
        if metadata.get('constraints_applied'):
            print(f"🔒 Constraints Applied: {', '.join(metadata['constraints_applied'])}")
        
        if metadata.get('warnings'):
            print(f"\n⚠️  Warnings: {len(metadata['warnings'])}")
    else:
        print(f"❌ Error: {response.text}")

def example_4_skin_conditions():
    """Example 4: Beauty products for sensitive skin"""
    print_section("EXAMPLE 4: Dry + Sensitive Skin")
    
    request_data = {
        "category": "beauty_skincare",
        "skin_conditions": ["dry", "sensitive"],
        "avoid": ["fragrance"],
        "preferences": ["hypoallergenic"],
        "top_k": 2
    }
    
    print("Request:")
    print(json.dumps(request_data, indent=2))
    print()
    
    response = requests.post(
        f"{BASE_URL}/recommend",
        json=request_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Got {data['count']} recommendations\n")
        for rec in data['recommendations']:
            print(f"- {rec['name']} ({rec['price']} DA)")
            print(f"  {rec['reason']}")
    else:
        print(f"❌ Error: {response.text}")

def example_5_natural_language():
    """Example 5: Natural language query"""
    print_section("EXAMPLE 5: Natural Language Query")
    
    request_data = {
        "query": "I have diabetes and anemia, need vitamins without sugar",
        "top_k": 3
    }
    
    print("Request:")
    print(json.dumps(request_data, indent=2))
    print()
    
    response = requests.post(
        f"{BASE_URL}/recommend",
        json=request_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Got {data['count']} recommendations\n")
        for rec in data['recommendations']:
            print(f"- {rec['name']} ({rec['price']} DA)")
    else:
        print(f"❌ Error: {response.text}")

def example_6_product_lookup():
    """Example 6: Get specific product by ID"""
    print_section("EXAMPLE 6: Get Product by ID")
    
    product_id = "supp-001"
    print(f"Request: GET /product/{product_id}\n")
    
    response = requests.get(f"{BASE_URL}/product/{product_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        product = data['product']
        print(f"✅ Found product!\n")
        print(f"ID: {product['id']}")
        print(f"Name: {product['name']}")
        print(f"Price: {product['price']} {product['currency']}")
        print(f"Category: {product['category']}")
        print(f"Stock: {product.get('stock', 0)}")
    else:
        print(f"❌ Error: {response.text}")

def example_7_search_products():
    """Example 7: Search products by name"""
    print_section("EXAMPLE 7: Search Products")
    
    search_term = "vitamin"
    print(f"Request: GET /product/search/{search_term}\n")
    
    response = requests.get(f"{BASE_URL}/product/search/{search_term}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['count']} products matching '{search_term}'\n")
        for product in data['products'][:3]:
            print(f"- [{product['id']}] {product['name']} - {product['price']} DA")
    else:
        print(f"❌ Error: {response.text}")

def main():
    print("\n" + "🚀 VALID API REQUEST EXAMPLES")
    print("="*70)
    print(f"Server: {BASE_URL}")
    print("="*70)
    
    # Check server health first
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print(f"\n❌ Server not responding correctly at {BASE_URL}")
            print("Make sure server is running on port 4708")
            return
        print("✅ Server is running!\n")
    except Exception as e:
        print(f"\n❌ Cannot connect to server at {BASE_URL}")
        print(f"Error: {e}")
        print("\nStart the server with:")
        print("  python -m uvicorn app:app --host 0.0.0.0 --port 4708")
        return
    
    # Run all examples
    try:
        example_1_minimal_request()
        example_2_simple_category()
        example_3_medical_conditions()
        example_4_skin_conditions()
        example_5_natural_language()
        example_6_product_lookup()
        example_7_search_products()
        
        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nKey Takeaways:")
        print("  1. Use requests.post() with json= parameter")
        print("  2. All fields in /recommend are optional")
        print("  3. Arrays must be lists: ['item1', 'item2']")
        print("  4. top_k must be between 1-10")
        print("  5. Use requests.get() for /product/* endpoints")
        print("\n📚 View API docs: http://localhost:4708/docs\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
