#!/bin/bash

# JARVIS AI - Integration Test Suite
# Tests all major components and API endpoints

echo "🧪 JARVIS AI Integration Tests"
echo "==============================="
echo ""

API_URL="http://localhost:8000"
BACKEND_PID=""
FRONTEND_PID=""
TEST_PASSED=0
TEST_FAILED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print test result
print_result() {
    local test_name=$1
    local result=$2
    if [ $result -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $test_name"
        ((TEST_PASSED++))
    else
        echo -e "${RED}✗${NC} $test_name"
        ((TEST_FAILED++))
    fi
}

# Check if backend is running
echo "📡 Checking backend..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/health" 2>/dev/null)

if [ "$response" = "200" ]; then
    print_result "Backend Health Check" 0
else
    print_result "Backend Health Check" 1
    echo -e "${YELLOW}ℹ${NC} Make sure backend is running: python backend/main.py"
    exit 1
fi

echo ""
echo "🔍 Running API Tests..."
echo ""

# Test 1: Health endpoint
echo "Test 1: GET /health"
response=$(curl -s "$API_URL/health")
echo "Response: $response"
echo ""

# Test 2: Models endpoint
echo "Test 2: GET /models"
response=$(curl -s "$API_URL/models")
echo "Response: $response"
echo ""

# Test 3: Simple query (Groq)
echo "Test 3: POST /query (Simple - Groq)"
response=$(curl -s -X POST "$API_URL/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 2+2?", "force_groq": true}')
echo "Response: $response"
if echo "$response" | grep -q "success"; then
    print_result "Simple Query (Groq)" 0
else
    print_result "Simple Query (Groq)" 1
fi
echo ""

# Test 4: Complex query (Gemini)
echo "Test 4: POST /query (Complex - Gemini)"
response=$(curl -s -X POST "$API_URL/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum computing", "force_gemini": true}')
echo "Response: $response"
if echo "$response" | grep -q "success"; then
    print_result "Complex Query (Gemini)" 0
else
    print_result "Complex Query (Gemini)" 1
fi
echo ""

# Test 5: PC Control (Mock)
echo "Test 5: POST /action (PC Control)"
response=$(curl -s -X POST "$API_URL/action" \
  -H "Content-Type: application/json" \
  -d '{"action": "pc_control", "params": {"action_type": "screenshot", "filename": "test.png"}}')
echo "Response: $response"
if echo "$response" | grep -q "success"; then
    print_result "PC Control Action" 0
else
    print_result "PC Control Action" 1
fi
echo ""

# Test Summary
echo "==============================="
echo "📊 Test Summary"
echo "==============================="
echo -e "${GREEN}Passed: $TEST_PASSED${NC}"
echo -e "${RED}Failed: $TEST_FAILED${NC}"
echo ""

if [ $TEST_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
