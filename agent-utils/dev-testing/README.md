# Agent Development Testing Directory

## Purpose

This directory contains quick, isolated tests created during the implementation of data platform features. These tests are designed to verify individual methods, functions, or components work as intended during development.

## Overview

During implementation, agents should create small, focused tests that can be run independently to ensure specific functionality works correctly. These tests complement the main test suite and provide:

1. **Rapid Feedback** - Quick verification during development
2. **Isolation** - Test individual components without full system setup
3. **Documentation** - Examples of how components should be used
4. **Debugging Aid** - Reproducible test cases for troubleshooting

## Directory Structure

```
agent-utils/dev-testing/
├── README.md                           # This file
├── pipelines/                          # Pipeline component tests
│   ├── test_ingestion_logic.py        # Example: Test data ingestion functions
│   └── test_transformation.py         # Example: Test data transformation logic
├── dbt/                                # dbt model tests
│   ├── test_bronze_model.sql          # Example: Bronze layer model test
│   └── test_silver_model.sql          # Example: Silver layer model test
├── api/                                # API and service tests
│   ├── test_data_service.py           # Example: Test data service methods
│   └── test_api_endpoints.py          # Example: Test API endpoints
├── infrastructure/                     # Infrastructure tests
│   ├── test_bicep_template.sh         # Example: Test Bicep template validation
│   └── test_terraform_config.sh       # Example: Test Terraform configuration
└── utils/                              # Utility function tests
    └── test_helper_functions.py       # Example: Test utility functions
```

## Guidelines for Creating Tests

### 1. Test File Naming

- Use descriptive names that indicate what is being tested
- Follow naming conventions:
  - Python: `test_<component_name>.py`
  - SQL: `test_<model_name>.sql`
  - Shell: `test_<component_name>.sh`

### 2. Test Documentation

Each test file MUST include:
- Purpose statement at the top
- Prerequisites or setup instructions
- Expected outcomes
- How to run the test

### 3. Test Structure

```python
"""
Purpose: Test the lead scoring data transformation logic
Prerequisites: Sample input data in JSON format
Expected: Transformed data with calculated scores
How to run: python test_lead_scoring_transform.py
"""

# Test implementation here
```

### 4. Self-Contained Tests

Tests should be as self-contained as possible:
- Include sample data inline or reference small test data files
- Avoid dependencies on full database or infrastructure setup
- Mock external services when necessary
- Can run without extensive configuration

### 5. Quick Execution

Tests should execute quickly:
- Target execution time: < 5 seconds for most tests
- < 30 seconds for integration-style tests
- Use minimal data samples

## Example Test Templates

### Python Function Test

```python
"""
Purpose: Test the data quality validation function
Prerequisites: None (uses inline test data)
Expected: Returns validation results with pass/fail status
How to run: python agent-utils/dev-testing/utils/test_data_quality.py
"""

def validate_data_quality(df, rules):
    """Validate data quality based on rules."""
    # Implementation would be here
    pass

if __name__ == "__main__":
    import pandas as pd
    
    # Sample test data
    test_data = pd.DataFrame({
        'id': [1, 2, 3, None],
        'score': [85, 92, 78, 88],
        'category': ['A', 'B', 'A', 'C']
    })
    
    # Test rules
    rules = {
        'id': {'not_null': True},
        'score': {'min': 0, 'max': 100},
        'category': {'allowed_values': ['A', 'B', 'C']}
    }
    
    # Run validation
    result = validate_data_quality(test_data, rules)
    
    # Verify results
    assert result['id']['has_nulls'] == True, "Expected null detection to fail"
    assert result['score']['in_range'] == True, "Expected score range check to pass"
    
    print("✅ All tests passed!")
```

### SQL Model Test

```sql
-- Purpose: Test the bronze to silver transformation for lead data
-- Prerequisites: None (uses CTE test data)
-- Expected: Clean data with standardized formats
-- How to run: Run this query in Synapse/database query editor

WITH test_data AS (
    SELECT 
        'lead-001' as lead_id,
        'john.doe@example.com' as email,
        '2024-01-15' as created_date,
        85 as score
    UNION ALL
    SELECT 
        'lead-002',
        'jane.smith@example.com',
        '2024-01-16',
        92
)
SELECT 
    lead_id,
    LOWER(email) as email_normalized,
    CAST(created_date AS DATE) as created_date,
    score,
    CASE 
        WHEN score >= 80 THEN 'hot'
        WHEN score >= 60 THEN 'warm'
        ELSE 'cold'
    END as lead_temperature
FROM test_data;

-- Expected output:
-- lead_id  | email_normalized         | created_date | score | lead_temperature
-- lead-001 | john.doe@example.com     | 2024-01-15   | 85    | hot
-- lead-002 | jane.smith@example.com   | 2024-01-16   | 92    | hot
```

### Shell Script Test

```bash
#!/bin/bash
# Purpose: Test Bicep template syntax validation
# Prerequisites: Azure CLI installed
# Expected: No syntax errors in Bicep template
# How to run: bash agent-utils/dev-testing/infrastructure/test_bicep_validation.sh

set -e

echo "Testing Bicep template validation..."

# Test file path
TEMPLATE_PATH="infra/main.bicep"

# Validate syntax
if az bicep build --file "$TEMPLATE_PATH" --stdout > /dev/null 2>&1; then
    echo "✅ Bicep template validation passed"
else
    echo "❌ Bicep template validation failed"
    exit 1
fi

echo "All infrastructure tests passed!"
```

## Best Practices

1. **Keep Tests Simple** - Focus on one aspect of functionality
2. **Use Clear Assertions** - Make expected outcomes explicit
3. **Document Assumptions** - Note any prerequisites or constraints
4. **Clean Up After Tests** - Remove temporary files/data
5. **Version Control** - Commit useful tests that may help future development
6. **Update as Needed** - Modify tests when implementation changes

## Integration with Main Test Suite

These development tests are **supplementary** to the main test suite:

- Main tests (`tests/` directory): Comprehensive, part of CI/CD
- Dev tests (`agent-utils/dev-testing/`): Quick, isolated, development-focused

Some dev tests may graduate to the main test suite if they prove valuable for regression testing.

## Cleanup Policy

- Keep tests that document important edge cases or tricky logic
- Remove tests that are no longer relevant after implementation is complete
- Archive tests that may be useful as examples

## See Also

- [User Stories Documentation Guidelines](../../.github/instructions/docs/user-stories.instructions.md)
- [Testing Strategy in Implementation Plans](../../.github/prompts/gen-e2/5-generate-implementation-plan.prompt.md)
- [Execution Prompt](../../.github/prompts/gen-e2/6-execute-plan.prompt.md)
