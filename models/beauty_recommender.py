import json
import numpy as np
import faiss
from utils.embeddings import get_embedding, get_embeddings
from utils.scoring import compute_score, normalize
from typing import Dict, List, Optional, Tuple

class BeautyRecommender:
    """Beauty product recommender with support for structured summaries"""
    
    def __init__(self, products_path='data/beauty_products.json'):
        with open(products_path, 'r', encoding='utf-8') as f:
            self.products = json.load(f)
        
        # Create searchable text for each product (multilingual)
        self.product_texts = []
        for p in self.products:
            text = f"{p['name']} {p.get('name_ar', '')} {p.get('name_fr', '')} "
            text += f"{p['description']} {p.get('description_ar', '')} {p.get('description_fr', '')} "
            text += f"{' '.join(p.get('tags', []))} "
            text += f"{' '.join(p.get('skin_types', []))} "
            text += f"{' '.join(p.get('hair_types', []))} "
            text += f"{' '.join(p.get('problems_solved', []))}"
            self.product_texts.append(text)
        
        self.product_embeddings = get_embeddings(self.product_texts)
        self._build_faiss_index()
        
        print(f"✅ Loaded {len(self.products)} beauty products with FAISS index")

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

    def recommend_from_summary(self, summary: Dict, top_k: int = 3, language: str = 'en') -> List[Dict]:
        """
        Recommend products based on structured summary
        
        Args:
            summary: Dict with fields like skin_type, hair_type, problem, budget, age, gender, etc.
            top_k: Number of recommendations to return (1-3)
            language: Preferred language for response ('en', 'ar', 'fr')
        
        Returns:
            Dict with recommendations and metadata including warnings and budget info
        """
        # Initialize metadata
        metadata = {
            'warnings': [],
            'budget_info': {},
            'search_info': {}
        }
        
        # Parse summary into search query
        query_text = self._parse_summary(summary)
        
        # Try vector search first
        results = self._vector_search(query_text, summary, top_k * 5)
        
        # If insufficient results, try keyword fallback
        if len(results) < top_k:
            keyword_results = self._keyword_search(summary, top_k * 3)
            results.extend(keyword_results)
            # Remove duplicates
            seen = set()
            unique_results = []
            for r in results:
                if r['id'] not in seen:
                    seen.add(r['id'])
                    unique_results.append(r)
            results = unique_results
        
        metadata['search_info']['total_candidates'] = len(results)
        
        # Apply business rules and filters (now returns filtered + metadata)
        filtered, filter_metadata = self._apply_business_rules(results, summary, return_metadata=True)
        
        # Merge filter metadata
        metadata.update(filter_metadata)
        
        metadata['search_info']['after_filtering'] = len(filtered)
        
        # Format recommendations
        recommendations = self._format_recommendations(filtered[:top_k], summary, language)
        
        return {
            'recommendations': recommendations,
            'metadata': metadata
        }

    def _parse_summary(self, summary: Dict) -> str:
        """Convert summary object into search query text"""
        query_parts = []
        
        # Add skin/hair type
        if summary.get('skin_type'):
            query_parts.append(f"skin type: {summary['skin_type']}")
        if summary.get('hair_type'):
            query_parts.append(f"hair type: {summary['hair_type']}")
        
        # Add problem/concern
        if summary.get('problem'):
            query_parts.append(f"problem: {summary['problem']}")
        
        # Add category preference
        if summary.get('category'):
            query_parts.append(f"category: {summary['category']}")
        
        # Add product type
        if summary.get('product_type'):
            query_parts.append(f"product: {summary['product_type']}")
        
        # Add specific concerns
        if summary.get('concerns'):
            if isinstance(summary['concerns'], list):
                query_parts.append(' '.join(summary['concerns']))
            else:
                query_parts.append(str(summary['concerns']))
        
        # Add age range
        if summary.get('age'):
            query_parts.append(f"age {summary['age']}")
        
        # Add budget info (convert to price range for search context)
        if summary.get('budget'):
            budget = summary['budget']
            if isinstance(budget, (int, float)):
                query_parts.append(f"price around {budget}")
            elif isinstance(budget, str):
                import re
                budget_str = budget.lower()
                numeric_match = re.search(r'(\d+)', budget_str)
                if numeric_match:
                    query_parts.append(f"price around {numeric_match.group(1)}")
                else:
                    query_parts.append(f"budget {budget}")
        
        return ' '.join(query_parts)

    def _vector_search(self, query_text: str, summary: Dict, top_k: int) -> List[Dict]:
        """Perform FAISS vector similarity search"""
        if not query_text.strip():
            return []
        
        query_emb = get_embedding(query_text).reshape(1, -1).astype('float32')
        faiss.normalize_L2(query_emb)
        
        search_k = min(top_k, len(self.products))
        similarities, indices = self.index.search(query_emb, search_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue
            
            product = self.products[int(idx)]
            
            # Basic filter: in stock
            if product.get('stock', 0) <= 0:
                continue
            
            similarity = float(similarities[0][i])
            
            # Calculate keyword boost
            boost = self._calculate_keyword_boost(query_text, product, summary)
            enhanced_sim = min(similarity + boost, 1.0)
            
            # Compute score
            score = self._compute_product_score(product, enhanced_sim)
            
            results.append({
                'id': product['id'],
                'product': product,
                'similarity': similarity,
                'enhanced_similarity': enhanced_sim,
                'score': score
            })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def _keyword_search(self, summary: Dict, top_k: int) -> List[Dict]:
        """Fallback keyword-based search"""
        results = []
        
        # Extract search criteria
        skin_type = summary.get('skin_type', '').lower()
        hair_type = summary.get('hair_type', '').lower()
        problem = summary.get('problem', '').lower()
        category = summary.get('category', '').lower()
        
        for product in self.products:
            if product.get('stock', 0) <= 0:
                continue
            
            match_score = 0.0
            
            # Match skin type
            if skin_type:
                skin_types = [st.lower() for st in product.get('skin_types', [])]
                if skin_type in skin_types or any(skin_type in st for st in skin_types):
                    match_score += 0.4
            
            # Match hair type
            if hair_type:
                hair_types = [ht.lower() for ht in product.get('hair_types', [])]
                if hair_type in hair_types or any(hair_type in ht for ht in hair_types):
                    match_score += 0.4
            
            # Match problem
            if problem:
                problems = [p.lower() for p in product.get('problems_solved', [])]
                tags = [t.lower() for t in product.get('tags', [])]
                if any(problem in p for p in problems) or any(problem in t for t in tags):
                    match_score += 0.5
            
            # Match category
            if category:
                if category in product.get('category', '').lower():
                    match_score += 0.3
            
            if match_score > 0:
                score = self._compute_product_score(product, match_score)
                results.append({
                    'id': product['id'],
                    'product': product,
                    'similarity': match_score,
                    'enhanced_similarity': match_score,
                    'score': score
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]

    def _calculate_keyword_boost(self, query: str, product: Dict, summary: Dict) -> float:
        """Calculate boost based on keyword matches"""
        boost = 0.0
        query_lower = query.lower()
        
        # Boost for problem matches
        problems = product.get('problems_solved', [])
        for problem in problems:
            if problem.lower() in query_lower:
                boost += 0.3
        
        # Boost for tag matches
        tags = product.get('tags', [])
        for tag in tags:
            if tag.lower() in query_lower:
                boost += 0.2
        
        # Boost for skin/hair type matches
        skin_types = product.get('skin_types', [])
        hair_types = product.get('hair_types', [])
        
        if summary.get('skin_type'):
            for st in skin_types:
                if summary['skin_type'].lower() in st.lower():
                    boost += 0.35
        
        if summary.get('hair_type'):
            for ht in hair_types:
                if summary['hair_type'].lower() in ht.lower():
                    boost += 0.35
        
        return min(boost, 0.6)  # Cap at 0.6

    def _compute_product_score(self, product: Dict, similarity: float) -> float:
        """Compute final product score"""
        pop = normalize(product.get('popularity', 0.5))
        stock = normalize(product.get('stock', 0), min_val=0, max_val=100)
        recency = normalize(product.get('recency', 0.5))
        personal = normalize(product.get('personal', 0.0))
        seller_boost = product.get('seller_boost', 0.0)
        
        score = compute_score(
            sim=similarity,
            cat=1.0,  # Already filtered
            pop=pop,
            stock=stock,
            recency=recency,
            personal=personal,
            seller_boost=seller_boost
        )
        
        return score

    def _apply_business_rules(self, results: List[Dict], summary: Dict, return_metadata: bool = False) -> tuple:
        """Apply business rules for filtering and ranking"""
        filtered = []
        
        # Initialize metadata
        metadata = {
            'warnings': [],
            'budget_info': {
                'requested_budget': summary.get('budget'),
                'cheapest_available': None,
                'products_in_budget': 0,
                'products_over_budget': 0,
                'budget_type': None
            }
        }
        
        # Extract user criteria for strict filtering
        skin_type = summary.get('skin_type', '').lower()
        hair_type = summary.get('hair_type', '').lower()
        category = summary.get('category', '').lower()
        problem = summary.get('problem', '').lower()
        
        # Extract constraints
        budget = summary.get('budget', '')
        age = summary.get('age')
        gender = summary.get('gender', '').lower()
        
        # Track all product prices for budget analysis
        all_prices = [r['product'].get('price', 0) for r in results]
        if all_prices:
            metadata['budget_info']['cheapest_available'] = min(all_prices)
            metadata['budget_info']['most_expensive'] = max(all_prices)
            metadata['budget_info']['average_price'] = sum(all_prices) / len(all_prices)
        
        # Parse budget - can be numeric or categorical
        budget_numeric = None
        budget_category = None
        
        if budget:
            if isinstance(budget, (int, float)):
                budget_numeric = float(budget)
                metadata['budget_info']['budget_type'] = 'numeric'
            elif isinstance(budget, str):
                # Try to extract numeric value
                import re
                budget_str = budget.lower().replace(',', '').replace('da', '').replace('dinar', '').strip()
                # Check for numeric value
                numeric_match = re.search(r'(\d+)', budget_str)
                if numeric_match:
                    budget_numeric = float(numeric_match.group(1))
                    metadata['budget_info']['budget_type'] = 'numeric'
                # Check for category keywords
                elif any(keyword in budget_str for keyword in ['low', 'cheap', 'affordable', 'budget']):
                    budget_category = 'low'
                    metadata['budget_info']['budget_type'] = 'categorical'
                elif any(keyword in budget_str for keyword in ['high', 'expensive', 'premium', 'luxury']):
                    budget_category = 'high'
                    metadata['budget_info']['budget_type'] = 'categorical'
                elif any(keyword in budget_str for keyword in ['medium', 'moderate', 'average', 'mid']):
                    budget_category = 'medium'
                    metadata['budget_info']['budget_type'] = 'categorical'
        
        # Track budget statistics
        skipped_by_budget = 0
        penalized_by_budget = 0
        
        for result in results:
            product = result['product']
            product_price = product.get('price', 0)
            
            # STRICT FILTER: Skin type - if user specifies skin type, product MUST support it
            if skin_type:
                product_skin_types = [st.lower() for st in product.get('skin_types', [])]
                # If product has skin type restrictions and user's type is not supported, SKIP
                if product_skin_types and 'all' not in product_skin_types:
                    if not any(skin_type in st or st in skin_type for st in product_skin_types):
                        continue  # Skip products that don't match skin type
            
            # STRICT FILTER: Hair type - if user specifies hair type, product MUST support it
            if hair_type:
                product_hair_types = [ht.lower() for ht in product.get('hair_types', [])]
                # If product has hair type restrictions and user's type is not supported, SKIP
                if product_hair_types and 'all' not in product_hair_types:
                    if not any(hair_type in ht or ht in hair_type for ht in product_hair_types):
                        continue  # Skip products that don't match hair type
            
            # STRICT FILTER: Category - if user specifies category, product MUST match
            if category:
                product_category = product.get('category', '').lower()
                if category not in product_category and product_category not in category:
                    continue  # Skip products from wrong category
            
            # Track original state before budget filter
            was_skipped = False
            was_penalized = False
            
            # Budget filter - numeric approach
            if budget_numeric is not None:
                price_ratio = product_price / budget_numeric
                
                # Track budget conformance
                if price_ratio <= 1.0:
                    metadata['budget_info']['products_in_budget'] = metadata['budget_info'].get('products_in_budget', 0) + 1
                else:
                    metadata['budget_info']['products_over_budget'] = metadata['budget_info'].get('products_over_budget', 0) + 1
                
                if price_ratio > 1.5:  # More than 50% over budget
                    skipped_by_budget += 1
                    was_skipped = True
                    # DON'T continue here - we'll add with warning instead
                elif price_ratio > 1.2:  # 20-50% over budget
                    result['score'] *= 0.6  # Heavy penalty
                elif price_ratio > 1.0:  # Slightly over budget
                    result['score'] *= 0.8  # Medium penalty
                elif price_ratio >= 0.8:  # Within budget range
                    result['score'] *= 1.1  # Small boost
                elif price_ratio >= 0.5:  # Good value
                    result['score'] *= 1.05  # Slight boost
                # Very cheap products (< 50% of budget) - no penalty or boost
            
            # Budget filter - categorical approach
            elif budget_category:
                product_budget = product.get('budget', '').lower()
                
                # Define price ranges for categories based on actual prices
                if budget_category == 'low':
                    if product_price > 3000:  # Hard limit for low budget
                        continue
                    elif product_budget == 'high':
                        continue
                    elif product_budget == 'medium':
                        result['score'] *= 0.7
                
                elif budget_category == 'medium':
                    if product_price > 5000:  # Hard limit for medium budget
                        result['score'] *= 0.5
                    elif product_budget == 'high':
                        result['score'] *= 0.8
                
                elif budget_category == 'high':
                    # No restrictions for high budget
                    # Prefer premium products
                    if product_budget == 'high':
                        result['score'] *= 1.1
            
            # Age range filter (soft filter - penalize if not matching)
            if age:
                age_ranges = product.get('age_range', [])
                if age_ranges:
                    age_match = False
                    try:
                        age_num = int(age)
                        for age_range in age_ranges:
                            if '-' in age_range:
                                min_age, max_age = age_range.split('-')
                                if min_age.endswith('+'):
                                    if age_num >= int(min_age.replace('+', '')):
                                        age_match = True
                                elif max_age.endswith('+'):
                                    if age_num >= int(max_age.replace('+', '')):
                                        age_match = True
                                else:
                                    if int(min_age) <= age_num <= int(max_age):
                                        age_match = True
                    except:
                        pass
                    
                    if not age_match:
                        result['score'] *= 0.7  # Penalty for age mismatch
            
            # Gender filter (soft filter)
            if gender:
                product_genders = [g.lower() for g in product.get('gender', [])]
                if 'unisex' not in product_genders and gender not in product_genders:
                    result['score'] *= 0.8
            
            filtered.append(result)
        
        # Generate warnings based on budget analysis
        if budget_numeric is not None and metadata['budget_info']['products_in_budget'] == 0:
            metadata['warnings'].append({
                'type': 'budget',
                'severity': 'high',
                'message': f'No products found within budget of {budget_numeric} DA. Showing closest alternatives.',
                'suggestion': f'Consider increasing budget to at least {metadata["budget_info"]["cheapest_available"]} DA'
            })
        elif budget_numeric is not None and skipped_by_budget > 0:
            metadata['warnings'].append({
                'type': 'budget',
                'severity': 'medium',
                'message': f'{skipped_by_budget} products were too far over budget (>50% more).',
                'suggestion': f'Cheapest available product: {metadata["budget_info"]["cheapest_available"]} DA'
            })
        
        # Warning if very few results
        if len(filtered) < 3 and len(results) > 5:
            metadata['warnings'].append({
                'type': 'filtering',
                'severity': 'medium',
                'message': f'Only {len(filtered)} products match your criteria. Consider relaxing some filters.',
                'suggestion': 'Try removing skin_type, hair_type, or category filters for more results'
            })
        
        # Re-sort after applying penalties
        filtered.sort(key=lambda x: x['score'], reverse=True)
        
        if return_metadata:
            return filtered, metadata
        return filtered

    def _format_recommendations(self, results: List[Dict], summary: Dict, language: str = 'en') -> List[Dict]:
        """Format final recommendations with localized content"""
        recommendations = []
        
        for result in results:
            product = result['product']
            
            # Select name based on language
            if language == 'ar':
                name = product.get('name_ar', product['name'])
                description = product.get('description_ar', product['description'])
            elif language == 'fr':
                name = product.get('name_fr', product['name'])
                description = product.get('description_fr', product['description'])
            else:
                name = product['name']
                description = product['description']
            
            # Generate reason
            reason = self._generate_reason(product, summary, language)
            
            recommendations.append({
                'id': product['id'],
                'name': name,
                'price': product['price'],
                'currency': product.get('currency', 'DA'),
                'image': product.get('image', ''),
                'tags': product.get('tags', []),
                'description': description,
                'reason': reason,
                'score': round(result['score'], 3),
                'category': product['category'],
                'subcategory': product.get('subcategory', '')
            })
        
        return recommendations

    def _generate_reason(self, product: Dict, summary: Dict, language: str = 'en') -> str:
        """Generate localized recommendation reason"""
        reasons = []
        
        # Skin type match
        if summary.get('skin_type'):
            skin_types = [st.lower() for st in product.get('skin_types', [])]
            if any(summary['skin_type'].lower() in st for st in skin_types):
                if language == 'ar':
                    reasons.append(f"مناسب لنوع بشرتك ({summary['skin_type']})")
                elif language == 'fr':
                    reasons.append(f"Adapté à votre type de peau ({summary['skin_type']})")
                else:
                    reasons.append(f"Perfect for your {summary['skin_type']} skin type")
        
        # Hair type match
        if summary.get('hair_type'):
            hair_types = [ht.lower() for ht in product.get('hair_types', [])]
            if any(summary['hair_type'].lower() in ht for ht in hair_types):
                if language == 'ar':
                    reasons.append(f"مثالي لنوع شعرك ({summary['hair_type']})")
                elif language == 'fr':
                    reasons.append(f"Idéal pour votre type de cheveux ({summary['hair_type']})")
                else:
                    reasons.append(f"Ideal for your {summary['hair_type']} hair type")
        
        # Problem match
        if summary.get('problem'):
            problems = [p.lower() for p in product.get('problems_solved', [])]
            if any(summary['problem'].lower() in p for p in problems):
                if language == 'ar':
                    reasons.append(f"يعالج مشكلة {summary['problem']}")
                elif language == 'fr':
                    reasons.append(f"Traite le problème de {summary['problem']}")
                else:
                    reasons.append(f"Addresses your {summary['problem']} concern")
        
        # Budget match - numeric
        budget = summary.get('budget')
        product_price = product.get('price', 0)
        
        if budget:
            import re
            budget_numeric = None
            
            if isinstance(budget, (int, float)):
                budget_numeric = float(budget)
            elif isinstance(budget, str):
                budget_str = budget.lower().replace(',', '').replace('da', '').replace('dinar', '').strip()
                numeric_match = re.search(r'(\d+)', budget_str)
                if numeric_match:
                    budget_numeric = float(numeric_match.group(1))
            
            if budget_numeric:
                if product_price <= budget_numeric:
                    if language == 'ar':
                        reasons.append(f"ضمن ميزانيتك ({product_price} DA)")
                    elif language == 'fr':
                        reasons.append(f"Dans votre budget ({product_price} DA)")
                    else:
                        reasons.append(f"Within your budget ({product_price} DA)")
                elif product_price <= budget_numeric * 1.2:
                    if language == 'ar':
                        reasons.append(f"قريب من ميزانيتك ({product_price} DA)")
                    elif language == 'fr':
                        reasons.append(f"Proche de votre budget ({product_price} DA)")
                    else:
                        reasons.append(f"Close to your budget ({product_price} DA)")
            else:
                # Categorical budget
                budget_category = summary.get('budget', '').lower()
                product_budget = product.get('budget', '').lower()
                if budget_category and budget_category == product_budget:
                    if language == 'ar':
                        reasons.append("يناسب ميزانيتك")
                    elif language == 'fr':
                        reasons.append("Correspond à votre budget")
                    else:
                        reasons.append("Fits your budget")
        
        # Default reason
        if not reasons:
            if language == 'ar':
                return f"منتج رائع من فئة {product['category']}"
            elif language == 'fr':
                return f"Excellent produit de la catégorie {product['category']}"
            else:
                return f"Highly recommended {product['category']} product"
        
        return ' • '.join(reasons)

    def get_products(self):
        """Get all products"""
        return self.products
    
    def get_stats(self):
        """Get catalog statistics"""
        total = len(self.products)
        in_stock = sum(1 for p in self.products if p.get('stock', 0) > 0)
        categories = {}
        for p in self.products:
            cat = p.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total_products': total,
            'in_stock': in_stock,
            'categories': categories,
            'index_type': type(self.index).__name__
        }
