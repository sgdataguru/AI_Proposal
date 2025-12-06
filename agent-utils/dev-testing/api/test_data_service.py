"""
Purpose: Test API data service methods (mock-based)
Prerequisites: None (uses mock data and functions)
Expected: Service methods handle data correctly
How to run: python agent-utils/dev-testing/api/test_data_service.py

Example test demonstrating API service testing with mocked responses.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional


class DataService:
    """Mock data service for testing."""
    
    def __init__(self):
        self.cache = {}
    
    def fetch_lead_scores(self, date_range: Optional[tuple] = None) -> List[Dict]:
        """
        Fetch lead scores within date range.
        
        Args:
            date_range: Tuple of (start_date, end_date) as datetime objects
            
        Returns:
            List of lead score records
        """
        # Mock data
        all_leads = [
            {
                'lead_id': 'L001',
                'score': 85,
                'category': 'hot',
                'scored_at': datetime.now() - timedelta(days=1)
            },
            {
                'lead_id': 'L002',
                'score': 65,
                'category': 'warm',
                'scored_at': datetime.now() - timedelta(days=2)
            },
            {
                'lead_id': 'L003',
                'score': 45,
                'category': 'cool',
                'scored_at': datetime.now() - timedelta(days=5)
            },
            {
                'lead_id': 'L004',
                'score': 25,
                'category': 'cold',
                'scored_at': datetime.now() - timedelta(days=10)
            }
        ]
        
        if date_range:
            start_date, end_date = date_range
            filtered_leads = [
                lead for lead in all_leads
                if start_date <= lead['scored_at'] <= end_date
            ]
            return filtered_leads
        
        return all_leads
    
    def get_lead_by_id(self, lead_id: str) -> Optional[Dict]:
        """
        Get single lead by ID.
        
        Args:
            lead_id: Lead identifier
            
        Returns:
            Lead record or None if not found
        """
        leads = self.fetch_lead_scores()
        for lead in leads:
            if lead['lead_id'] == lead_id:
                return lead
        return None
    
    def aggregate_scores(self, leads: List[Dict], group_by: str = 'category') -> Dict:
        """
        Aggregate lead scores by category.
        
        Args:
            leads: List of lead records
            group_by: Field to group by (default: 'category')
            
        Returns:
            Dictionary with aggregated statistics
        """
        if not leads:
            return {}
        
        groups = {}
        for lead in leads:
            key = lead.get(group_by, 'unknown')
            if key not in groups:
                groups[key] = {
                    'count': 0,
                    'total_score': 0,
                    'min_score': float('inf'),
                    'max_score': float('-inf')
                }
            
            groups[key]['count'] += 1
            groups[key]['total_score'] += lead['score']
            groups[key]['min_score'] = min(groups[key]['min_score'], lead['score'])
            groups[key]['max_score'] = max(groups[key]['max_score'], lead['score'])
        
        # Calculate averages
        for key in groups:
            groups[key]['avg_score'] = groups[key]['total_score'] / groups[key]['count']
        
        return groups


def run_tests():
    """Run data service tests."""
    print("Testing data service methods...\n")
    
    service = DataService()
    
    # Test 1: Fetch all leads
    print("Test 1: Fetch All Leads")
    all_leads = service.fetch_lead_scores()
    print(f"  Total leads fetched: {len(all_leads)}")
    assert len(all_leads) == 4, "Expected 4 leads"
    assert all(k in all_leads[0] for k in ['lead_id', 'score', 'category']), \
        "Expected all required fields"
    print("  ✅ Fetch all leads test passed\n")
    
    # Test 2: Fetch leads with date range
    print("Test 2: Fetch Leads with Date Range (last 3 days)")
    start_date = datetime.now() - timedelta(days=3)
    end_date = datetime.now()
    recent_leads = service.fetch_lead_scores(date_range=(start_date, end_date))
    print(f"  Recent leads (last 3 days): {len(recent_leads)}")
    assert len(recent_leads) == 2, "Expected 2 leads in last 3 days"
    print("  ✅ Date range filter test passed\n")
    
    # Test 3: Get lead by ID
    print("Test 3: Get Lead by ID")
    lead_id = 'L002'
    lead = service.get_lead_by_id(lead_id)
    print(f"  Found lead: {lead['lead_id']}")
    print(f"  Score: {lead['score']}")
    print(f"  Category: {lead['category']}")
    assert lead is not None, "Expected to find lead L002"
    assert lead['lead_id'] == lead_id, f"Expected lead_id {lead_id}"
    assert lead['score'] == 65, "Expected score 65"
    print("  ✅ Get lead by ID test passed\n")
    
    # Test 4: Get non-existent lead
    print("Test 4: Get Non-existent Lead")
    missing_lead = service.get_lead_by_id('L999')
    print(f"  Result: {missing_lead}")
    assert missing_lead is None, "Expected None for non-existent lead"
    print("  ✅ Non-existent lead test passed\n")
    
    # Test 5: Aggregate scores by category
    print("Test 5: Aggregate Scores by Category")
    aggregates = service.aggregate_scores(all_leads)
    print(f"  Categories: {list(aggregates.keys())}")
    
    # Verify hot category
    hot_stats = aggregates.get('hot')
    print(f"  Hot leads - Count: {hot_stats['count']}, Avg: {hot_stats['avg_score']:.1f}")
    assert hot_stats['count'] == 1, "Expected 1 hot lead"
    assert hot_stats['avg_score'] == 85, "Expected avg score 85"
    
    # Verify we have all categories
    expected_categories = {'hot', 'warm', 'cool', 'cold'}
    actual_categories = set(aggregates.keys())
    assert expected_categories == actual_categories, \
        f"Expected categories {expected_categories}, got {actual_categories}"
    
    print("  ✅ Aggregation test passed\n")
    
    # Test 6: Aggregate with empty list
    print("Test 6: Aggregate with Empty List")
    empty_aggregates = service.aggregate_scores([])
    print(f"  Result: {empty_aggregates}")
    assert empty_aggregates == {}, "Expected empty dict for empty input"
    print("  ✅ Empty aggregation test passed\n")
    
    print("=" * 50)
    print("✅ All data service tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
