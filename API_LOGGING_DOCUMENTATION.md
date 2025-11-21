# API Logging Documentation

## Overview

The intelligent recommendation system now includes comprehensive logging for all API endpoints. Every API call is logged with detailed information, making it easy to monitor system activity, debug issues, and track usage patterns.

## What Gets Logged

### For All Endpoints

Each API call logs:
- 📥 **Incoming Request Marker**: Clear visual separator with timestamp
- **Endpoint**: The specific endpoint being called
- **Parameters**: All request parameters and their values
- **Response**: Summary of the response (success/failure, counts, etc.)
- **Timestamp**: Exact time of the request (YYYY-MM-DD HH:MM:SS)

### Endpoint-Specific Logging

#### 1. `/recommend` Endpoint

**Logs:**
- Category
- Needs
- Skin conditions
- Medical conditions
- Items to avoid
- Budget
- Age
- Preferences
- Query (natural language)
- Top K (number of results)
- Language

**Example Log Output:**
```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:30:45
================================================================================
Endpoint: POST /recommend
Request Data:
  - Category: health_supplements
  - Needs: ['energy', 'immunity']
  - Skin Conditions: None
  - Medical Conditions: ['diabetes', 'anemia']
  - Avoid: ['sugar']
  - Budget: 5000
  - Age: None
  - Preferences: None
  - Query: None
  - Top K: 3
  - Language: en
================================================================================

✅ RESPONSE: 3 recommendations returned
================================================================================
```

#### 2. `/product/{product_id}` Endpoint

**Logs:**
- Product ID being looked up

**Example Log Output (Success):**
```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:31:20
================================================================================
Endpoint: GET /product/supp-001
Product ID: supp-001
================================================================================

✅ RESPONSE: Product 'Sugar-Free Multivitamin for Diabetics' found
================================================================================
```

**Example Log Output (Not Found):**
```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:31:25
================================================================================
Endpoint: GET /product/xyz-999
Product ID: xyz-999
================================================================================

⚠️  RESPONSE: Product with ID 'xyz-999' not found (404)
================================================================================
```

#### 3. `/product/search/{search_term}` Endpoint

**Logs:**
- Search term

**Example Log Output (Success):**
```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:32:10
================================================================================
Endpoint: GET /product/search/vitamin
Search Term: vitamin
================================================================================

✅ RESPONSE: 2 products found matching 'vitamin'
================================================================================
```

**Example Log Output (No Results):**
```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:32:15
================================================================================
Endpoint: GET /product/search/nonexistent
Search Term: nonexistent
================================================================================

⚠️  RESPONSE: No products found matching 'nonexistent'
================================================================================
```

### Error Logging

When errors occur, detailed error information is logged:

```
================================================================================
📥 INCOMING API CALL - 2024-01-15 14:33:00
================================================================================
Endpoint: POST /recommend
Request Data:
  ...
================================================================================

❌ ERROR: Invalid category: xyz
Traceback (most recent call last):
  ...
================================================================================
```

## Log Symbols Reference

| Symbol | Meaning |
|--------|---------|
| 📥 | Incoming API call |
| ✅ | Successful response |
| ⚠️  | Warning (e.g., not found, no results) |
| ❌ | Error occurred |

## Testing the Logging

### Method 1: Using the Test Script

Run the automated test script to see logging in action:

```bash
# Make sure server is running
./start_server.sh

# In another terminal
python test_logging.py
```

This will make multiple API calls and you'll see detailed logs in the server console.

### Method 2: Manual Testing

#### Test /recommend logging:
```bash
curl -X POST "http://localhost:4708/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "health_supplements",
    "medical_conditions": ["diabetes"],
    "top_k": 3
  }'
```

#### Test /product/{product_id} logging:
```bash
# Existing product
curl "http://localhost:4708/product/supp-001"

# Non-existent product
curl "http://localhost:4708/product/xyz-999"
```

#### Test /product/search/{search_term} logging:
```bash
# Products found
curl "http://localhost:4708/product/search/vitamin"

# No products found
curl "http://localhost:4708/product/search/nonexistent"
```

### Method 3: Using Python Requests

```python
import requests

# Test /recommend
response = requests.post("http://localhost:4708/recommend", json={
    "category": "health_supplements",
    "needs": ["energy"],
    "top_k": 3
})

# Test /product/{product_id}
response = requests.get("http://localhost:4708/product/supp-001")

# Test /product/search/{search_term}
response = requests.get("http://localhost:4708/product/search/baby")
```

