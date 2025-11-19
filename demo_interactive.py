#!/usr/bin/env python3
"""
Interactive Demo for Beauty Recommendation API

This script provides an interactive CLI to test the recommendation system.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "=" * 60)
    print(text.center(60))
    print("=" * 60)

def print_product(product: Dict[str, Any], index: int):
    """Pretty print a product recommendation"""
    print(f"\n{index}. {product['name']}")
    print(f"   ID: {product['id']}")
    print(f"   Price: {product['price']} {product['currency']}")
    print(f"   Category: {product['category']} > {product.get('subcategory', 'N/A')}")
    print(f"   Tags: {', '.join(product.get('tags', []))}")
    print(f"   Description: {product['description']}")
    print(f"   🎯 Reason: {product['reason']}")
    print(f"   Score: {product['score']}")

def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            health = response.json()
            print("✅ Server is running")
            print(f"   Services: {health['services']}")
            return True
        else:
            print("❌ Server responded with error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        print("   Please start the server with: uvicorn app:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_user_input():
    """Get recommendation criteria from user"""
    print("\n📝 Enter recommendation criteria (press Enter to skip):")
    
    summary = {}
    
    # Skin type
    print("\nSkin Type (oily/dry/combination/normal/sensitive):")
    skin_type = input("  > ").strip().lower()
    if skin_type:
        summary['skin_type'] = skin_type
    
    # Hair type
    print("\nHair Type (oily/dry/normal/curly/straight/wavy):")
    hair_type = input("  > ").strip().lower()
    if hair_type:
        summary['hair_type'] = hair_type
    
    # Problem
    print("\nMain Problem (acne/wrinkles/dryness/frizz/dark_spots/etc):")
    problem = input("  > ").strip().lower()
    if problem:
        summary['problem'] = problem
    
    # Category
    print("\nCategory (skin_care/hair_care/makeup):")
    category = input("  > ").strip().lower()
    if category:
        summary['category'] = category
    
    # Budget
    print("\nBudget (low/medium/high):")
    budget = input("  > ").strip().lower()
    if budget:
        summary['budget'] = budget
    
    # Age
    print("\nAge (e.g., 25, 30-40, 40+):")
    age = input("  > ").strip()
    if age:
        summary['age'] = age
    
    # Gender
    print("\nGender (female/male/unisex):")
    gender = input("  > ").strip().lower()
    if gender:
        summary['gender'] = gender
    
    # Language
    print("\nResponse Language (en/ar/fr):")
    language = input("  > ").strip().lower() or 'en'
    
    # Top K
    print("\nNumber of recommendations (1-5):")
    top_k_input = input("  > ").strip() or '3'
    try:
        top_k = int(top_k_input)
        top_k = max(1, min(5, top_k))  # Clamp between 1-5
    except:
        top_k = 3
    
    return summary, language, top_k

def get_recommendations(summary: Dict, language: str, top_k: int):
    """Get recommendations from API"""
    payload = {
        "summary": summary,
        "language": language,
        "top_k": top_k
    }
    
    print("\n📡 Sending request to API...")
    print(f"Summary: {json.dumps(summary, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/recommend/summary",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.json().get('detail', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def demo_preset(name: str, summary: Dict, language: str = 'en'):
    """Run a preset demo"""
    print(f"\n🎬 Running preset: {name}")
    print(f"   Summary: {json.dumps(summary, indent=2)}")
    
    result = get_recommendations(summary, language, 3)
    if result:
        display_results(result)

def display_results(result: Dict):
    """Display recommendation results"""
    recommendations = result.get('recommendations', [])
    count = result.get('count', 0)
    language = result.get('language', 'en')
    
    if count == 0:
        print("\n❌ No recommendations found")
        print(f"   {result.get('message', 'No matching products')}")
        return
    
    print_header(f"Found {count} Recommendation(s)")
    print(f"Language: {language.upper()}")
    
    for i, product in enumerate(recommendations, 1):
        print_product(product, i)

def interactive_mode():
    """Interactive mode - get input from user"""
    while True:
        print_header("Interactive Recommendation Mode")
        summary, language, top_k = get_user_input()
        
        if not summary:
            print("\n⚠️  No criteria entered. Exiting interactive mode.")
            break
        
        result = get_recommendations(summary, language, top_k)
        if result:
            display_results(result)
        
        print("\n" + "-" * 60)
        again = input("\nTry another search? (y/n): ").strip().lower()
        if again != 'y':
            break

def preset_demos():
    """Run preset demonstrations"""
    print_header("Preset Demonstrations")
    
    demos = [
        {
            "name": "Oily Skin with Acne (English)",
            "summary": {"skin_type": "oily", "problem": "acne", "budget": "medium"},
            "language": "en"
        },
        {
            "name": "Dry Skin Hydration (Arabic)",
            "summary": {"skin_type": "dry", "problem": "hydration"},
            "language": "ar"
        },
        {
            "name": "Curly Hair Frizz (French)",
            "summary": {"hair_type": "curly", "problem": "frizz"},
            "language": "fr"
        },
        {
            "name": "Anti-Aging Serum",
            "summary": {"problem": "wrinkles", "product_type": "serum", "age": "40"},
            "language": "en"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n[{i}/{len(demos)}]")
        demo_preset(demo['name'], demo['summary'], demo['language'])
        
        if i < len(demos):
            input("\nPress Enter to continue to next demo...")

def main():
    """Main function"""
    print_header("Beauty Recommendation API - Interactive Demo")
    
    # Check server
    if not check_server():
        return
    
    while True:
        print("\n" + "-" * 60)
        print("Choose an option:")
        print("  1. Interactive mode (enter your criteria)")
        print("  2. Run preset demos")
        print("  3. View system stats")
        print("  4. Exit")
        print("-" * 60)
        
        choice = input("\nYour choice (1-4): ").strip()
        
        if choice == '1':
            interactive_mode()
        elif choice == '2':
            preset_demos()
        elif choice == '3':
            response = requests.get(f"{BASE_URL}/stats")
            if response.status_code == 200:
                print("\n📊 System Statistics:")
                print(json.dumps(response.json(), indent=2))
            else:
                print("❌ Failed to get stats")
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
