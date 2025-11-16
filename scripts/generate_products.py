"""
Generate a large product catalog with diverse categories and realistic data
"""
import json
import random

# Product templates by category
CATEGORIES = {
    "Sportswear": {
        "prefixes": ["Running", "Training", "Athletic", "Performance", "Pro", "Elite", "Speed", "Comfort"],
        "items": ["Shoes", "Sneakers", "Trainers", "Runners", "Kicks"],
        "suffixes": ["Pro", "2.0", "Elite", "Max", "Plus", "X", "XT", "Ultra"],
        "features": ["lightweight", "breathable", "cushioned", "durable", "flexible", "supportive", "moisture-wicking", "ergonomic"]
    },
    "Fitness": {
        "prefixes": ["Yoga", "Pilates", "Exercise", "Workout", "Gym", "Training", "Fitness", "Premium"],
        "items": ["Mat", "Band", "Ball", "Roller", "Block", "Strap", "Towel", "Gloves"],
        "suffixes": ["Pro", "Deluxe", "Premium", "Plus", "Essential", "Advanced", "Basic"],
        "features": ["thick", "non-slip", "portable", "durable", "comfortable", "eco-friendly", "textured", "antimicrobial"]
    },
    "Electronics": {
        "prefixes": ["Wireless", "Bluetooth", "Smart", "Digital", "Portable", "Rechargeable", "USB-C", "Premium"],
        "items": ["Earbuds", "Headphones", "Speaker", "Charger", "Tracker", "Watch", "Camera", "Monitor"],
        "suffixes": ["Pro", "Max", "Plus", "Elite", "Air", "Ultra", "Mini", "2.0"],
        "features": ["noise-cancelling", "waterproof", "long-battery", "fast-charging", "high-fidelity", "touch-control", "voice-assistant", "wireless"]
    },
    "Home & Kitchen": {
        "prefixes": ["Stainless", "Non-stick", "Electric", "Digital", "Ceramic", "Glass", "Premium", "Professional"],
        "items": ["Blender", "Mixer", "Pan", "Pot", "Knife", "Cooker", "Kettle", "Toaster"],
        "suffixes": ["Pro", "Deluxe", "Plus", "Max", "Premium", "Elite", "Essential"],
        "features": ["dishwasher-safe", "energy-efficient", "easy-clean", "durable", "multi-functional", "compact", "programmable", "quick-heat"]
    },
    "Books": {
        "prefixes": ["The Art of", "Mastering", "Complete Guide to", "Introduction to", "Advanced", "Essential", "Modern", "Practical"],
        "items": ["Programming", "Cooking", "Photography", "Design", "Marketing", "Leadership", "Meditation", "Fitness"],
        "suffixes": ["Handbook", "Bible", "Manual", "Guide", "Essentials", "Masterclass", "101", "Workshop"],
        "features": ["comprehensive", "illustrated", "step-by-step", "beginner-friendly", "advanced-techniques", "updated-edition", "practical-examples", "expert-authored"]
    },
    "Clothing": {
        "prefixes": ["Cotton", "Lightweight", "Premium", "Casual", "Comfort", "Essential", "Classic", "Modern"],
        "items": ["T-Shirt", "Hoodie", "Jacket", "Pants", "Shorts", "Socks", "Hat", "Scarf"],
        "suffixes": ["Collection", "Series", "Edition", "Pack", "Set", "Bundle"],
        "features": ["breathable", "stretchy", "wrinkle-free", "quick-dry", "soft", "durable", "stylish", "comfortable"]
    },
    "Beauty": {
        "prefixes": ["Natural", "Organic", "Hydrating", "Anti-Aging", "Gentle", "Deep", "Nourishing", "Radiance"],
        "items": ["Serum", "Cream", "Lotion", "Mask", "Cleanser", "Toner", "Oil", "Balm"],
        "suffixes": ["Formula", "Complex", "Treatment", "System", "Therapy", "Care", "Boost"],
        "features": ["hypoallergenic", "fragrance-free", "paraben-free", "vegan", "cruelty-free", "dermatologist-tested", "fast-absorbing", "long-lasting"]
    },
    "Toys & Games": {
        "prefixes": ["Educational", "Interactive", "Creative", "Building", "Puzzle", "Strategy", "Adventure", "Family"],
        "items": ["Game", "Set", "Kit", "Blocks", "Board Game", "Puzzle", "Figure", "Playset"],
        "suffixes": ["Deluxe", "Collection", "Edition", "Pack", "Bundle", "Set"],
        "features": ["age-appropriate", "safe", "educational", "entertaining", "durable", "colorful", "engaging", "award-winning"]
    },
    "Outdoor": {
        "prefixes": ["Camping", "Hiking", "Backpacking", "Survival", "Portable", "Waterproof", "Lightweight", "Heavy-Duty"],
        "items": ["Tent", "Backpack", "Sleeping Bag", "Lantern", "Cooler", "Chair", "Hammock", "Knife"],
        "suffixes": ["Pro", "Elite", "Adventure", "Explorer", "Expedition", "Plus"],
        "features": ["waterproof", "lightweight", "durable", "compact", "weather-resistant", "easy-setup", "portable", "ventilated"]
    },
    "Pet Supplies": {
        "prefixes": ["Premium", "Natural", "Organic", "Interactive", "Comfortable", "Durable", "Healthy", "Smart"],
        "items": ["Food", "Toy", "Bed", "Collar", "Leash", "Bowl", "Carrier", "Grooming Kit"],
        "suffixes": ["Plus", "Premium", "Deluxe", "Pro", "Essential", "Advanced"],
        "features": ["veterinarian-approved", "non-toxic", "washable", "comfortable", "adjustable", "sturdy", "interactive", "nutritious"]
    }
}

