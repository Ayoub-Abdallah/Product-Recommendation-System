from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from models.beauty_recommender import BeautyRecommender
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional, List, Dict, Any
import json
import os

app = FastAPI(title="Beauty & Health Recommendation System", version="2.0")

# Load beauty & health recommender
beauty_products_path = 'data/beauty_products.json'
if os.path.exists(beauty_products_path):
    beauty_recommender = BeautyRecommender(beauty_products_path)
    print(f"✅ Beauty & Health recommender loaded with {len(beauty_recommender.products)} products")
else:
    raise FileNotFoundError(f"❌ Beauty products file not found at {beauty_products_path}")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class SummaryRecommendRequest(BaseModel):
    """Request model for summary-based beauty & health recommendations"""
    summary: Dict[str, Any] = Field(..., description="Structured summary object")
    top_k: Optional[int] = Field(default=3, ge=1, le=10, description="Number of recommendations (1-10)")
    language: Optional[str] = Field(default='en', description="Response language: en, ar, fr")

@app.post('/recommend')
def recommend(req: SummaryRecommendRequest):
    """
    Main endpoint for beauty & health product recommendations
    
    Request body:
    {
        "summary": {
            "skin_type": "oily" | "dry" | "combination" | "normal" | "sensitive",
            "hair_type": "oily" | "dry" | "normal" | "curly" | "straight" | "wavy",
            "problem": "acne" | "wrinkles" | "dark_spots" | "hair_loss" | "dandruff" | etc,
            "category": "skin_care" | "hair_care" | "makeup" | "supplements" | "wellness",
            "product_type": "serum" | "cream" | "shampoo" | "vitamin" | etc,
            "budget": 2500 (numeric) | "low" | "medium" | "high" (string),
            "age": "25" | "30-40" | etc,
            "gender": "female" | "male" | "unisex",
            "concerns": ["anti_aging", "hydration", "acne", "energy"],
            "language": "en" | "ar" | "fr"
        },
        "top_k": 3,
        "language": "en"
    }
    
    Response:
    {
        "recommendations": [
            {
                "id": "product-001",
                "name": "Product Name",
                "price": 2500,
                "currency": "DA",
                "image": "url",
                "tags": ["tag1", "tag2"],
                "description": "...",
                "reason": "Perfect for your skin type • Addresses your concern",
                "score": 0.95,
                "category": "skin_care",
                "subcategory": "serum"
            }
        ],
        "count": 1,
        "language": "en"
    }
    """
    # Validate summary
    if not req.summary:
        raise HTTPException(status_code=400, detail="Summary object is required")
    
    try:
        # Get recommendations (now returns dict with recommendations and metadata)
        result = beauty_recommender.recommend_from_summary(
            summary=req.summary,
            top_k=req.top_k,
            language=req.language
        )
        
        recommendations = result.get('recommendations', [])
        metadata = result.get('metadata', {})
        
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
