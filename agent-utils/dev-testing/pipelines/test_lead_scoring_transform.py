"""
Purpose: Test lead scoring transformation logic
Prerequisites: None (uses inline test data)
Expected: Correctly transforms and scores lead data
How to run: python agent-utils/dev-testing/pipelines/test_lead_scoring_transform.py

Example test for data transformation pipeline logic.
"""

from datetime import datetime, timedelta


def calculate_lead_score(lead_data):
    """
    Calculate lead score based on engagement metrics.
    
    Scoring rules:
    - Email opens: +5 points per open (max 25)
    - Link clicks: +10 points per click (max 40)
    - Form submissions: +15 points per submission (max 30)
    - Days since last activity: -1 point per day (max -20)
    
    Total possible: 100 points
    """
    score = 0
    
    # Email engagement
    email_opens = min(lead_data.get('email_opens', 0), 5)
    score += email_opens * 5
    
    # Click engagement
    link_clicks = min(lead_data.get('link_clicks', 0), 4)
    score += link_clicks * 10
    
    # Form submissions
    form_submissions = min(lead_data.get('form_submissions', 0), 2)
    score += form_submissions * 15
    
    # Recency penalty
    days_inactive = lead_data.get('days_since_last_activity', 0)
    recency_penalty = min(days_inactive, 20)
    score -= recency_penalty
    
    # Ensure score is between 0-100
    return max(0, min(100, score))


def categorize_lead(score):
    """Categorize lead based on score."""
    if score >= 80:
        return 'hot'
    elif score >= 60:
        return 'warm'
    elif score >= 40:
        return 'cool'
    else:
        return 'cold'


def transform_lead_data(raw_lead):
    """Transform raw lead data into scored lead record."""
    score = calculate_lead_score(raw_lead)
    category = categorize_lead(score)
    
    return {
        'lead_id': raw_lead['lead_id'],
        'email': raw_lead['email'].lower().strip(),
        'company': raw_lead.get('company', 'Unknown'),
        'score': score,
        'category': category,
        'email_opens': raw_lead.get('email_opens', 0),
        'link_clicks': raw_lead.get('link_clicks', 0),
        'form_submissions': raw_lead.get('form_submissions', 0),
        'days_since_last_activity': raw_lead.get('days_since_last_activity', 0),
        'scored_at': datetime.now().isoformat()
    }


def run_tests():
    """Run transformation tests."""
    print("Testing lead scoring transformation logic...\n")
    
    # Test Case 1: High engagement lead (should be 'hot')
    print("Test 1: High Engagement Lead")
    high_engagement = {
        'lead_id': 'L001',
        'email': 'JOHN.DOE@EXAMPLE.COM  ',  # Should be normalized
        'company': 'Acme Corp',
        'email_opens': 6,  # Will cap at 5
        'link_clicks': 4,  # Max for 40 points
        'form_submissions': 2,  # Max for 30 points
        'days_since_last_activity': 2
    }
    
    result1 = transform_lead_data(high_engagement)
    expected_score1 = (5*5) + (4*10) + (2*15) - 2  # 25+40+30-2 = 93
    
    print(f"  Lead ID: {result1['lead_id']}")
    print(f"  Email (normalized): {result1['email']}")
    print(f"  Score: {result1['score']} (expected: {expected_score1})")
    print(f"  Category: {result1['category']} (expected: hot)")
    
    assert result1['email'] == 'john.doe@example.com', "Email should be normalized"
    assert result1['score'] == expected_score1, f"Expected score {expected_score1}"
    assert result1['category'] == 'hot', "Expected 'hot' category"
    print("  ✅ High engagement test passed\n")
    
    # Test Case 2: Medium engagement lead (should be 'warm')
    print("Test 2: Medium Engagement Lead")
    medium_engagement = {
        'lead_id': 'L002',
        'email': 'jane.smith@example.com',
        'company': 'Tech Inc',
        'email_opens': 3,
        'link_clicks': 2,
        'form_submissions': 1,
        'days_since_last_activity': 5
    }
    
    result2 = transform_lead_data(medium_engagement)
    expected_score2 = (3*5) + (2*10) + (1*15) - 5  # 15+20+15-5 = 45
    
    print(f"  Lead ID: {result2['lead_id']}")
    print(f"  Score: {result2['score']} (expected: {expected_score2})")
    print(f"  Category: {result2['category']} (expected: cool)")
    
    assert result2['score'] == expected_score2, f"Expected score {expected_score2}"
    assert result2['category'] == 'cool', "Expected 'cool' category"
    print("  ✅ Medium engagement test passed\n")
    
    # Test Case 3: Low engagement lead (should be 'cold')
    print("Test 3: Low Engagement Lead")
    low_engagement = {
        'lead_id': 'L003',
        'email': 'inactive@example.com',
        'company': 'Old Co',
        'email_opens': 1,
        'link_clicks': 0,
        'form_submissions': 0,
        'days_since_last_activity': 15
    }
    
    result3 = transform_lead_data(low_engagement)
    expected_score3 = (1*5) - 15  # 5-15 = -10, capped at 0
    
    print(f"  Lead ID: {result3['lead_id']}")
    print(f"  Score: {result3['score']} (expected: {max(0, expected_score3)})")
    print(f"  Category: {result3['category']} (expected: cold)")
    
    assert result3['score'] == max(0, expected_score3), "Score should not go below 0"
    assert result3['category'] == 'cold', "Expected 'cold' category"
    print("  ✅ Low engagement test passed\n")
    
    # Test Case 4: No activity data (should handle gracefully)
    print("Test 4: Minimal Data Lead")
    minimal_data = {
        'lead_id': 'L004',
        'email': 'minimal@example.com'
    }
    
    result4 = transform_lead_data(minimal_data)
    
    print(f"  Lead ID: {result4['lead_id']}")
    print(f"  Company: {result4['company']} (expected: Unknown)")
    print(f"  Score: {result4['score']} (expected: 0)")
    print(f"  Category: {result4['category']} (expected: cold)")
    
    assert result4['company'] == 'Unknown', "Should default to 'Unknown'"
    assert result4['score'] == 0, "Should score 0 with no data"
    assert result4['category'] == 'cold', "Should be 'cold' with score 0"
    print("  ✅ Minimal data test passed\n")
    
    print("=" * 50)
    print("✅ All lead scoring transformation tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
