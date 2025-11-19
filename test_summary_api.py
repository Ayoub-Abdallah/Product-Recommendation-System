#!/usr/bin/env python3
"""
Test script for the new summary-based recommendation API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_summary_recommendation():
    """Test summary-based recommendation"""
    print("\n=== Testing Summary Recommendation (English) ===")
    
    payload = {
        "summary": {
            "skin_type": "oily",
            "problem": "acne",
            "budget": "medium",
            "age": "25",
            "gender": "female"
        },
        "top_k": 3,
        "language": "en"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_summary_arabic():
    """Test Arabic language response"""
    print("\n=== Testing Summary Recommendation (Arabic) ===")
    
    payload = {
        "summary": {
            "skin_type": "dry",
            "problem": "hydration",
            "budget": "medium"
        },
        "top_k": 2,
        "language": "ar"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_summary_french():
    """Test French language response"""
    print("\n=== Testing Summary Recommendation (French) ===")
    
    payload = {
        "summary": {
            "hair_type": "dry",
            "problem": "damaged",
            "budget": "high"
        },
        "top_k": 2,
        "language": "fr"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_complex_summary():
    """Test complex summary with multiple criteria"""
    print("\n=== Testing Complex Summary ===")
    
    payload = {
        "summary": {
            "skin_type": "combination",
            "problem": "anti_aging",
            "category": "skin_care",
            "product_type": "serum",
            "budget": "medium",
            "age": "35",
            "gender": "female",
            "concerns": ["wrinkles", "hydration", "brightening"]
        },
        "top_k": 3,
        "language": "en"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_hair_care():
    """Test hair care recommendations"""
    print("\n=== Testing Hair Care Recommendation ===")
    
    payload = {
        "summary": {
            "hair_type": "curly",
            "problem": "frizz",
            "budget": "medium"
        },
        "top_k": 3,
        "language": "en"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_minimal_summary():
    """Test with minimal summary"""
    print("\n=== Testing Minimal Summary ===")
    
    payload = {
        "summary": {
            "problem": "acne"
        },
        "top_k": 2,
        "language": "en"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_empty_summary():
    """Test with empty summary (should still return results)"""
    print("\n=== Testing Empty Summary ===")
    
    payload = {
        "summary": {},
        "top_k": 3,
        "language": "en"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    response = requests.post(f"{BASE_URL}/recommend/summary", json=payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_stats():
    """Test stats endpoint"""
    print("\n=== Testing Stats Endpoint ===")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_beauty_products():
    """Test beauty products endpoint"""
    print("\n=== Testing Beauty Products Endpoint ===")
    response = requests.get(f"{BASE_URL}/beauty/products")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        products = response.json()
        print(f"Total products: {len(products)}")
        if products:
            print(f"First product: {json.dumps(products[0], indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("=" * 60)
    print("Beauty Recommendation API Test Suite")
    print("=" * 60)
    
    try:
        # Test health first
        test_health()
        
        # Test stats
        test_stats()
        
        # Test beauty products
        test_beauty_products()
        
        # Test various summary scenarios
        test_summary_recommendation()
        test_summary_arabic()
        test_summary_french()
        test_complex_summary()
        test_hair_care()
        test_minimal_summary()
        test_empty_summary()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Please make sure the server is running with: uvicorn app:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
