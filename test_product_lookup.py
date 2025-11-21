#!/usr/bin/env python3
"""
Test the product lookup endpoints
"""

import requests
import json

BASE_URL = "http://localhost:4708"

def print_separator(title=""):
    print("\n" + "="*80)
    if title:
        print(f"  {title}")
        print("="*80)

def test_get_product_by_id():
    """Test getting a specific product by ID"""
    print_separator("TEST 1: Get Product by ID")
    
    # Try to get the sugar-free multivitamin
    product_id = "supp-001"
    
    print(f"\n📝 Request: GET /product/{product_id}")
    response = requests.get(f"{BASE_URL}/product/{product_id}")
    
    if response.status_code == 200:
        data = response.json()
        product = data['product']
        print(f"\n✅ Found product!")
        print(f"   ID: {product['id']}")
        print(f"   Name: {product['name']}")
        print(f"   Category: {product['category']} > {product['subcategory']}")
        print(f"   Price: {product['price']} {product['currency']}")
        print(f"   Tags: {', '.join(product['tags'][:5])}")
        print(f"   Stock: {product.get('stock', 0)}")
        if 'medical_conditions' in product:
            med = product['medical_conditions']
            if 'safe_for' in med:
                print(f"   Safe for: {', '.join(med['safe_for'])}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.json())

def test_get_product_by_id_not_found():
    """Test getting a non-existent product"""
    print_separator("TEST 2: Get Non-Existent Product (404 Expected)")
    
    product_id = "INVALID-999"
    
    print(f"\n📝 Request: GET /product/{product_id}")
    response = requests.get(f"{BASE_URL}/product/{product_id}")
    
    if response.status_code == 404:
        print(f"\n✅ Correctly returned 404 for invalid ID")
        print(f"   Message: {response.json()['detail']}")
    else:
        print(f"❌ Unexpected status code: {response.status_code}")

def test_search_product_by_name():
    """Test searching products by name"""
    print_separator("TEST 3: Search Products by Name")
    
    search_terms = ["vitamin", "sugar", "baby", "diabetic", "skin"]
    
    for search_term in search_terms:
        print(f"\n📝 Request: GET /product/search/{search_term}")
        response = requests.get(f"{BASE_URL}/product/search/{search_term}")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Found {data['count']} product(s) matching '{search_term}':")
                for product in data['products'][:3]:  # Show first 3
                    print(f"   - [{product['id']}] {product['name']} - {product['price']} {product['currency']}")
                if data['count'] > 3:
                    print(f"   ... and {data['count'] - 3} more")
            else:
                print(f"ℹ️  No results for '{search_term}'")
        else:
            print(f"❌ Error: {response.status_code}")

def test_search_no_match():
    """Test searching for non-existent product name"""
    print_separator("TEST 4: Search with No Matches")
    
    search_term = "xyz123notfound"
    
    print(f"\n📝 Request: GET /product/search/{search_term}")
    response = requests.get(f"{BASE_URL}/product/search/{search_term}")
    
    if response.status_code == 200:
        data = response.json()
        if data['success'] == False:
            print(f"✅ Correctly returned no results")
            print(f"   Message: {data['message']}")
        else:
            print(f"❌ Should have returned no results")
    else:
        print(f"❌ Error: {response.status_code}")

def test_all_product_ids():
    """List all available product IDs"""
    print_separator("TEST 5: List All Available Products")
    
    print(f"\n📝 Request: GET /products")
    response = requests.get(f"{BASE_URL}/products")
    
    if response.status_code == 200:
        products = response.json()
        print(f"\n✅ Available Products ({len(products)}):\n")
        
        # Group by category
        by_category = {}
        for product in products:
            cat = product.get('category', 'other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(product)
        
        for category, prods in sorted(by_category.items()):
            print(f"   📦 {category.upper().replace('_', ' ')}")
            for product in prods:
                print(f"      [{product['id']}] {product['name']} - {product['price']} DA")
            print()
    else:
        print(f"❌ Error: {response.status_code}")

def test_case_insensitive():
    """Test case-insensitive search"""
    print_separator("TEST 6: Case-Insensitive Search")
    
    test_ids = ["SUPP-001", "Supp-001", "supp-001"]
    
    for product_id in test_ids:
        print(f"\n📝 Request: GET /product/{product_id}")
        response = requests.get(f"{BASE_URL}/product/{product_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found: {data['product']['name']}")
        else:
            print(f"❌ Failed for {product_id}")

def test_search_multilanguage():
    """Test searching in different languages"""
    print_separator("TEST 7: Multi-Language Search")
    
    # Search for Arabic/French terms if they exist
    search_terms = ["فيتامين", "vitamine", "bébé"]
    
    for term in search_terms:
        print(f"\n📝 Request: GET /product/search/{term}")
        response = requests.get(f"{BASE_URL}/product/search/{term}")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Found {data['count']} product(s) for '{term}'")
            else:
                print(f"ℹ️  No results for '{term}'")

def main():
    print("\n" + "🧪 PRODUCT LOOKUP ENDPOINT TESTS" + "\n")
    
    try:
        # Check server health
        print("Checking server health...")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print(f"❌ Server is not running at {BASE_URL}")
            print("   Please start the server with:")
            print("   ./venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 4708")
            return
        
        print("✅ Server is running\n")
        
        # Run all tests
        test_all_product_ids()
        test_get_product_by_id()
        test_get_product_by_id_not_found()
        test_search_product_by_name()
        test_search_no_match()
        test_case_insensitive()
        test_search_multilanguage()
        
        print_separator("✅ ALL TESTS COMPLETED")
        print("\n💡 New Endpoints Available:")
        print("   - GET /product/{product_id} - Get specific product by ID")
        print("   - GET /product/search/{search_term} - Search products by name/tags")
        print()
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to server at {BASE_URL}")
        print("   Please start the server with:")
        print("   ./venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 4708\n")
    except Exception as e:
        print(f"\n❌ Error running tests: {str(e)}\n")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
