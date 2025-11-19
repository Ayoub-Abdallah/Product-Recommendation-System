document.addEventListener('DOMContentLoaded', function() {
    // Handle beauty & health product recommendation form
    document.getElementById('beauty-form').onsubmit = function(e) {
        e.preventDefault();
        
        // Build summary object
        const summary = {};
        
        const skinType = document.getElementById('skin-type').value;
        if (skinType) summary.skin_type = skinType;
        
        const hairType = document.getElementById('hair-type').value;
        if (hairType) summary.hair_type = hairType;
        
        const category = document.getElementById('category').value;
        if (category) summary.category = category;
        
        const problem = document.getElementById('problem').value.trim();
        if (problem) summary.problem = problem;
        
        const budget = document.getElementById('budget').value.trim();
        if (budget) {
            // Try to parse as number, otherwise use as string
            const numBudget = parseFloat(budget);
            summary.budget = isNaN(numBudget) ? budget : numBudget;
        }
        
        const age = document.getElementById('age').value.trim();
        if (age) summary.age = age;
        
        const gender = document.getElementById('gender').value;
        if (gender) summary.gender = gender;
        
        const language = document.getElementById('language').value;
        const topK = parseInt(document.getElementById('top-k').value);
        
        // Call recommendation API
        fetch('/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                summary: summary,
                top_k: topK,
                language: language
            })
        })
        .then(r => r.json())
        .then(data => {
            displayRecommendations(data.recommendations, 'beauty', language);
        })
        .catch(err => {
            document.getElementById('recommendations').innerHTML = 
                `<div class="error">Error: ${err.message}</div>`;
        });
    };
});

function displayRecommendations(recommendations, type = 'legacy', language = 'en') {
    const recDiv = document.getElementById('recommendations');
    
    if (!recommendations || recommendations.length === 0) {
        recDiv.innerHTML = '<div class="no-results">No recommendations found. Try different criteria.</div>';
        return;
    }
    
    recDiv.innerHTML = '';
    
    // Add header
    const header = document.createElement('div');
    header.className = 'results-header';
    header.innerHTML = `<h3>Found ${recommendations.length} ${type === 'beauty' ? 'Beauty' : ''} Product(s)</h3>`;
    recDiv.appendChild(header);
    
    recommendations.forEach((rec, index) => {
        const div = document.createElement('div');
        div.className = 'recommendation';
        
        if (type === 'beauty') {
            // New beauty recommendation format with price
            div.innerHTML = `
                <div class="rec-header">
                    <span class="rec-number">${index + 1}</span>
                    <h4 class="rec-title">${rec.name}</h4>
                </div>
                <div class="rec-body">
                    <div class="rec-price">
                        <span class="price-label">Price:</span>
                        <span class="price-value">${rec.price} ${rec.currency || 'DA'}</span>
                    </div>
                    ${rec.category ? `<div class="rec-category">Category: ${rec.category}${rec.subcategory ? ' › ' + rec.subcategory : ''}</div>` : ''}
                    ${rec.description ? `<div class="rec-description">${rec.description}</div>` : ''}
                    <div class="rec-reason">
                        <span class="reason-icon">💡</span>
                        <span class="reason-text">${rec.reason}</span>
                    </div>
                    ${rec.tags && rec.tags.length > 0 ? `
                        <div class="rec-tags">
                            ${rec.tags.slice(0, 5).map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    <div class="rec-footer">
                        <span class="rec-score">Score: ${rec.score.toFixed(3)}</span>
                        <span class="rec-id">ID: ${rec.id}</span>
                    </div>
                </div>
            `;
        } else {
            // Legacy format with price (if available)
            const priceInfo = rec.price ? 
                `<div class="rec-price">
                    <span class="price-label">Price:</span>
                    <span class="price-value">${rec.price} DA</span>
                </div>` : '';
            
            div.innerHTML = `
                <div class="rec-header">
                    <span class="rec-number">${index + 1}</span>
                    <h4 class="rec-title">${rec.title}</h4>
                </div>
                <div class="rec-body">
                    ${priceInfo}
                    ${rec.category ? `<div class="rec-category">Category: ${rec.category}</div>` : ''}
                    <div class="rec-reason">
                        <span class="reason-icon">💡</span>
                        <span class="reason-text">${rec.reason}</span>
                    </div>
                    <div class="rec-footer">
                        <span class="rec-score">Score: ${rec.score.toFixed(3)}</span>
                        ${rec.similarity ? `<span class="rec-similarity">Similarity: ${rec.similarity.toFixed(3)}</span>` : ''}
                    </div>
                </div>
            `;
        }
        
        recDiv.appendChild(div);
    });
}
