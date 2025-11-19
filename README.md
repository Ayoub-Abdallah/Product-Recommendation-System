# Beauty & Health Product Recommendation System

## Overview

This is a comprehensive **Beauty & Health Product Recommendation System** that provides personalized product recommendations across multiple categories including skincare, haircare, makeup, supplements, and wellness products.

## 🎯 Key Features

### 1. **Multiple Product Categories**
- **Skin Care** (11 products): Serums, moisturizers, cleansers, treatments, toners, eye care, sunscreen
- **Hair Care** (4 products): Shampoos, conditioners, treatments
- **Makeup** (2 products): Foundations with skincare benefits
- **Supplements** (5 products): Vitamins, beauty supplements, essential fatty acids, multivitamins
- **Wellness** (2 products): Sleep support, digestive health

**Total: 24 curated products**

### 2. **Smart Recommendation Engine**
- **Semantic search** using sentence transformers
- **FAISS-powered** vector similarity search
- **Multi-factor scoring** based on:
  - Similarity to user needs
  - Product popularity
  - Stock availability
  - Recency
  - Personal preferences
  - Seller boost

### 3. **Intelligent Budget Handling**
- **Numeric budgets**: e.g., 2500 DA (exact price filtering)
- **Categorical budgets**: "low", "medium", "high"
- **Price ratio filtering**: Finds products within budget range with smart tolerance

### 4. **Multilingual Support**
- **English** (en)
- **Arabic** (ar) - العربية
- **French** (fr) - Français

### 5. **Personalization Factors**
- Skin type (oily, dry, combination, normal, sensitive)
- Hair type (oily, dry, normal, curly, straight, wavy)
- Specific problems/concerns (acne, wrinkles, hair loss, fatigue, etc.)
- Age range
- Gender
- Budget constraints

## 🚀 API Endpoints

### POST /recommend
Main recommendation endpoint (summary-based)

**Request:**
```json
{
  "summary": {
    "skin_type": "oily",
    "hair_type": "curly",
    "problem": "acne",
    "category": "skin_care",
    "budget": 2500,
    "age": "25",
    "gender": "female"
  },
  "top_k": 5,
  "language": "en"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": "hind-001",
      "name": "Niacinamide Serum 10% + Zinc 1%",
      "price": 2500,
      "currency": "DA",
      "category": "skin_care",
      "subcategory": "serum",
      "description": "Controls sebum production...",
      "reason": "Perfect for your oily skin type • Addresses your acne concern",
      "score": 1.189,
      "tags": ["oily_skin", "acne", "sebum_control"],
      "image": "https://example.com/..."
    }
  ],
  "count": 1,
  "language": "en"
}
```

### GET /products
Get all available products

### GET /categories
Get all product categories and subcategories

### GET /stats
Get system statistics

### GET /health
Health check endpoint

## 💻 Web Interface

The system includes a beautiful, modern web interface with:

- **Responsive design** (mobile-friendly)
- **Gradient purple theme**
- **Form-based product finder** with filters for:
  - Skin type
  - Hair type
  - Category
  - Problem/concern
  - Budget
  - Age
  - Gender
  - Language preference
  - Number of results (1-10)

- **Beautiful product cards** showing:
  - Product name with gradient header
  - Price (prominently displayed with gradient background)
  - Category and subcategory
  - Detailed reason for recommendation
  - Score
  - Product tags
  - Product ID

## 📦 Product Catalog Highlights

### Skincare Products
- Niacinamide Serum 10% + Zinc 1% (2500 DA)
- Hyaluronic Acid Hydrating Serum (2800 DA)
- Vitamin C Brightening Serum 15% (3200 DA)
- Retinol Night Cream 0.5% (3500 DA)
- Salicylic Acid 2% Acne Treatment (2200 DA)
- Glycolic Acid 7% Toning Solution (1900 DA)
- Azelaic Acid 10% Suspension (2400 DA)
- Ceramide Repair Cream (3000 DA)
- SPF 50 Sunscreen Gel (2600 DA)
- Gentle Foaming Cleanser (1800 DA)
- Caffeine Eye Serum (2000 DA)

### Hair Care Products
- Biotin & Collagen Shampoo (1600 DA)
- Keratin Repair Conditioner (1800 DA)
- Argan Oil Hair Treatment (2200 DA)
- Anti-Dandruff Shampoo (2400 DA)

### Makeup Products
- Matte Foundation SPF 30 (3500 DA)
- Vitamin C Brightening Serum Foundation (4200 DA)

### Supplements
- Vitamin D3 5000 IU (1800 DA)
- Biotin 10000 mcg Hair, Skin & Nails (2200 DA)
- Omega-3 Fish Oil 1000mg (2500 DA)
- Collagen Peptides Powder (3500 DA)
- Multivitamin Women's Formula (2800 DA)

### Wellness
- Melatonin 5mg Sleep Support (1500 DA)
- Probiotics 50 Billion CFU (3200 DA)

## 🔧 Technical Stack

- **Backend**: FastAPI (Python)
- **ML/AI**: 
  - Sentence Transformers (all-MiniLM-L6-v2)
  - FAISS (Facebook AI Similarity Search)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Server**: Uvicorn (ASGI server)

## 📝 Usage Examples

### Example 1: Skincare for Oily Acne-Prone Skin
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "skin_type": "oily",
      "problem": "acne",
      "budget": 2500
    },
    "top_k": 3,
    "language": "en"
  }'
```

### Example 2: Hair Growth Supplements
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "problem": "hair loss",
      "category": "supplements"
    },
    "top_k": 3,
    "language": "en"
  }'
```

### Example 3: Anti-Aging Products (French)
```bash
curl -X POST http://localhost:4708/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "summary": {
      "problem": "wrinkles",
      "age": "40+",
      "budget": "high"
    },
    "top_k": 5,
    "language": "fr"
  }'
```

## 🎨 Styling Features

- Modern gradient backgrounds
- Smooth hover animations
- Card-based layout
- Color-coded price displays (pink/red gradient)
- Professional typography
- Mobile-responsive grid system

## 🚦 Running the System

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app:app --host 0.0.0.0 --port 5000

# Or use the built-in runner
python app.py
```

Access the web interface at: `http://localhost:4708`

## 📊 System Statistics

- **Total Products**: 24
- **Categories**: 5 (skin_care, hair_care, makeup, supplements, wellness)
- **Subcategories**: 14
- **Languages Supported**: 3 (English, Arabic, French)
- **Price Range**: 1500 DA - 4200 DA
- **Average Price**: ~2500 DA

## 🔄 Recent Updates

### v2.0 - Beauty & Health Focus
- ✅ Removed all legacy conversation-based recommendation code
- ✅ Removed legacy sportswear products catalog
- ✅ Expanded to 24 products across 5 categories
- ✅ Added supplements and wellness categories
- ✅ Enhanced UI with modern gradient design
- ✅ Improved price display with prominent styling
- ✅ Added category filter in web interface
- ✅ Increased max results from 5 to 10
- ✅ Simplified API to single /recommend endpoint
- ✅ Added /categories endpoint for dynamic category discovery
- ✅ Enhanced health check endpoint with detailed stats

## 📄 License & Credits

Built for beauty and health product recommendations with a focus on the Algerian market (DA currency).

---

**Version**: 2.0  
**Last Updated**: November 18, 2025  
**Status**: ✅ Production Ready
