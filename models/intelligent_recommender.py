import json
import numpy as np
import faiss
from utils.embeddings import get_embedding, get_embeddings
from utils.scoring import compute_score, normalize
from typing import Dict, List, Optional, Tuple, Set

class IntelligentRecommender:
    """
    Multi-category intelligent recommendation system
    Handles complex user situations across beauty, health, supplements, sportswear, baby care, etc.
    """
    
    def __init__(self, products_path='data/products_catalog.json'):
        with open(products_path, 'r', encoding='utf-8') as f:
            self.products = json.load(f)
        
        # Create comprehensive searchable text for each product
        self.product_texts = []
        for p in self.products:
            text = self._create_product_text(p)
            self.product_texts.append(text)
        
        self.product_embeddings = get_embeddings(self.product_texts)
        self._build_faiss_index()
        
        print(f"✅ Loaded {len(self.products)} products across {len(self._get_categories())} categories")

    def _create_product_text(self, product: Dict) -> str:
        """Create comprehensive searchable text from product"""
        parts = []
        
        # Names in all languages
        parts.append(product.get('name', ''))
        parts.append(product.get('name_ar', ''))
        parts.append(product.get('name_fr', ''))
        
        # Descriptions
        parts.append(product.get('description', ''))
        parts.append(product.get('description_ar', ''))
        parts.append(product.get('description_fr', ''))
        
        # Category info
        parts.append(product.get('category', ''))
        parts.append(product.get('subcategory', ''))
        parts.extend(product.get('tags', []))
        
        # Skin conditions
        if 'skin_conditions' in product:
            parts.extend(product['skin_conditions'].get('suitable_for', []))
            
        # Medical conditions
        if 'medical_conditions' in product:
            med = product['medical_conditions']
            parts.extend(med.get('safe_for', []))
            parts.extend(med.get('beneficial_for', []))
            parts.extend(med.get('essential_for', []))
        
        # Nutritional info (for supplements)
        if 'nutritional_info' in product:
            parts.extend(product['nutritional_info'].get('key_nutrients', []))
        
        return ' '.join(str(p) for p in parts if p)

    def _build_faiss_index(self):
        """Build FAISS index for fast similarity search"""
        embedding_dim = self.product_embeddings.shape[1]
        faiss.normalize_L2(self.product_embeddings)
        
        if len(self.products) < 1000:
            self.index = faiss.IndexFlatIP(embedding_dim)
            self.index.add(self.product_embeddings)
        else:
            nlist = int(np.sqrt(len(self.products)))
            quantizer = faiss.IndexFlatIP(embedding_dim)
            self.index = faiss.IndexIVFFlat(quantizer, embedding_dim, nlist, faiss.METRIC_INNER_PRODUCT)
            self.index.train(self.product_embeddings)
            self.index.add(self.product_embeddings)
            self.index.nprobe = max(1, nlist // 10)
        
        print(f"📊 FAISS index: {type(self.index).__name__}, {len(self.products)} vectors")

    def _get_categories(self) -> Set[str]:
        """Get all unique categories"""
        return set(p.get('category', '') for p in self.products)

    def recommend(self, user_request: Dict, top_k: int = 5, language: str = 'en') -> Dict:
        """
        Main recommendation method with intelligent constraint handling
        
        Args:
            user_request: {
                "category": "health_supplements" | "beauty_skincare" | "sportswear" | "baby_care" | etc,
                "needs": ["energy", "immunity"],  # What they want
                "skin_conditions": ["dry", "sensitive"],  # For beauty products
                "medical_conditions": ["diabetes", "anemia"],  # Health constraints
                "avoid": ["sugar", "fragrance"],  # Things to avoid
                "budget": 5000 or "medium",
                "age": "newborn" | "25" | "40+",
                "preferences": ["organic", "fragrance_free"],
                "query": "I need vitamins but I'm diabetic and have anemia"  # Natural language
            }
            top_k: Number of recommendations
            language: Response language
        
        Returns:
            {
                "recommendations": [...],
                "count": int,
                "metadata": {
                    "warnings": [...],
                    "safety_info": [...],
                    "constraints_applied": [...]
                }
            }
        """
        metadata = {
            'warnings': [],
            'safety_info': [],
            'constraints_applied': [],
            'filtered_out': {
                'medical_safety': 0,
                'skin_incompatibility': 0,
                'budget': 0,
                'out_of_stock': 0
            }
        }
        
        # Step 1: Parse user request and create search query
        query_text, parsed_constraints = self._parse_user_request(user_request)
        
        # Step 2: Vector search for initial candidates
        candidates = self._vector_search(query_text, top_k * 10)
        
        # Step 3: Apply intelligent filtering based on constraints
        safe_products, filter_metadata = self._apply_intelligent_filters(
            candidates, 
            parsed_constraints,
            user_request
        )
        
        metadata.update(filter_metadata)
        
        # Step 4: Score and rank products
        scored_products = self._score_products(safe_products, user_request, parsed_constraints)
        
        # Step 5: Select top recommendations
        top_recommendations = scored_products[:top_k]
        
        # Step 6: Generate safety warnings and advice
        safety_warnings = self._generate_safety_warnings(top_recommendations, parsed_constraints)
        metadata['warnings'].extend(safety_warnings)
        
        # Step 7: Format response
        formatted_recommendations = self._format_recommendations(
            top_recommendations, 
            user_request, 
            language
        )
        
        return {
            'recommendations': formatted_recommendations,
            'count': len(formatted_recommendations),
            'metadata': metadata,
            'language': language
        }

    def _parse_user_request(self, request: Dict) -> Tuple[str, Dict]:
        """Parse user request into search query and constraints"""
        query_parts = []
        constraints = {
            'medical_conditions': set(),
            'skin_conditions': set(),
            'avoid_ingredients': set(),
            'avoid_conditions': set(),
            'must_have_features': set(),
            'category': request.get('category'),
            'budget': request.get('budget'),
            'age': request.get('age')
        }
        
        # Natural language query
        if 'query' in request:
            query_parts.append(request['query'])
        
        # Category
        if 'category' in request:
            query_parts.append(request['category'])
        
        # Needs
        if 'needs' in request:
            needs = request['needs']
            if isinstance(needs, list):
                query_parts.extend(needs)
            else:
                query_parts.append(needs)
        
        # Medical conditions
        if 'medical_conditions' in request:
            conditions = request['medical_conditions']
            if isinstance(conditions, list):
                constraints['medical_conditions'].update(conditions)
            else:
                constraints['medical_conditions'].add(conditions)
        
        # Skin conditions
        if 'skin_conditions' in request:
            skin_conds = request['skin_conditions']
            if isinstance(skin_conds, list):
                constraints['skin_conditions'].update(skin_conds)
            else:
                constraints['skin_conditions'].add(skin_conds)
        
        # Things to avoid
        if 'avoid' in request:
            avoid = request['avoid']
            if isinstance(avoid, list):
                constraints['avoid_ingredients'].update(avoid)
            else:
                constraints['avoid_ingredients'].add(avoid)
        
        # Preferences (must-have features)
        if 'preferences' in request:
            prefs = request['preferences']
            if isinstance(prefs, list):
                constraints['must_have_features'].update(prefs)
            else:
                constraints['must_have_features'].add(prefs)
        
        query_text = ' '.join(str(p) for p in query_parts if p)
        return query_text, constraints

    def _vector_search(self, query_text: str, top_k: int) -> List[Dict]:
        """Perform vector similarity search"""
        query_embedding = get_embedding(query_text)
        query_embedding = query_embedding.reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.products)))
        
        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx < len(self.products):
                product = self.products[idx].copy()
                product['similarity_score'] = float(score)
                results.append(product)
        
        return results

    def _apply_intelligent_filters(self, candidates: List[Dict], constraints: Dict, user_request: Dict) -> Tuple[List[Dict], Dict]:
        """Apply intelligent safety and compatibility filters"""
        metadata = {
            'warnings': [],
            'safety_info': [],
            'constraints_applied': [],
            'filtered_out': {
                'medical_safety': 0,
                'skin_incompatibility': 0,
                'budget': 0,
                'out_of_stock': 0,
                'category_mismatch': 0
            }
        }
        
        safe_products = []
        
        for product in candidates:
            reasons_to_exclude = []
            safety_notes = []
            
            # Filter 1: Category match
            if constraints['category']:
                if product.get('category') != constraints['category']:
                    metadata['filtered_out']['category_mismatch'] += 1
                    continue
            
            # Filter 2: Stock availability
            if product.get('stock', 0) <= 0:
                metadata['filtered_out']['out_of_stock'] += 1
                continue
            
            # Filter 3: Medical safety check (CRITICAL)
            if constraints['medical_conditions']:
                medical_check = self._check_medical_safety(product, constraints['medical_conditions'])
                if not medical_check['safe']:
                    reasons_to_exclude.append(medical_check['reason'])
                    metadata['filtered_out']['medical_safety'] += 1
                    continue
                if medical_check.get('consult_doctor'):
                    safety_notes.append(f"⚕️ Consult doctor: {medical_check['consult_doctor']}")
            
            # Filter 4: Skin compatibility check (for beauty/skincare)
            if product.get('category') in ['beauty_skincare', 'baby_care'] and constraints['skin_conditions']:
                skin_check = self._check_skin_compatibility(product, constraints['skin_conditions'])
                if not skin_check['compatible']:
                    reasons_to_exclude.append(skin_check['reason'])
                    metadata['filtered_out']['skin_incompatibility'] += 1
                    continue
            
            # Filter 5: Avoid ingredients/features check
            if constraints['avoid_ingredients']:
                avoid_check = self._check_avoidance(product, constraints['avoid_ingredients'])
                if not avoid_check['safe']:
                    reasons_to_exclude.append(avoid_check['reason'])
                    continue
            
            # Filter 6: Budget check
            if constraints['budget']:
                budget_check = self._check_budget(product, constraints['budget'])
                if not budget_check['within_budget']:
                    metadata['filtered_out']['budget'] += 1
                    continue
            
            # Product passed all filters
            product['safety_notes'] = safety_notes
            safe_products.append(product)
            
            # Track which constraints were applied
            if not metadata['constraints_applied']:
                applied = []
                if constraints['medical_conditions']:
                    applied.append('medical_safety')
                if constraints['skin_conditions']:
                    applied.append('skin_compatibility')
                if constraints['avoid_ingredients']:
                    applied.append('ingredient_avoidance')
                if constraints['budget']:
                    applied.append('budget')
                metadata['constraints_applied'] = applied
        
        return safe_products, metadata

    def _check_medical_safety(self, product: Dict, user_conditions: Set[str]) -> Dict:
        """Check if product is safe for user's medical conditions"""
        if 'medical_conditions' not in product:
            return {'safe': True}
        
        med_info = product['medical_conditions']
        
        # Check avoid_if conditions (CRITICAL - unsafe)
        avoid_if = set(med_info.get('avoid_if', []))
        conflicts = user_conditions.intersection(avoid_if)
        if conflicts:
            return {
                'safe': False,
                'reason': f"❌ Unsafe for: {', '.join(conflicts)}"
            }
        
        # Check consult_doctor conditions (WARNING - needs medical advice)
        consult = set(med_info.get('consult_doctor', []))
        needs_consultation = user_conditions.intersection(consult)
        if needs_consultation:
            return {
                'safe': True,
                'consult_doctor': ', '.join(needs_consultation)
            }
        
        # Check if product is beneficial for user's conditions
        safe_for = set(med_info.get('safe_for', []))
        beneficial = set(med_info.get('beneficial_for', []))
        essential = set(med_info.get('essential_for', []))
        
        return {'safe': True}

    def _check_skin_compatibility(self, product: Dict, user_skin_conditions: Set[str]) -> Dict:
        """Check skin type compatibility"""
        if 'skin_conditions' not in product:
            return {'compatible': True}
        
        skin_info = product['skin_conditions']
        
        # Check avoid_if conditions
        avoid_if = set(skin_info.get('avoid_if', []))
        conflicts = user_skin_conditions.intersection(avoid_if)
        if conflicts:
            return {
                'compatible': False,
                'reason': f"❌ Not suitable for skin type: {', '.join(conflicts)}"
            }
        
        # Check suitable_for
        suitable = set(skin_info.get('suitable_for', []))
        if suitable and not user_skin_conditions.intersection(suitable):
            # User's skin type not in suitable list
            return {
                'compatible': False,
                'reason': f"❌ Not formulated for your skin type"
            }
        
        return {'compatible': True}

    def _check_avoidance(self, product: Dict, avoid_items: Set[str]) -> Dict:
        """Check if product contains items user wants to avoid"""
        product_text = json.dumps(product).lower()
        
        for item in avoid_items:
            item_lower = item.lower()
            # Check in tags
            if any(item_lower in tag.lower() for tag in product.get('tags', [])):
                if item_lower not in ['sugar_free', 'fragrance_free']:  # These are good
                    return {'safe': False, 'reason': f"❌ Contains {item}"}
            
            # Special checks
            if item_lower == 'sugar':
                if 'nutritional_info' in product:
                    sugar = product['nutritional_info'].get('sugar_content', 0)
                    if sugar > 2:  # More than 2g sugar
                        return {'safe': False, 'reason': f"❌ Contains {sugar}g sugar"}
            
            if item_lower == 'fragrance':
                if 'fragrance_free' not in product.get('tags', []):
                    if 'fragrance' in product_text:
                        return {'safe': False, 'reason': "❌ Contains fragrance"}
        
        return {'safe': True}

    def _check_budget(self, product: Dict, budget) -> Dict:
        """Check if product fits budget"""
        price = product.get('price', 0)
        
        if isinstance(budget, (int, float)):
            return {
                'within_budget': price <= budget,
                'price': price,
                'budget': budget
            }
        
        # Categorical budget
        budget_ranges = {
            'low': (0, 2000),
            'medium': (2000, 5000),
            'high': (5000, float('inf'))
        }
        
        if isinstance(budget, str):
            budget_lower = budget.lower()
            if budget_lower in budget_ranges:
                min_price, max_price = budget_ranges[budget_lower]
                return {
                    'within_budget': min_price <= price <= max_price,
                    'price': price
                }
        
        return {'within_budget': True}

    def _score_products(self, products: List[Dict], user_request: Dict, constraints: Dict) -> List[Dict]:
        """Score and rank products based on user needs"""
        for product in products:
            score = product.get('similarity_score', 0.0)
            
            # Boost if beneficial for user's conditions
            if 'medical_conditions' in product and constraints['medical_conditions']:
                med_info = product['medical_conditions']
                beneficial = set(med_info.get('beneficial_for', []))
                essential = set(med_info.get('essential_for', []))
                
                matches = constraints['medical_conditions'].intersection(beneficial)
                if matches:
                    score += 0.3 * len(matches)
                
                matches = constraints['medical_conditions'].intersection(essential)
                if matches:
                    score += 0.5 * len(matches)
            
            # Boost if has required features
            if constraints['must_have_features']:
                product_tags = set(product.get('tags', []))
                matches = constraints['must_have_features'].intersection(product_tags)
                if matches:
                    score += 0.2 * len(matches)
            
            # Boost for exact category match
            if constraints['category'] and product.get('category') == constraints['category']:
                score += 0.2
            
            # Boost for in-stock items
            if product.get('stock', 0) > 0:
                score += 0.1
            
            product['final_score'] = score
        
        # Sort by final score
        products.sort(key=lambda p: p.get('final_score', 0), reverse=True)
        return products

    def _generate_safety_warnings(self, products: List[Dict], constraints: Dict) -> List[Dict]:
        """Generate safety warnings based on selected products"""
        warnings = []
        
        for product in products:
            if product.get('safety_notes'):
                for note in product['safety_notes']:
                    warnings.append({
                        'type': 'medical_consultation',
                        'severity': 'medium',
                        'product': product['name'],
                        'message': note
                    })
        
        return warnings

    def _format_recommendations(self, products: List[Dict], user_request: Dict, language: str) -> List[Dict]:
        """Format products for response"""
        formatted = []
        
        for product in products:
            # Select language-specific fields
            name_field = 'name'
            desc_field = 'description'
            if language == 'ar':
                name_field = 'name_ar'
                desc_field = 'description_ar'
            elif language == 'fr':
                name_field = 'name_fr'
                desc_field = 'description_fr'
            
            rec = {
                'id': product['id'],
                'name': product.get(name_field, product['name']),
                'price': product.get('price'),
                'currency': product.get('currency', 'DA'),
                'category': product.get('category'),
                'subcategory': product.get('subcategory'),
                'tags': product.get('tags', []),
                'description': product.get(desc_field, product['description']),
                'score': round(product.get('final_score', 0), 3),
                'stock': product.get('stock', 0)
            }
            
            # Add reason for recommendation
            rec['reason'] = self._generate_reason(product, user_request, language)
            
            # Add safety notes
            if product.get('safety_notes'):
                rec['safety_notes'] = product['safety_notes']
            
            formatted.append(rec)
        
        return formatted

    def _generate_reason(self, product: Dict, user_request: Dict, language: str) -> str:
        """Generate personalized reason for recommendation"""
        reasons = []
        
        # Check medical benefits
        if 'medical_conditions' in product and user_request.get('medical_conditions'):
            med_info = product['medical_conditions']
            user_conditions = set(user_request['medical_conditions']) if isinstance(user_request['medical_conditions'], list) else {user_request['medical_conditions']}
            
            safe_for = set(med_info.get('safe_for', []))
            beneficial = set(med_info.get('beneficial_for', []))
            
            matches = user_conditions.intersection(safe_for)
            if matches:
                reasons.append(f"✅ Safe for {', '.join(matches)}")
            
            matches = user_conditions.intersection(beneficial)
            if matches:
                reasons.append(f"💊 Beneficial for {', '.join(matches)}")
        
        # Check skin compatibility
        if 'skin_conditions' in product and user_request.get('skin_conditions'):
            skin_info = product['skin_conditions']
            user_skin = set(user_request['skin_conditions']) if isinstance(user_request['skin_conditions'], list) else {user_request['skin_conditions']}
            
            suitable = set(skin_info.get('suitable_for', []))
            matches = user_skin.intersection(suitable)
            if matches:
                reasons.append(f"🧴 Suitable for {', '.join(matches)} skin")
        
        # Check special features
        if user_request.get('preferences'):
            prefs = set(user_request['preferences']) if isinstance(user_request['preferences'], list) else {user_request['preferences']}
            product_tags = set(product.get('tags', []))
            matches = prefs.intersection(product_tags)
            if matches:
                reasons.append(f"⭐ Features: {', '.join(matches)}")
        
        if not reasons:
            reasons.append(f"📦 Recommended {product.get('category', 'product')}")
        
        return ' • '.join(reasons)

    def get_stats(self) -> Dict:
        """Get system statistics"""
        categories = {}
        for p in self.products:
            cat = p.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_products': len(self.products),
            'in_stock': sum(1 for p in self.products if p.get('stock', 0) > 0),
            'categories': categories,
            'index_type': type(self.index).__name__
        }
