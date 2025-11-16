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
        """Fast recommendation using FAISS ANN search"""
        session_emb = get_embedding(session_text).reshape(1, -1).astype('float32')
        faiss.normalize_L2(session_emb)  # Normalize for cosine similarity
        
        # Step 1: Fast ANN search - get top candidates (more than needed for filtering)
        search_k = min(top_k * 10, len(self.products))  # Search 10x more for filtering
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
            
            # Compute composite score
            cat_match = 1.0 if category and product['category'].lower() == category.lower() else 0.5
            pop = normalize(product['popularity'])
            stock = normalize(product['stock'], min_val=0, max_val=50)
            recency = normalize(product['recency'])
            personal = normalize(product['personal'])
            seller_boost = product.get('seller_boost', 0.0)
            
            score = compute_score(sim, cat_match, pop, stock, recency, personal, seller_boost)
            
            candidates.append({
                'id': product['id'],
                'title': product['title'],
                'category': product['category'],
                'price': product.get('price', 0),
                'similarity': float(round(sim, 3)),
                'score': float(round(score, 3)),
                'reason': self._reason(session_text, product)
            })
        
        # Step 3: Sort by composite score and return top-k
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return candidates[:top_k]

    def _reason(self, session_text, product):
        """Generate explanation for recommendation"""
        session_lower = session_text.lower()
        title_lower = product['title'].lower()
        desc_lower = product['description'].lower()
        
        # Check for specific matches
        keywords = ['running', 'yoga', 'wireless', 'lightweight', 'premium', 'pro', 'fitness']
        for keyword in keywords:
            if keyword in session_lower and (keyword in title_lower or keyword in desc_lower):
                return f"Matches your request for {keyword} products."
        
        return f"Highly relevant to your search in {product['category']}."

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
