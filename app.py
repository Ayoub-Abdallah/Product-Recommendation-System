from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from models.intelligent_recommender import IntelligentRecommender
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional, List, Dict, Any
import json
import os
from datetime import datetime

app = FastAPI(title="Intelligent Multi-Category Recommendation System", version="3.0")

# Load intelligent recommender
products_catalog_path = 'data/products_catalog.json'
if os.path.exists(products_catalog_path):
    recommender = IntelligentRecommender(products_catalog_path)
    print(f"✅ Intelligent recommender loaded with {len(recommender.products)} products")
else:
    raise FileNotFoundError(f"❌ Products catalog not found at {products_catalog_path}")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class RecommendRequest(BaseModel):
    """Request model for intelligent multi-category recommendations"""
    category: Optional[str] = Field(None, description="Product category: beauty_skincare, health_supplements, sportswear, baby_care, maternal_health, healthcare_devices")
    needs: Optional[List[str]] = Field(None, description="What user needs: energy, immunity, comfort, hydration, etc.")
    skin_conditions: Optional[List[str]] = Field(None, description="Skin conditions: dry, sensitive, oily, eczema_prone, combination, etc.")
    medical_conditions: Optional[List[str]] = Field(None, description="Medical conditions: diabetes, anemia, hypertension, pregnancy, eczema, etc.")
    avoid: Optional[List[str]] = Field(None, description="Things to avoid: sugar, fragrance, allergens, etc.")
    budget: Optional[Any] = Field(None, description="Budget: numeric (5000) or categorical (low/medium/high)")
    age: Optional[str] = Field(None, description="Age: newborn, 0-6months, 25, 40+, etc.")
    preferences: Optional[List[str]] = Field(None, description="Preferences: organic, fragrance_free, vegan, hypoallergenic, etc.")
    query: Optional[str] = Field(None, description="Natural language query: 'I need vitamins but I'm diabetic and have anemia'")
    top_k: Optional[int] = Field(default=5, ge=1, le=10, description="Number of recommendations (1-10)")
    language: Optional[str] = Field(default='en', description="Response language: en, ar, fr")

@app.post('/recommend')
def recommend(req: RecommendRequest):
    """
    Intelligent multi-category product recommendation endpoint
    
    Handles complex user situations across multiple categories:
    - Beauty & Skincare
    - Health Supplements
    - Sportswear
    - Baby Care
    - Maternal Health
    - Healthcare Devices
    
    Examples of complex situations:
    1. "I have diabetes and anemia, need vitamins without sugar"
    2. "Dry but sensitive skin, looking for fragrance-free moisturizer"
    3. "Need running shoes for diabetic feet with neuropathy"
    4. "Baby lotion for eczema-prone sensitive skin"
    5. "Pregnant with gestational diabetes, need prenatal vitamins"
    
    Request body examples:
    
    Example 1 - Health supplements for diabetic with anemia:
    {
        "category": "health_supplements",
        "medical_conditions": ["diabetes", "anemia"],
        "needs": ["energy", "immunity"],
        "avoid": ["sugar"],
        "budget": 5000,
        "top_k": 3
    }
    
    Example 2 - Skincare for dry, sensitive skin:
    {
        "category": "beauty_skincare",
        "skin_conditions": ["dry", "sensitive"],
        "avoid": ["fragrance"],
        "preferences": ["hypoallergenic"],
        "budget": "medium",
        "top_k": 3
    }
    
    Example 3 - Natural language query:
    {
        "query": "I need vitamins but I'm diabetic and have anemia, no sugar please",
        "top_k": 5
    }
    
    Example 4 - Baby care for eczema:
    {
        "category": "baby_care",
        "skin_conditions": ["eczema_prone", "sensitive"],
        "age": "newborn",
        "preferences": ["organic", "fragrance_free"],
        "top_k": 3
    }
    
    Response format:
    {
        "recommendations": [
            {
                "id": "supp-001",
                "name": "Sugar-Free Multivitamin for Diabetics",
                "price": 3500,
                "currency": "DA",
                "category": "health_supplements",
                "subcategory": "multivitamins",
                "tags": ["sugar_free", "diabetic_friendly", "iron"],
                "description": "Complete multivitamin formulated for diabetics...",
                "reason": "✅ Safe for diabetes, anemia • 💊 Beneficial for anemia • ⭐ Features: sugar_free",
                "score": 1.245,
                "stock": 80,
                "safety_notes": ["⚕️ Consult doctor if on blood thinners"]
            }
        ],
        "count": 3,
        "metadata": {
            "warnings": [
                {
                    "type": "medical_consultation",
                    "severity": "medium",
                    "product": "Product Name",
                    "message": "⚕️ Consult doctor: kidney_disease"
                }
            ],
            "safety_info": [],
            "constraints_applied": ["medical_safety", "ingredient_avoidance", "budget"],
            "filtered_out": {
                "medical_safety": 2,
                "skin_incompatibility": 0,
                "budget": 1,
                "out_of_stock": 0,
                "category_mismatch": 5
            }
        },
        "language": "en"
    }
    """
    # Log the incoming request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*80)
    print(f"📥 INCOMING API CALL - {timestamp}")
    print("="*80)
    print(f"Endpoint: POST /recommend")
    print(f"Request Data:")
    print(f"  - Category: {req.category}")
    print(f"  - Needs: {req.needs}")
    print(f"  - Skin Conditions: {req.skin_conditions}")
    print(f"  - Medical Conditions: {req.medical_conditions}")
    print(f"  - Avoid: {req.avoid}")
    print(f"  - Budget: {req.budget}")
    print(f"  - Age: {req.age}")
    print(f"  - Preferences: {req.preferences}")
    print(f"  - Query: {req.query}")
    print(f"  - Top K: {req.top_k}")
    print(f"  - Language: {req.language}")
    print("="*80)
    
    try:
        # Build user request dict
        user_request = {}
        if req.category:
            user_request['category'] = req.category
        if req.needs:
            user_request['needs'] = req.needs
        if req.skin_conditions:
            user_request['skin_conditions'] = req.skin_conditions
        if req.medical_conditions:
            user_request['medical_conditions'] = req.medical_conditions
        if req.avoid:
            user_request['avoid'] = req.avoid
        if req.budget is not None:
            user_request['budget'] = req.budget
        if req.age:
            user_request['age'] = req.age
        if req.preferences:
            user_request['preferences'] = req.preferences
        if req.query:
            user_request['query'] = req.query
        
        # Get recommendations
        result = recommender.recommend(
            user_request=user_request,
            top_k=req.top_k,
            language=req.language
        )
        
        # Log the response
        print(f"\n✅ RESPONSE: {result['count']} recommendations returned")
        print("="*80 + "\n")
        
        # Return result (already includes recommendations, count, metadata, language)
        return result
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*80 + "\n")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating recommendations: {str(e)}"
        )

