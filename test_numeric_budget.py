#!/usr/bin/env python3
"""
Test script for numeric budget handling in the recommendation API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_numeric_budget():
    """Test recommendations with numeric budget"""
    print("\n" + "="*60)
    print("Testing Numeric Budget Support")
    print("="*60)
    
    test_cases = [
        {
            "name": "Exact Budget - 2500 DA",
            "summary": {
                "skin_type": "oily",
                "problem": "acne",
                "budget": 2500
            }
        },
        {
            "name": "Budget with String - '3000 DA'",
            "summary": {
                "skin_type": "dry",
                "problem": "hydration",
                "budget": "3000 DA"
            }
        },
        {
            "name": "Low Budget - 1500 DA",
            "summary": {
                "hair_type": "dry",
                "problem": "damaged",
                "budget": 1500
            }
        },
        {
            "name": "High Budget - 5000 DA",
            "summary": {
                "skin_type": "normal",
                "problem": "anti_aging",
                "budget": 5000
            }
        },
        {
            "name": "Budget Range - 'around 2800 DA'",
            "summary": {
                "skin_type": "combination",
                "budget": "around 2800 DA"
            }
        },
        {
            "name": "Categorical Budget - 'low'",
            "summary": {
                "problem": "acne",
                "budget": "low"
            }
        },
        {
            "name": "Categorical Budget - 'medium'",
            "summary": {
                "problem": "hydration",
                "budget": "medium"
            }
        },
        {
            "name": "Categorical Budget - 'high'",
            "summary": {
                "problem": "anti_aging",
                "budget": "high"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {i}/{len(test_cases)}] {test_case['name']}")
        print(f"Summary: {json.dumps(test_case['summary'], indent=2)}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/recommend/summary",
                json={
                    "summary": test_case['summary'],
                    "top_k": 3,
                    "language": "en"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                recommendations = result.get('recommendations', [])
                
                print(f"\n✅ Found {len(recommendations)} recommendations:")
                for j, product in enumerate(recommendations, 1):
                    print(f"\n  {j}. {product['name']}")
                    print(f"     Price: {product['price']} {product['currency']}")
                    print(f"     Score: {product['score']}")
                    print(f"     Reason: {product['reason']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"   {response.json()}")
        
        except requests.exceptions.ConnectionError:
            print("❌ Server not running. Start with: ./start_server.sh")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
        
        if i < len(test_cases):
            input("\nPress Enter to continue...")

def test_budget_comparison():
    """Compare different budget approaches"""
    print("\n" + "="*60)
    print("Budget Comparison Test")
    print("="*60)
    
    base_summary = {
        "skin_type": "oily",
        "problem": "acne"
    }
    
    budgets = [
        ("No Budget", {}),
        ("Numeric: 2000", {"budget": 2000}),
        ("Numeric: 2500", {"budget": 2500}),
        ("Numeric: 3000", {"budget": 3000}),
        ("Numeric: 4000", {"budget": 4000}),
        ("Category: low", {"budget": "low"}),
        ("Category: medium", {"budget": "medium"}),
        ("Category: high", {"budget": "high"}),
    ]
    
    print("\nComparing recommendations for same skin type/problem with different budgets:\n")
    
    for budget_name, budget_dict in budgets:
        summary = {**base_summary, **budget_dict}
        
        try:
            response = requests.post(
                f"{BASE_URL}/recommend/summary",
                json={"summary": summary, "top_k": 3, "language": "en"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                recommendations = result.get('recommendations', [])
                
                print(f"{budget_name:20} → ", end="")
                if recommendations:
                    prices = [f"{p['price']} DA" for p in recommendations[:3]]
                    print(f"{len(recommendations)} products: {', '.join(prices)}")
                else:
                    print("No recommendations")
            else:
                print(f"{budget_name:20} → Error {response.status_code}")
        
        except Exception as e:
            print(f"{budget_name:20} → Error: {e}")
            return

def test_arabic_with_budget():
    """Test Arabic responses with budget info"""
    print("\n" + "="*60)
    print("Arabic Response with Budget")
    print("="*60)
    
    summary = {
        "skin_type": "dry",
        "problem": "hydration",
        "budget": 2500
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/recommend/summary",
            json={"summary": summary, "top_k": 3, "language": "ar"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result.get('recommendations', [])
            
            print(f"\nوجدت {len(recommendations)} منتجات:\n")
            for i, product in enumerate(recommendations, 1):
                print(f"{i}. {product['name']}")
                print(f"   السعر: {product['price']} {product['currency']}")
                print(f"   السبب: {product['reason']}\n")
        else:
            print(f"❌ خطأ: {response.status_code}")
    
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    print("="*60)
    print("Numeric Budget Feature Test Suite")
    print("="*60)
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ Server is not healthy")
            exit(1)
        
        print("\n✅ Server is running\n")
        
        while True:
            print("\nChoose a test:")
            print("  1. Test numeric budget support")
            print("  2. Budget comparison (numeric vs categorical)")
            print("  3. Arabic response with budget")
            print("  4. Run all tests")
            print("  5. Exit")
            
            choice = input("\nYour choice (1-5): ").strip()
            
            if choice == '1':
                test_numeric_budget()
            elif choice == '2':
                test_budget_comparison()
            elif choice == '3':
                test_arabic_with_budget()
            elif choice == '4':
                test_numeric_budget()
                input("\nPress Enter to continue to next test...")
                test_budget_comparison()
                input("\nPress Enter to continue to next test...")
                test_arabic_with_budget()
            elif choice == '5':
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server")
        print("   Please start the server with: ./start_server.sh")
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
