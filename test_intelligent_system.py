#!/usr/bin/env python3
"""
Test the intelligent recommendation system with complex scenarios
"""

import requests
import json

BASE_URL = "http://localhost:4708"

def print_separator(title=""):
    print("\n" + "="*80)
    if title:
        print(f"  {title}")
        print("="*80)

def test_scenario(title, request_data):
    """Test a specific scenario"""
    print_separator(title)
    print(f"\n📝 Request:")
    print(json.dumps(request_data, indent=2))
    print()
    
    response = requests.post(f"{BASE_URL}/recommend", json=request_data)
    
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
            
            if product.get('safety_notes'):
                print(f"   ⚕️  Safety: {', '.join(product['safety_notes'])}")
            print()
        
        # Show metadata
        metadata = data.get('metadata', {})
        if metadata.get('warnings'):
            print("⚠️  WARNINGS:")
            for warning in metadata['warnings']:
                print(f"   - [{warning['severity'].upper()}] {warning['message']}")
            print()
        
        if metadata.get('constraints_applied'):
            print(f"🔒 Constraints Applied: {', '.join(metadata['constraints_applied'])}")
        
        if metadata.get('filtered_out'):
            filtered = metadata['filtered_out']
            total_filtered = sum(filtered.values())
            if total_filtered > 0:
                print(f"🚫 Filtered Out: {total_filtered} products")
                for reason, count in filtered.items():
                    if count > 0:
                        print(f"   - {reason}: {count}")
        print()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def main():
    print("\n" + "🌟 INTELLIGENT MULTI-CATEGORY RECOMMENDATION SYSTEM TEST" + "\n")
    
    # Scenario 1: Diabetic with Anemia needing vitamins
    test_scenario(
        "SCENARIO 1: Diabetic with Anemia - No Sugar",
        {
            "category": "health_supplements",
            "medical_conditions": ["diabetes", "anemia"],
            "needs": ["energy", "immunity"],
            "avoid": ["sugar"],
            "budget": 5000,
            "top_k": 2
        }
    )
    
    # Scenario 2: Dry + Sensitive Skin
    test_scenario(
        "SCENARIO 2: Dry + Sensitive Skin - No Fragrance",
        {
            "category": "beauty_skincare",
            "skin_conditions": ["dry", "sensitive"],
            "avoid": ["fragrance"],
            "preferences": ["hypoallergenic"],
            "budget": "medium",
            "top_k": 2
        }
    )
    
    # Scenario 3: Baby with Eczema
    test_scenario(
        "SCENARIO 3: Baby with Eczema - Organic & Fragrance-Free",
        {
            "category": "baby_care",
            "skin_conditions": ["eczema_prone", "sensitive"],
            "age": "newborn",
            "preferences": ["organic", "fragrance_free"],
            "top_k": 2
        }
    )
    
    # Scenario 4: Diabetic needing athletic shoes
    test_scenario(
        "SCENARIO 4: Diabetic Needing Running Shoes",
        {
            "category": "sportswear",
            "medical_conditions": ["diabetes"],
            "needs": ["comfort", "support"],
            "budget": 10000,
            "top_k": 2
        }
    )
    
    # Scenario 5: Pregnant woman with gestational diabetes
    test_scenario(
        "SCENARIO 5: Pregnant with Gestational Diabetes",
        {
            "category": "maternal_health",
            "medical_conditions": ["pregnancy", "gestational_diabetes"],
            "needs": ["prenatal_vitamins"],
            "avoid": ["sugar"],
            "top_k": 2
        }
    )
    
    # Scenario 6: Natural Language Query
    test_scenario(
        "SCENARIO 6: Natural Language - 'I'm diabetic and anemic, need vitamins'",
        {
            "query": "I have diabetes and anemia, need vitamins without sugar",
            "top_k": 3
        }
    )
    
    print_separator("✅ ALL TESTS COMPLETED")
    print("\n💡 TIP: The system intelligently filters unsafe products and provides safety warnings\n")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API at", BASE_URL)
        print("💡 Make sure the server is running: ./venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 4708\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
