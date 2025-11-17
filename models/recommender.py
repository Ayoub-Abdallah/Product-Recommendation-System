import json
import numpy as np
import faiss
from utils.embeddings import get_embedding, get_embeddings
from utils.scoring import compute_score, normalize

class Recommender:
    def __init__(self, products_path):
        with open(products_path, 'r') as f:
            self.products = json.load(f)
        self.product_texts = [p['title'] + ' ' + p['description'] for p in self.products]
        self.product_embeddings = get_embeddings(self.product_texts)
        
        # Build FAISS index for fast ANN search
        self._build_faiss_index()
        
        print(f"✅ Loaded {len(self.products)} products with FAISS ANN index")

    def _build_faiss_index(self):
        """Build FAISS index for Approximate Nearest Neighbor search"""
        embedding_dim = self.product_embeddings.shape[1]
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.product_embeddings)
        
        # Use IndexIVFFlat for large datasets (faster than brute force)
        # For very large catalogs (100K+), consider IndexHNSW
        if len(self.products) < 1000:
            # For small datasets, use exact search (IndexFlatIP)
            self.index = faiss.IndexFlatIP(embedding_dim)
            self.index.add(self.product_embeddings)
        else:
            # For larger datasets, use IVF (Inverted File Index)
            nlist = int(np.sqrt(len(self.products)))  # number of clusters
            quantizer = faiss.IndexFlatIP(embedding_dim)
            self.index = faiss.IndexIVFFlat(quantizer, embedding_dim, nlist, faiss.METRIC_INNER_PRODUCT)
            
            # Train the index
            self.index.train(self.product_embeddings)
            self.index.add(self.product_embeddings)
            
            # Set search parameters (nprobe = number of clusters to search)
            self.index.nprobe = max(1, nlist // 10)  # Search 10% of clusters
        
        print(f"📊 FAISS index built: {type(self.index).__name__}, {len(self.products)} vectors, dim={embedding_dim}")

    def recommend(self, session_text, category=None, top_k=5):
        """Fast recommendation using FAISS ANN search with smart keyword boosting"""
        session_emb = get_embedding(session_text).reshape(1, -1).astype('float32')
        faiss.normalize_L2(session_emb)  # Normalize for cosine similarity
        
        # Extract keywords and infer category if not provided
        session_lower = session_text.lower()
        detected_category, keyword_matches = self._detect_product_type(session_lower)
        
        # Use detected category if none provided
        if not category and detected_category:
            category = detected_category
        
        # Step 1: Fast ANN search - get more candidates for better filtering
        search_k = min(top_k * 20, len(self.products))  # Search 20x more for better results
        similarities, indices = self.index.search(session_emb, search_k)
        
        # Step 2: Filter and score candidates
        candidates = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:  # FAISS returns -1 for empty results
                continue
                
            product = self.products[int(idx)]
            
            # Apply filters
            if product['stock'] <= 0:
                continue
            if category and product['category'].lower() != category.lower():
                continue
            
            # Similarity from FAISS (already normalized, range 0-1)
            sim = float(similarities[0][i])
            
            # Smart keyword matching - boost products with exact keyword matches
            keyword_boost = self._calculate_keyword_boost(session_lower, product, keyword_matches)
            
            # Category relevance - penalize irrelevant categories
            category_penalty = self._calculate_category_penalty(session_lower, product['category'])
            
            # Enhanced similarity with keyword boost
            enhanced_sim = min(sim + keyword_boost, 1.0)
            
            # Compute composite score
            cat_match = 1.0 if category and product['category'].lower() == category.lower() else 0.5
            pop = normalize(product['popularity'])
            stock = normalize(product['stock'], min_val=0, max_val=50)
            recency = normalize(product['recency'])
            personal = normalize(product['personal'])
            seller_boost = product.get('seller_boost', 0.0)
            
            # Apply category penalty
            score = compute_score(enhanced_sim, cat_match, pop, stock, recency, personal, seller_boost)
            score = score * (1 - category_penalty)
            
            candidates.append({
                'id': product['id'],
                'title': product['title'],
                'category': product['category'],
                'price': product.get('price', 0),
                'similarity': float(round(sim, 3)),
                'enhanced_similarity': float(round(enhanced_sim, 3)),
                'keyword_boost': float(round(keyword_boost, 3)),
                'score': float(round(score, 3)),
                'reason': self._reason(session_text, product, keyword_matches)
            })
        
        # Step 3: Sort by composite score and return top-k
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return candidates[:top_k]
    
    def _detect_product_type(self, query):
        """Detect product type and extract relevant keywords from query"""
        # Product type keywords mapped to categories
        product_keywords = {
            'Outdoor': ['chair', 'seat', 'bench', 'stool', 'sit', 'sitting', 'tent', 'camping', 'backpack', 'sleeping bag', 'lantern', 'cooler', 'hammock'],
            'Furniture': ['chair', 'seat', 'bench', 'stool', 'sit', 'sitting', 'table', 'desk', 'sofa', 'couch'],
            'Sportswear': ['shoes', 'sneakers', 'trainers', 'runners', 'kicks', 'cleats', 'boots', 'footwear'],
            'Fitness': ['mat', 'yoga', 'pilates', 'exercise', 'workout', 'gym', 'dumbbell', 'band', 'ball', 'fitness'],
            'Electronics': ['headphones', 'earbuds', 'speaker', 'charger', 'tracker', 'watch', 'phone', 'laptop', 'wireless', 'bluetooth'],
            'Home & Kitchen': ['blender', 'mixer', 'pan', 'pot', 'knife', 'cooker', 'kettle', 'toaster', 'kitchen'],
            'Clothing': ['shirt', 't-shirt', 'hoodie', 'jacket', 'pants', 'shorts', 'socks', 'hat', 'wear'],
            'Beauty': ['cream', 'lotion', 'serum', 'mask', 'cleanser', 'shampoo', 'conditioner', 'beauty'],
            'Toys & Games': ['toy', 'game', 'puzzle', 'blocks', 'doll', 'action figure', 'play'],
            'Pet Supplies': ['pet', 'dog', 'cat', 'food', 'toy', 'bed', 'collar', 'leash', 'animal']
        }
        
        # Common phrases mapped to keywords
        phrase_mappings = {
            'sit on': 'chair',
            'sitting': 'chair',
            'to sit': 'chair',
            'listen to music': 'headphones',
            'listen music': 'headphones',
            'make smoothie': 'blender',
            'blend': 'blender',
            'cook': 'kitchen',
            'wear': 'clothing',
            'run': 'shoes',
            'jog': 'shoes',
            'walk': 'shoes',
        }
        
        detected_category = None
        matched_keywords = []
        
        # Check phrase mappings first
        for phrase, keyword in phrase_mappings.items():
            if phrase in query:
                matched_keywords.append(keyword)
        
        # Then check individual keywords
        for category, keywords in product_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    if keyword not in matched_keywords:
                        matched_keywords.append(keyword)
                    if not detected_category:
                        detected_category = category
        
        return detected_category, matched_keywords
    
    def _calculate_keyword_boost(self, query, product, keyword_matches):
        """Calculate boost based on exact keyword matches in product title/description"""
        title_lower = product['title'].lower()
        desc_lower = product['description'].lower()
        
        boost = 0.0
        
        # Boost for exact keyword matches
        for keyword in keyword_matches:
            if keyword in title_lower:
                boost += 0.3  # Strong boost for title match
            elif keyword in desc_lower:
                boost += 0.15  # Medium boost for description match
        
        # Extract important words from query (nouns/adjectives)
        query_words = [w for w in query.split() if len(w) > 3 and w not in ['this', 'that', 'what', 'where', 'when', 'need', 'want', 'looking', 'search']]
        
        # Boost for query word matches
        for word in query_words:
            if word in title_lower:
                boost += 0.2
            elif word in desc_lower:
                boost += 0.1
        
        return min(boost, 0.5)  # Cap at 0.5 to prevent over-boosting
    
    def _calculate_category_penalty(self, query, product_category):
        """Penalize obviously irrelevant categories"""
        category_lower = product_category.lower()
        
        # Strong penalties for mismatched categories
        penalties = {
            'books': ['chair', 'seat', 'shoes', 'headphones', 'blender', 'tent', 'bed', 'mat'],
            'clothing': ['blender', 'chair', 'tent', 'headphones', 'laptop'],
            'electronics': ['chair', 'shoes', 'shirt', 'pants'],
        }
        
        for cat, keywords in penalties.items():
            if cat in category_lower:
                for keyword in keywords:
                    if keyword in query:
                        return 0.7  # 70% penalty for obviously wrong category
        
        return 0.0  # No penalty

    def _reason(self, session_text, product, keyword_matches=None):
        """Generate explanation for recommendation"""
        session_lower = session_text.lower()
        title_lower = product['title'].lower()
        desc_lower = product['description'].lower()
        
        # Check for keyword matches
        if keyword_matches:
            for keyword in keyword_matches:
                if keyword in title_lower:
                    return f"Perfect match: Contains '{keyword}' that you're looking for."
                elif keyword in desc_lower:
                    return f"Great match: Features '{keyword}' in description."
        
        # Check for specific query terms
        query_words = [w for w in session_lower.split() if len(w) > 3]
        for word in query_words:
            if word in title_lower:
                return f"Matches your search for '{word}'."
        
        # Check common keywords
        common_keywords = {
            'running': 'running', 'yoga': 'yoga', 'wireless': 'wireless',
            'lightweight': 'lightweight', 'premium': 'premium', 'pro': 'professional',
            'fitness': 'fitness', 'outdoor': 'outdoor', 'camping': 'camping'
        }
        
        for key, display in common_keywords.items():
            if key in session_lower and (key in title_lower or key in desc_lower):
                return f"Recommended for your {display} needs."
        
        return f"Top-rated product in {product['category']}."

    def update_seller_boost(self, product_id, boost):
        """Update seller boost for a product and rebuild index"""
        for product in self.products:
            if product['id'] == product_id:
                product['seller_boost'] = boost
                break
        
        # Save updated products
        with open('data/products.json', 'w') as f:
            json.dump(self.products, f, indent=2)

    def get_products(self):
        """Get all products"""
        return self.products
    
    def get_stats(self):
        """Get catalog statistics"""
        total = len(self.products)
        in_stock = sum(1 for p in self.products if p['stock'] > 0)
        categories = {}
        for p in self.products:
            cat = p['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_products': total,
            'in_stock': in_stock,
            'categories': categories,
            'index_type': type(self.index).__name__
        }