@app.get('/products')
def get_products():
    """Get all products in catalog"""
    return recommender.products

@app.get('/product/search/{search_term}')
def search_products_by_name(search_term: str):
    """
    Search for products by name (partial match, case-insensitive)
    
    Args:
        search_term: Product name or partial name to search
    
    Returns:
        List of matching products
        
    Example:
        GET /product/search/vitamin
        
    Response:
        {
            "success": true,
            "count": 2,
            "search_term": "vitamin",
            "products": [...]
        }
    """
    # Log the incoming request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*80)
    print(f"📥 INCOMING API CALL - {timestamp}")
    print("="*80)
    print(f"Endpoint: GET /product/search/{search_term}")
    print(f"Search Term: {search_term}")
    print("="*80)
    
    try:
        search_lower = search_term.lower()
        
        # Search in multiple fields
        matching_products = []
        for p in recommender.products:
            # Check name (all languages)
            if (search_lower in p.get('name', '').lower() or
                search_lower in p.get('name_ar', '').lower() or
                search_lower in p.get('name_fr', '').lower() or
                # Check description
                search_lower in p.get('description', '').lower() or
                # Check tags
                any(search_lower in tag.lower() for tag in p.get('tags', [])) or
                # Check category
                search_lower in p.get('category', '').lower() or
                search_lower in p.get('subcategory', '').lower()):
                matching_products.append(p)
        
        if not matching_products:
            print(f"\n⚠️  RESPONSE: No products found matching '{search_term}'")
            print("="*80 + "\n")
            return {
                "success": False,
                "message": f"No products found matching '{search_term}'",
                "search_term": search_term,
                "count": 0,
                "products": []
            }
        
        print(f"\n✅ RESPONSE: {len(matching_products)} products found matching '{search_term}'")
        print("="*80 + "\n")
        return {
            "success": True,
            "search_term": search_term,
            "count": len(matching_products),
            "products": matching_products
        }
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*80 + "\n")
        raise HTTPException(
            status_code=500, 
            detail=f"Error searching products: {str(e)}"
        )

@app.get('/product/{product_id}')
def get_product_by_id(product_id: str):
    """
    Get a specific product by its ID
    
    Args:
        product_id: The unique product ID to lookup
    
    Returns:
        Product details with full information
        
    Example:
        GET /product/supp-001
        
    Response:
        {
            "success": true,
            "product": {
                "id": "supp-001",
                "name": "Sugar-Free Multivitamin for Diabetics",
                "price": 3500,
                "currency": "DA",
                ...
            }
        }
    """
    # Log the incoming request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*80)
    print(f"📥 INCOMING API CALL - {timestamp}")
    print("="*80)
    print(f"Endpoint: GET /product/{product_id}")
    print(f"Product ID: {product_id}")
    print("="*80)
    
    try:
        # Search for product by ID (case-insensitive)
        product = next(
            (p for p in recommender.products if p.get('id', '').lower() == product_id.lower()), 
            None
        )
        
        if not product:
            print(f"\n⚠️  RESPONSE: Product with ID '{product_id}' not found (404)")
            print("="*80 + "\n")
            raise HTTPException(
                status_code=404, 
                detail=f"Product with ID '{product_id}' not found"
            )
        
        print(f"\n✅ RESPONSE: Product '{product.get('name', 'N/A')}' found")
        print("="*80 + "\n")
        return {
            "success": True,
            "product": product
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*80 + "\n")
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching product: {str(e)}"
        )

@app.get('/categories')
def get_categories():
    """Get all available categories and subcategories"""
    categories = {}
    for product in recommender.products:
        cat = product.get('category')
        subcat = product.get('subcategory')
        if cat:
            if cat not in categories:
                categories[cat] = set()
            if subcat:
                categories[cat].add(subcat)
    
    # Convert sets to lists for JSON serialization
    return {k: sorted(list(v)) for k, v in categories.items()}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Serve web UI"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/stats")
def get_stats():
    """Get system statistics"""
    return recommender.get_stats()

@app.get('/health')
def health_check():
    """Health check endpoint"""
    stats = recommender.get_stats()
    return {
        "status": "healthy",
        "service": "Intelligent Multi-Category Recommendation System",
        "version": "3.0",
        "products_loaded": stats['total_products'],
        "categories": len(stats['categories']),
        "categories_list": list(stats['categories'].keys())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4708)
