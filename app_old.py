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
    category: Optional[str] = Field(None, description="Product category: beauty_skincare, health_supplements, sportswear, baby_care, etc.")
    needs: Optional[List[str]] = Field(None, description="What user needs: energy, immunity, comfort, etc.")
    skin_conditions: Optional[List[str]] = Field(None, description="Skin conditions: dry, sensitive, oily, eczema_prone, etc.")
    medical_conditions: Optional[List[str]] = Field(None, description="Medical conditions: diabetes, anemia, hypertension, pregnancy, etc.")
    avoid: Optional[List[str]] = Field(None, description="Things to avoid: sugar, fragrance, allergens, etc.")
    budget: Optional[Any] = Field(None, description="Budget: numeric (5000) or categorical (low/medium/high)")
    age: Optional[str] = Field(None, description="Age: newborn, 25, 40+, etc.")
    preferences: Optional[List[str]] = Field(None, description="Preferences: organic, fragrance_free, vegan, etc.")
    query: Optional[str] = Field(None, description="Natural language query")
    top_k: Optional[int] = Field(default=5, ge=1, le=10, description="Number of recommendations")
    language: Optional[str] = Field(default='en', description="Response language: en, ar, fr")

@app.post('/recommend')
def recommend(req: RecommendRequest):
    """
    Intelligent multi-category product recommendation endpoint
    
    Handles complex user situations like:
    - "I have diabetes and anemia, need vitamins without sugar"
    - "Dry but sensitive skin, looking for fragrance-free moisturizer"
    - "Need running shoes for diabetic feet"
    - "Baby lotion for eczema-prone skin"
    
    Request body examples:
    
    1. Health supplements for diabetic with anemia:
    {
        "category": "health_supplements",
        "medical_conditions": ["diabetes", "anemia"],
        "needs": ["energy", "immunity"],
        "avoid": ["sugar"],
        "budget": 5000,
        "top_k": 3
    }
    
    2. Skincare for dry, sensitive skin:
    {
        "category": "beauty_skincare",
        "skin_conditions": ["dry", "sensitive"],
        "avoid": ["fragrance"],
        "preferences": ["hypoallergenic"],
        "budget": "medium",
        "top_k": 3
    }
    
    3. Natural language query:
    {
        "query": "I need vitamins but I'm diabetic and have anemia",
        "top_k": 5
    }
    
    Response:
    {
        "recommendations": [
            {
                "id": "supp-001",
                "name": "Sugar-Free Multivitamin for Diabetics",
                "price": 3500,
                "currency": "DA",
                "category": "health_supplements",
                "tags": ["sugar_free", "diabetic_friendly"],
                "description": "Complete multivitamin formulated for diabetics...",
                "reason": "✅ Safe for diabetes, anemia • 💊 Beneficial for anemia...",
                "score": 1.245,
                "safety_notes": ["⚕️ Consult doctor if on blood thinners"]
            }
        ],
        "count": 1,
        "metadata": {
            "warnings": [...],
            "safety_info": [...],
            "constraints_applied": ["medical_safety", "ingredient_avoidance"],
            "filtered_out": {
                "medical_safety": 2,
                "skin_incompatibility": 0,
                "budget": 1
            }
        }
    }
    """
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
        if req.budget:
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
        
        # Handle no results
        if not recommendations:
            return {
                "recommendations": [],
                "count": 0,
                "language": req.language,
                "metadata": metadata,
                "message": "No matching products found. Please try different criteria."
            }
        
        return {
            "recommendations": recommendations,
            "count": len(recommendations),
            "language": req.language,
            "metadata": metadata
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating recommendations: {str(e)}"
        )

@app.get('/products')
def get_products():
    """Get all beauty & health products"""
    return beauty_recommender.get_products()

@app.get('/categories')
def get_categories():
    """Get all product categories"""
    categories = {}
    for product in beauty_recommender.products:
        cat = product.get('category', 'other')
        subcat = product.get('subcategory', 'other')
        if cat not in categories:
            categories[cat] = set()
        categories[cat].add(subcat)
    
    # Convert sets to lists for JSON serialization
    return {cat: list(subcats) for cat, subcats in categories.items()}

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/stats")
def get_stats():
    """Get recommendation system statistics"""
    return beauty_recommender.get_stats()

@app.get('/health')
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Beauty & Health Recommendation System",
        "products_loaded": len(beauty_recommender.products),
        "categories": len(set(p.get('category') for p in beauty_recommender.products))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4708)