## Benefits of API Logging

### 1. **Debugging**
- Quickly identify what parameters are being sent
- See exact timestamps of requests
- Track errors with full stack traces

### 2. **Monitoring**
- Monitor API usage in real-time
- Identify popular endpoints and search terms
- Track response times and success rates

### 3. **Analytics**
- Analyze user behavior and search patterns
- Identify common medical conditions and needs
- Optimize product catalog based on searches

### 4. **Security**
- Detect unusual API access patterns
- Monitor for potential abuse
- Track failed requests

## Log File Management

### Current Setup
- Logs are printed to **stdout** (console)
- When running with `uvicorn`, logs appear in the terminal
- When running as a service, logs can be captured to a file

### Redirecting Logs to File

To save logs to a file:

```bash
# Run server and save logs
python app.py > logs/api_$(date +%Y%m%d_%H%M%S).log 2>&1
```

Or modify `start_server.sh`:

```bash
#!/bin/bash
mkdir -p logs
LOG_FILE="logs/api_$(date +%Y%m%d_%H%M%S).log"
echo "Starting server... (logs: $LOG_FILE)"
python app.py > "$LOG_FILE" 2>&1
```

### Log Rotation

For production use, implement log rotation:

```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

# Configure rotating file handler
handler = RotatingFileHandler(
    'logs/api.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler, logging.StreamHandler()]
)
```

## Advanced Usage

### Filtering Logs

Use `grep` to filter specific types of logs:

```bash
# Only show incoming requests
tail -f logs/api.log | grep "📥 INCOMING"

# Only show errors
tail -f logs/api.log | grep "❌ ERROR"

# Only show /recommend endpoint calls
tail -f logs/api.log | grep "POST /recommend"

# Show all product searches
tail -f logs/api.log | grep "/product/search"
```

### Analyzing Logs

Extract useful statistics from logs:

```bash
# Count total API calls today
grep "📥 INCOMING" logs/api_*.log | wc -l

# Count calls per endpoint
grep "Endpoint:" logs/api_*.log | sort | uniq -c

# Find most searched terms
grep "Search Term:" logs/api_*.log | sort | uniq -c | sort -rn

# Find most requested product IDs
grep "Product ID:" logs/api_*.log | sort | uniq -c | sort -rn
```

## Privacy Considerations

**Current Implementation:**
- Logs contain request parameters but no personal user data
- No IP addresses or authentication tokens are logged
- Safe for development and testing

**For Production:**
- Consider adding user/session IDs for tracking (if privacy-compliant)
- Implement log anonymization if needed
- Follow GDPR/privacy regulations for log retention
- Consider PII (Personal Identifiable Information) masking

## Future Enhancements

Potential logging improvements:

1. **Structured Logging**: Use JSON format for machine parsing
2. **Performance Metrics**: Log response times and latency
3. **User Analytics**: Track user sessions and behavior
4. **Alert System**: Auto-alert on errors or unusual patterns
5. **Dashboard**: Web UI to view logs and analytics
6. **Log Aggregation**: Integration with ELK stack or similar

## Troubleshooting

### Logs Not Appearing

**Issue**: Server is running but no logs are shown

**Solution**:
1. Check if server is running in background mode
2. Make sure you're looking at the correct terminal
3. Verify the server started successfully: `curl http://localhost:4708/health`

### Too Many Logs

**Issue**: Console is flooded with logs

**Solution**:
1. Redirect logs to file (see Log File Management above)
2. Implement log levels (INFO, DEBUG, ERROR)
3. Use log filtering with `grep`

### Logs Missing Information

**Issue**: Some parameters not showing in logs

**Solution**:
1. Check that parameters are being sent correctly
2. Verify API request format matches documentation
3. Test with example requests from `api_examples.py`

## Summary

The API logging system provides:
- ✅ Complete visibility into all API calls
- ✅ Clear, readable log format with symbols
- ✅ Detailed request and response information
- ✅ Error tracking with stack traces
- ✅ Timestamp for every request
- ✅ Easy to test and verify
- ✅ Production-ready with file output options

For questions or issues with logging, refer to this documentation or run `test_logging.py` to see examples.
