#!/usr/bin/env python3
"""
Test improved keyword matching and category filtering
"""
import sys
sys.path.insert(0, '/home/ayoub/hind_smart_agent_system/system/recommendation system')

from models.recommender import Recommender

def test_keyword_accuracy():
    print("=" * 80)
    print("🧪 Testing Improved Keyword Matching & Category Filtering")
    print("=" * 80)
    
    recommender = Recommender('data/products.json')
    
    # Test cases that should NOT return books
    test_queries = [
        {
            'query': 'something to sit on',
            'expected_categories': ['Outdoor', 'Furniture'],
            'avoid_categories': ['Books'],
            'keywords': ['chair', 'seat', 'bench']
        },
        {
            'query': 'I need a chair',
            'expected_categories': ['Outdoor', 'Furniture'],
            'avoid_categories': ['Books'],
            'keywords': ['chair']
        },
        {
            'query': 'outdoor seating',
            'expected_categories': ['Outdoor'],
            'avoid_categories': ['Books', 'Electronics'],
            'keywords': ['chair', 'seat']
        },
        {
            'query': 'wireless headphones for gym',
            'expected_categories': ['Electronics'],
            'avoid_categories': ['Books', 'Outdoor'],
            'keywords': ['headphones', 'wireless']
        },
        {
            'query': 'running shoes for marathon',
            'expected_categories': ['Sportswear'],
            'avoid_categories': ['Books', 'Electronics'],
            'keywords': ['shoes', 'running']
        },
        {
            'query': 'kitchen blender',
            'expected_categories': ['Home & Kitchen'],
            'avoid_categories': ['Books', 'Outdoor'],
            'keywords': ['blender']
        }
    ]
    
    for test in test_queries:
        print("\n" + "─" * 80)
        print(f"📝 Query: \"{test['query']}\"")
        print(f"   Expected: {', '.join(test['expected_categories'])}")
        print(f"   Should avoid: {', '.join(test['avoid_categories'])}")
        
        results = recommender.recommend(test['query'], top_k=5)
        
        print(f"\n   📋 Top 5 Results:")
        
        # Check results
        categories_found = []
        avoided_found = []
        
        for i, rec in enumerate(results, 1):
            print(f"   {i}. {rec['title']}")
            print(f"      Category: {rec['category']} | Price: ${rec['price']:.2f}")
            print(f"      Similarity: {rec['similarity']:.3f} | Boosted: {rec.get('enhanced_similarity', rec['similarity']):.3f} | Score: {rec['score']:.3f}")
            print(f"      Keyword Boost: +{rec.get('keyword_boost', 0):.3f}")
            print(f"      Reason: {rec['reason']}")
            
            categories_found.append(rec['category'])
            if rec['category'] in test['avoid_categories']:
                avoided_found.append(rec['category'])
        
        # Validation
        print(f"\n   ✅ Validation:")
        
        has_expected = any(cat in categories_found for cat in test['expected_categories'])
        has_avoided = len(avoided_found) > 0
        
        if has_expected:
            print(f"      ✓ Found expected categories: {set(cat for cat in categories_found if cat in test['expected_categories'])}")
        else:
            print(f"      ✗ Missing expected categories!")
        
        if has_avoided:
            print(f"      ✗ Found unwanted categories: {set(avoided_found)} ❌")
        else:
            print(f"      ✓ No unwanted categories (Books, etc.) ✅")
        
        # Count chair products if looking for seating
        if 'chair' in test['keywords'] or 'seat' in test['keywords']:
            chair_count = sum(1 for r in results if 'chair' in r['title'].lower() or 'seat' in r['title'].lower())
            print(f"      ✓ Found {chair_count}/5 chair/seating products")
    
    # Special test: Count total chairs in catalog
    print("\n" + "=" * 80)
    print("📊 Catalog Analysis")
    print("=" * 80)
    
    all_products = recommender.get_products()
    
    # Count chairs
    chairs = [p for p in all_products if 'chair' in p['title'].lower() or 'seat' in p['title'].lower() or 'bench' in p['title'].lower() or 'stool' in p['title'].lower()]
    books = [p for p in all_products if p['category'] == 'Books']
    
    print(f"\nTotal products: {len(all_products)}")
    print(f"Chair/Seating products: {len(chairs)}")
    print(f"  Categories: {set(p['category'] for p in chairs)}")
    
    print(f"\nBooks: {len(books)}")
    
    print(f"\n📌 Sample chairs:")
    for chair in chairs[:10]:
        print(f"  - {chair['title']} ({chair['category']})")
    
    print("\n" + "=" * 80)
    print("✅ Test Complete!")
    print("=" * 80)

if __name__ == "__main__":
    test_keyword_accuracy()
