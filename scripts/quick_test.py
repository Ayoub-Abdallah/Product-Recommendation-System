#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/ayoub/hind_smart_agent_system/system/recommendation system')
from models.recommender import Recommender

r = Recommender('data/products.json')

queries = [
    'something to sit on',
    'I need a chair', 
    'wireless headphones',
    'blender for smoothies'
]

for query in queries:
    print(f'\n{"="*80}')
    print(f'📝 "{query}"')
    print("="*80)
    
    results = r.recommend(query, top_k=5)
    
    # Check categories
    categories = set(r['category'] for r in results)
    has_books = 'Books' in categories
    
    print(f'Categories: {categories}')
    if has_books:
        print('❌ WARNING: Books found!')
    else:
        print('✅ No books!')
    
    print(f'\nTop 5:')
    for i, rec in enumerate(results, 1):
        boost = rec.get('keyword_boost', 0)
        boost_icon = '🚀' if boost > 0 else '  '
        print(f'{boost_icon} {i}. {rec["title"]} - {rec["category"]} (Score: {rec["score"]:.3f}, Boost: +{boost:.2f})')