def generate_product(product_id, category, templates):
    """Generate a single product with realistic data"""
    prefix = random.choice(templates["prefixes"])
    item = random.choice(templates["items"])
    suffix = random.choice(templates["suffixes"])
    
    title = f"{prefix} {item} {suffix}"
    
    # Generate description
    features = random.sample(templates["features"], k=random.randint(2, 4))
    description = f"{random.choice(['Perfect for', 'Ideal for', 'Great for', 'Designed for', 'Best for'])} "
    description += f"{random.choice(['daily use', 'professionals', 'beginners', 'enthusiasts', 'everyone'])}. "
    description += f"Features: {', '.join(features)}."
    
    # Generate realistic metrics
    popularity = round(random.uniform(0.3, 1.0), 2)
    stock = random.randint(0, 50)
    recency = round(random.uniform(0.1, 1.0), 2)
    personal = round(random.uniform(0.0, 0.5), 2)
    seller_boost = round(random.uniform(0.0, 0.25), 2)
    
    # Price based on category
    price_ranges = {
        "Sportswear": (50, 200),
        "Fitness": (20, 150),
        "Electronics": (80, 500),
        "Home & Kitchen": (30, 300),
        "Books": (15, 60),
        "Clothing": (20, 120),
        "Beauty": (25, 150),
        "Toys & Games": (15, 100),
        "Outdoor": (40, 400),
        "Pet Supplies": (10, 100)
    }
    
    price = round(random.uniform(*price_ranges.get(category, (20, 200))), 2)
    
    return {
        "id": product_id,
        "title": title,
        "description": description,
        "category": category,
        "price": price,
        "popularity": popularity,
        "stock": stock,
        "recency": recency,
        "personal": personal,
        "seller_boost": seller_boost
    }

def generate_product_catalog(num_products=1000):
    """Generate a large product catalog"""
    products = []
    product_id = 1
    
    # Distribute products across categories
    categories = list(CATEGORIES.keys())
    products_per_category = num_products // len(categories)
    
    for category in categories:
        templates = CATEGORIES[category]
        for _ in range(products_per_category):
            products.append(generate_product(product_id, category, templates))
            product_id += 1
    
    # Fill remaining slots
    while len(products) < num_products:
        category = random.choice(categories)
        templates = CATEGORIES[category]
        products.append(generate_product(product_id, category, templates))
        product_id += 1
    
    return products

if __name__ == "__main__":
    print("Generating product catalog...")
    products = generate_product_catalog(1000)
    
    # Save to file
    with open('data/products.json', 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"✅ Generated {len(products)} products")
    
    # Print statistics
    from collections import Counter
    category_counts = Counter(p['category'] for p in products)
    print("\nProducts by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")
    
    in_stock = sum(1 for p in products if p['stock'] > 0)
    print(f"\nIn stock: {in_stock}/{len(products)} ({in_stock/len(products)*100:.1f}%)")
    
    avg_price = sum(p['price'] for p in products) / len(products)
    print(f"Average price: ${avg_price:.2f}")
