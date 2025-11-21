"""
Test script to demonstrate API logging functionality
This script will make requests to all endpoints and show the logging output in the server console
"""

import requests
import time

BASE_URL = "http://localhost:4708"

def print_test_header(test_name):
    """Print a test header"""
    print("\n" + "="*80)
    print(f"🧪 TEST: {test_name}")
    print("="*80)

def test_recommend_endpoint():
    """Test /recommend endpoint with logging"""
    print_test_header("Testing /recommend endpoint (should show detailed logging)")
    
    # Test 1: Simple recommendation
    print("\n1. Simple recommendation request...")
    payload = {
        "category": "health_supplements",
        "needs": ["energy", "immunity"],
        "top_k": 3
    }
    
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Recommendations returned: {response.json()['count']}")
    time.sleep(1)
    
    # Test 2: Complex recommendation with constraints
    print("\n2. Complex recommendation with medical conditions...")
    payload = {
        "category": "health_supplements",
        "medical_conditions": ["diabetes", "anemia"],
        "avoid": ["sugar"],
        "budget": 5000,
        "top_k": 3
    }
    
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Recommendations returned: {response.json()['count']}")
    time.sleep(1)
    
    # Test 3: Natural language query
    print("\n3. Natural language query...")
    payload = {
        "query": "I need vitamins but I'm diabetic",
        "top_k": 5
    }
    
    response = requests.post(f"{BASE_URL}/recommend", json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Recommendations returned: {response.json()['count']}")
    time.sleep(1)

def test_product_by_id_endpoint():
    """Test /product/{product_id} endpoint with logging"""
    print_test_header("Testing /product/{product_id} endpoint (should show logging)")
    
    # Test 1: Existing product
    print("\n1. Looking up existing product (supp-001)...")
    response = requests.get(f"{BASE_URL}/product/supp-001")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Product found: {response.json()['product']['name']}")
    time.sleep(1)
    
    # Test 2: Non-existent product
    print("\n2. Looking up non-existent product (xyz-999)...")
    response = requests.get(f"{BASE_URL}/product/xyz-999")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 404:
        print(f"Expected 404: {response.json()['detail']}")
    time.sleep(1)
    
    # Test 3: Another existing product
    print("\n3. Looking up another product (skin-001)...")
    response = requests.get(f"{BASE_URL}/product/skin-001")
    print(f"Response Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Product found: {response.json()['product']['name']}")
    time.sleep(1)

def test_product_search_endpoint():
    """Test /product/search/{search_term} endpoint with logging"""
    print_test_header("Testing /product/search/{search_term} endpoint (should show logging)")
    
    # Test 1: Search for "vitamin"
    print("\n1. Searching for 'vitamin'...")
    response = requests.get(f"{BASE_URL}/product/search/vitamin")
    print(f"Response Status: {response.status_code}")
    print(f"Products found: {response.json()['count']}")
    time.sleep(1)
    
    # Test 2: Search for "baby"
    print("\n2. Searching for 'baby'...")
    response = requests.get(f"{BASE_URL}/product/search/baby")
    print(f"Response Status: {response.status_code}")
    print(f"Products found: {response.json()['count']}")
    time.sleep(1)
    
    # Test 3: Search for non-existent term
    print("\n3. Searching for 'nonexistent'...")
    response = requests.get(f"{BASE_URL}/product/search/nonexistent")
    print(f"Response Status: {response.status_code}")
    print(f"Products found: {response.json()['count']}")
    time.sleep(1)
    
    # Test 4: Search for "moisturizer"
    print("\n4. Searching for 'moisturizer'...")
    response = requests.get(f"{BASE_URL}/product/search/moisturizer")
    print(f"Response Status: {response.status_code}")
    print(f"Products found: {response.json()['count']}")
    time.sleep(1)

def main():
    """Run all tests"""
    print("="*80)
    print("🚀 STARTING LOGGING TESTS")
    print("="*80)
    print("\n📝 Check the server console to see the detailed logging output!")
    print("   Each request will show:")
    print("   - Timestamp")
    print("   - Endpoint called")
    print("   - Request parameters")
    print("   - Response summary")
    print("\n" + "="*80)
    
    try:
        # Test health check first
        print("\n🔍 Checking if server is running...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Server is running: {response.json()['status']}")
        time.sleep(1)
        
        # Run all tests
        test_recommend_endpoint()
        test_product_by_id_endpoint()
        test_product_search_endpoint()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED!")
        print("="*80)
        print("\n📝 Check the server console to see all the logging output.")
        print("   Each API call should have detailed logs showing:")
        print("   - 📥 INCOMING API CALL with timestamp and parameters")
        print("   - ✅ RESPONSE with results summary")
        print("   - ⚠️  RESPONSE for not found cases")
        print("   - ❌ ERROR for any exceptions")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server at", BASE_URL)
        print("   Please make sure the server is running:")
        print("   ./start_server.sh")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
