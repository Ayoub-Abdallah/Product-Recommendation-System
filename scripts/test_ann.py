#!/usr/bin/env python3
"""
Test the ANN-based recommendation system
"""
import sys
import json
import time

# Add parent directory to path
sys.path.insert(0, '/home/ayoub/hind_smart_agent_system/system/recommendation system')

from models.recommender import Recommender

def test_ann_system():
    print("=" * 70)
    print("🚀 Testing ANN-Based Recommendation System")
    print("=" * 70)
    
    # Initialize recommender
    print("\n📦 Loading products and building FAISS index...")
    start = time.time()
    recommender = Recommender('data/products.json')
    load_time = time.time() - start
    print(f"⏱️  Loaded in {load_time:.2f} seconds")
    
    # Get stats
    print("\n📊 System Statistics:")
    stats = recommender.get_stats()
    for key, value in stats.items():
        if key == 'categories':
            print(f"  Categories ({len(value)}):")
            for cat, count in sorted(value.items()):
                print(f"    - {cat}: {count} products")
        else:
            print(f"  {key}: {value}")
    
    # Test queries
    test_queries = [
        ("I need running shoes for marathon training", "Sportswear"),
        ("Looking for wireless earbuds for gym", "Electronics"),
        ("Want a yoga mat for home workouts", "Fitness"),
        ("Need a blender for smoothies", "Home & Kitchen"),
        ("Looking for outdoor camping gear", "Outdoor"),
    ]
    
    print("\n" + "=" * 70)
    print("🔍 Testing Recommendations")
    print("=" * 70)
    
    for query, category in test_queries:
        print(f"\n📝 Query: \"{query}\"")
        if category:
            print(f"   Category: {category}")
        
        start = time.time()
        results = recommender.recommend(query, category=category, top_k=5)
        query_time = (time.time() - start) * 1000  # Convert to ms
        
        print(f"⏱️  Search time: {query_time:.2f}ms")
        print(f"📋 Top {len(results)} Results:")
        
        for i, rec in enumerate(results, 1):
            print(f"   {i}. {rec['title']}")
            print(f"      Category: {rec['category']} | Price: ${rec['price']:.2f}")
            print(f"      Similarity: {rec['similarity']:.3f} | Score: {rec['score']:.3f}")
            print(f"      Reason: {rec['reason']}")
        
        if not results:
            print("   ⚠️  No results found")
    
    # Performance test
    print("\n" + "=" * 70)
    print("⚡ Performance Benchmark")
    print("=" * 70)
    
    num_queries = 100
    print(f"\nRunning {num_queries} random queries...")
    
    queries = [
        "wireless headphones", "running shoes", "yoga mat", "kitchen blender",
        "camping tent", "pet toys", "workout clothes", "fitness tracker",
        "cooking pot", "outdoor backpack"
    ] * 10
    
    start = time.time()
    for q in queries:
        recommender.recommend(q, top_k=5)
    total_time = time.time() - start
    
    avg_time = (total_time / num_queries) * 1000
    print(f"✅ Average query time: {avg_time:.2f}ms")
    print(f"   Total time for {num_queries} queries: {total_time:.2f}s")
    print(f"   Throughput: {num_queries/total_time:.2f} queries/second")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)

if __name__ == "__main__":
    test_ann_system()
