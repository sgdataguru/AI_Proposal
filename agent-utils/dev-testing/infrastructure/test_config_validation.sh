#!/bin/bash
# Purpose: Test infrastructure configuration validation
# Prerequisites: None (validates configuration files exist and are well-formed)
# Expected: All infrastructure files pass basic validation
# How to run: bash agent-utils/dev-testing/infrastructure/test_config_validation.sh

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "=========================================="
echo "Infrastructure Configuration Tests"
echo "=========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_count=0
pass_count=0
fail_count=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    test_count=$((test_count + 1))
    echo "Test $test_count: $test_name"
    
    if eval "$test_command"; then
        echo -e "  ${GREEN}✅ PASS${NC}"
        pass_count=$((pass_count + 1))
    else
        echo -e "  ${RED}❌ FAIL${NC}"
        fail_count=$((fail_count + 1))
    fi
    echo ""
}

# Test 1: Check if infra directory exists
run_test "Infrastructure directory exists" \
    "[ -d '$PROJECT_ROOT/infra' ]"

# Test 2: Check for Terraform files
run_test "Terraform configuration files exist" \
    "[ -f '$PROJECT_ROOT/infra/main.tf' ] || [ -f '$PROJECT_ROOT/infra/terraform.tf' ] || [ -d '$PROJECT_ROOT/infra/terraform' ]"

# Test 3: Check for valid JSON in docker-compose
if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
    run_test "Docker Compose file is valid YAML" \
        "python3 -c 'import yaml; yaml.safe_load(open(\"$PROJECT_ROOT/docker-compose.yml\"))' 2>/dev/null"
else
    echo "Test $((test_count + 1)): Docker Compose file exists"
    echo -e "  ${YELLOW}⊘ SKIP (file not found)${NC}"
    echo ""
fi

# Test 4: Check for Terraform variable files
if [ -d "$PROJECT_ROOT/infra" ]; then
    run_test "Terraform variables or tfvars files exist" \
        "find '$PROJECT_ROOT/infra' -name '*.tfvars' -o -name 'variables.tf' | grep -q ."
fi

# Test 5: Check .gitignore includes common infrastructure artifacts
run_test ".gitignore includes infrastructure artifacts" \
    "grep -q 'terraform' '$PROJECT_ROOT/.gitignore' 2>/dev/null || grep -q '.tfstate' '$PROJECT_ROOT/.gitignore' 2>/dev/null"

# Test 6: Check for environment variable example file
run_test "Environment variable example file exists" \
    "[ -f '$PROJECT_ROOT/.env.example' ]"

# Test 7: Validate JSON files if any exist
if find "$PROJECT_ROOT/infra" -name "*.json" 2>/dev/null | grep -q .; then
    run_test "JSON configuration files are valid" \
        "find '$PROJECT_ROOT/infra' -name '*.json' -exec python3 -m json.tool {} \\; > /dev/null 2>&1"
else
    echo "Test $((test_count + 1)): JSON files are valid"
    echo -e "  ${YELLOW}⊘ SKIP (no JSON files found)${NC}"
    echo ""
fi

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Total tests: $test_count"
echo -e "Passed: ${GREEN}$pass_count${NC}"
echo -e "Failed: ${RED}$fail_count${NC}"
echo ""

if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}✅ All infrastructure configuration tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    exit 1
fi
