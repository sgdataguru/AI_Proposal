"""
Purpose: Test data validation utility functions
Prerequisites: None (uses inline test data)
Expected: Validates data quality rules correctly
How to run: python agent-utils/dev-testing/utils/test_data_validation.py

Example test demonstrating how to validate data quality during development.
"""


def validate_not_null(series, column_name):
    """Check if a series has null values."""
    null_count = series.isna().sum()
    return {
        'column': column_name,
        'has_nulls': null_count > 0,
        'null_count': int(null_count),
        'total_rows': len(series)
    }


def validate_range(series, column_name, min_val=None, max_val=None):
    """Check if numeric values are within specified range."""
    valid_data = series.dropna()
    
    result = {
        'column': column_name,
        'in_range': True,
        'min_value': float(valid_data.min()) if len(valid_data) > 0 else None,
        'max_value': float(valid_data.max()) if len(valid_data) > 0 else None
    }
    
    if min_val is not None:
        result['in_range'] = result['in_range'] and (result['min_value'] >= min_val)
    if max_val is not None:
        result['in_range'] = result['in_range'] and (result['max_value'] <= max_val)
    
    return result


def validate_allowed_values(series, column_name, allowed_values):
    """Check if all values are in the allowed set."""
    valid_data = series.dropna()
    invalid_values = set(valid_data) - set(allowed_values)
    
    return {
        'column': column_name,
        'all_valid': len(invalid_values) == 0,
        'invalid_values': list(invalid_values),
        'invalid_count': sum(valid_data.isin(invalid_values))
    }


def run_tests():
    """Run validation tests with sample data."""
    import pandas as pd
    
    print("Testing data validation functions...\n")
    
    # Sample test data
    test_data = pd.DataFrame({
        'lead_id': ['L001', 'L002', 'L003', None, 'L005'],
        'score': [85, 92, 78, 88, 150],  # Note: 150 is out of range
        'category': ['hot', 'warm', 'hot', 'cold', 'invalid'],  # Note: 'invalid' not allowed
        'revenue': [10000.50, 25000.00, 15000.75, None, 30000.00]
    })
    
    # Test 1: Null validation
    print("Test 1: Null Validation")
    null_result = validate_not_null(test_data['lead_id'], 'lead_id')
    print(f"  Column: {null_result['column']}")
    print(f"  Has nulls: {null_result['has_nulls']}")
    print(f"  Null count: {null_result['null_count']}/{null_result['total_rows']}")
    assert null_result['has_nulls'] == True, "Expected to find null values"
    assert null_result['null_count'] == 1, "Expected exactly 1 null value"
    print("  ✅ Null validation test passed\n")
    
    # Test 2: Range validation
    print("Test 2: Range Validation (0-100)")
    range_result = validate_range(test_data['score'], 'score', min_val=0, max_val=100)
    print(f"  Column: {range_result['column']}")
    print(f"  In range: {range_result['in_range']}")
    print(f"  Min: {range_result['min_value']}, Max: {range_result['max_value']}")
    assert range_result['in_range'] == False, "Expected out of range value (150)"
    print("  ✅ Range validation test passed\n")
    
    # Test 3: Allowed values validation
    print("Test 3: Allowed Values Validation")
    allowed_result = validate_allowed_values(
        test_data['category'], 
        'category', 
        allowed_values=['hot', 'warm', 'cold']
    )
    print(f"  Column: {allowed_result['column']}")
    print(f"  All valid: {allowed_result['all_valid']}")
    print(f"  Invalid values: {allowed_result['invalid_values']}")
    print(f"  Invalid count: {allowed_result['invalid_count']}")
    assert allowed_result['all_valid'] == False, "Expected invalid value 'invalid'"
    assert 'invalid' in allowed_result['invalid_values'], "Expected 'invalid' in results"
    print("  ✅ Allowed values validation test passed\n")
    
    # Test 4: Null validation on column with nulls
    print("Test 4: Null Validation on Revenue Column")
    revenue_null_result = validate_not_null(test_data['revenue'], 'revenue')
    print(f"  Column: {revenue_null_result['column']}")
    print(f"  Has nulls: {revenue_null_result['has_nulls']}")
    assert revenue_null_result['has_nulls'] == True, "Expected null in revenue"
    print("  ✅ Revenue null validation test passed\n")
    
    print("=" * 50)
    print("✅ All data validation tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        run_tests()
    except ImportError as e:
        print(f"⚠️  Missing dependency: {e}")
        print("This test requires pandas. Install with: pip install pandas")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
