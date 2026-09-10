# Comprehensive Testing Guide

## Quick Test

### 1. API Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "groq": "✓",
  "gemini": "✓"
}
```

### 2. Simple Query Test
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 2+2?", "force_groq": true}'
```

### 3. Complex Query Test
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum computing", "force_gemini": true}'
```

## Automated Testing

### Run Integration Tests
```bash
bash tests/test_api.sh
```

### Run with pytest (if installed)
```bash
pip install pytest pytest-asyncio
pytest tests/ -v
```

## Common Issues & Solutions

### Issue: "API Key not found"
**Solution:**
1. Check .env file exists: `ls -la .env`
2. Verify keys: `cat .env | grep API_KEY`
3. Restart backend: `python backend/main.py`

### Issue: "Connection refused"
**Solution:**
1. Backend not running: `python backend/main.py`
2. Port already in use: `lsof -ti:8000 | xargs kill -9`
3. Check firewall settings

### Issue: "Rate limit exceeded"
**Solution:**
- System automatically handles rate limits
- Implemented exponential backoff
- Check health endpoint: `curl http://localhost:8000/health`

### Issue: "Browser automation fails"
**Solution:**
1. Install Playwright: `pip install playwright`
2. Install browsers: `playwright install`
3. Check if browser is already running

## Performance Monitoring

### Check Health Metrics
```bash
curl http://localhost:8000/health | jq .metrics
```

### Monitor Response Times
Response times are tracked in the health endpoint:
- Under 1s: ✓ Excellent
- 1-3s: ✓ Good
- 3-5s: ⚠️  Acceptable
- Over 5s: ✗ Check rate limits

## Load Testing

### Simple Load Test (10 concurrent requests)
```bash
for i in {1..10}; do
  curl -X POST http://localhost:8000/query \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello"}' &
done
wait
```

### With Apache Bench (if installed)
```bash
ab -n 100 -c 10 http://localhost:8000/health
```
