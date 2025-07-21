"""
Test request_db functionality - Collection analysis and database operations.
"""

import sys
import os
import tempfile
import csv
from unittest.mock import patch, MagicMock

# Fix imports for tests directory
from test_utils import fix_test_imports
fix_test_imports()

from request_db import (
    check_card_in_db,
    line_cleaner,
    get_cards_from_txt,
    get_cards_from_csv,
    request_owners,
    get_known_owners,
    get_set_stats,
    quick_rarity_comparison_by_owner
)


def test_card_checking():
    """Test card checking functionality."""
    print("🧪 Testing Card Checking...")
    
    # Sample database
    sample_db = [
        {"Name": "Lightning Bolt", "Set": "M21", "Owner": "TestUser"},
        {"Name": "Counterspell", "Set": "M21", "Owner": "OtherUser"},
        {"Name": "Giant Growth", "Set": "M21", "Owner": "TestUser"},
    ]
    
    # Test finding existing card
    result1 = check_card_in_db(sample_db, "Lightning Bolt")
    if result1:
        print("✅ Found existing card correctly")
    else:
        print("❌ Failed to find existing card")
    
    # Test finding card with specific owner
    result2 = check_card_in_db(sample_db, "Lightning Bolt", owner="TestUser")
    if result2:
        print("✅ Found card with correct owner")
    else:
        print("❌ Failed to find card with owner filter")
    
    # Test not finding card with wrong owner
    result3 = check_card_in_db(sample_db, "Lightning Bolt", owner="WrongUser")
    if not result3:
        print("✅ Correctly excluded card with wrong owner")
    else:
        print("❌ Found card with wrong owner (should not happen)")
    
    # Test card not in database
    result4 = check_card_in_db(sample_db, "Nonexistent Card")
    if not result4:
        print("✅ Correctly reported card not found")
    else:
        print("❌ Found nonexistent card (should not happen)")


def test_line_cleaner():
    """Test line cleaning functionality."""
    print("\n🧽 Testing Line Cleaning...")
    
    # Test basic cleaning
    dirty_lines = [
        "  Lightning Bolt  ",
        "\tCounterspell\n",
        "  Giant Growth\r\n  ",
        "",
        "   "
    ]
    
    cleaned = line_cleaner(dirty_lines)
    expected = ["Lightning Bolt", "Counterspell", "Giant Growth"]
    
    if cleaned == expected:
        print("✅ Line cleaning works correctly")
    else:
        print(f"❌ Line cleaning failed: expected {expected}, got {cleaned}")
    
    # Test with quantity prefixes (common in card lists)
    quantity_lines = [
        "1x Lightning Bolt",
        "4 Counterspell",
        "2x Giant Growth"
    ]
    
    quantity_cleaned = line_cleaner(quantity_lines)
    expected_quantity = ["Lightning Bolt", "Counterspell", "Giant Growth"]
    
    if quantity_cleaned == expected_quantity:
        print("✅ Quantity prefix removal works correctly")
    else:
        print(f"❌ Quantity cleaning failed: expected {expected_quantity}, got {quantity_cleaned}")


def test_file_processing():
    """Test file processing functions."""
    print("\n📁 Testing File Processing...")
    
    # Test TXT file processing
    txt_content = """Lightning Bolt
Counterspell
Giant Growth
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(txt_content)
        txt_file_path = f.name
    
    try:
        txt_cards = get_cards_from_txt(txt_file_path)
        expected_txt = ["Lightning Bolt", "Counterspell", "Giant Growth"]
        
        if txt_cards == expected_txt:
            print("✅ TXT file processing works correctly")
        else:
            print(f"❌ TXT processing failed: expected {expected_txt}, got {txt_cards}")
    finally:
        os.unlink(txt_file_path)
    
    # Test CSV file processing
    csv_data = [
        ["Name", "Set", "Rarity"],
        ["Lightning Bolt", "M21", "Common"],
        ["Counterspell", "M21", "Uncommon"],
        ["Giant Growth", "M21", "Common"]
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
        csv_file_path = f.name
    
    try:
        csv_cards = get_cards_from_csv(csv_file_path)
        expected_csv = ["Lightning Bolt", "Counterspell", "Giant Growth"]
        
        if csv_cards == expected_csv:
            print("✅ CSV file processing works correctly")
        else:
            print(f"❌ CSV processing failed: expected {expected_csv}, got {csv_cards}")
    finally:
        os.unlink(csv_file_path)


def test_owner_operations():
    """Test owner-related operations."""
    print("\n👤 Testing Owner Operations...")
    
    sample_collection = [
        {"Name": "Lightning Bolt", "Set": "M21", "Owner": "Alice"},
        {"Name": "Counterspell", "Set": "M21", "Owner": "Bob"},
        {"Name": "Giant Growth", "Set": "M21", "Owner": "Alice"},
        {"Name": "Dark Ritual", "Set": "M21", "Owner": "Charlie"},
    ]
    
    # Test getting known owners
    known_owners = get_known_owners(sample_collection)
    expected_owners = ["Alice", "Bob", "Charlie"]
    
    # Check if all expected owners are found (order may vary)
    if set(known_owners) == set(expected_owners):
        print("✅ Known owners extraction works correctly")
    else:
        print(f"❌ Owner extraction failed: expected {set(expected_owners)}, got {set(known_owners)}")
    
    # Test requesting owners for specific cards
    test_cards = ["Lightning Bolt", "Counterspell"]
    owners_result = request_owners(test_cards, sample_collection)
    
    if owners_result:
        print("✅ Owner request functionality works")
        
        # Check if it found the correct owners
        found_alice = any("Alice" in str(result) for result in owners_result)
        found_bob = any("Bob" in str(result) for result in owners_result)
        
        if found_alice and found_bob:
            print("✅ Found correct owners for requested cards")
        else:
            print("❌ Did not find expected owners")
    else:
        print("❌ Owner request returned no results")


def test_set_statistics():
    """Test set statistics functionality."""
    print("\n📊 Testing Set Statistics...")
    
    # Mock Scryfall API call for set stats
    mock_set_data = {
        "code": "MH3",
        "name": "Modern Horizons 3", 
        "card_count": 303,
        "released_at": "2024-06-14"
    }
    
    with patch('request_db.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_set_data
        mock_get.return_value = mock_response
        
        try:
            stats = get_set_stats("MH3")
            
            if stats and stats.get("name") == "Modern Horizons 3":
                print("✅ Set statistics retrieval works correctly")
            else:
                print(f"❌ Set stats failed: {stats}")
                
        except Exception as e:
            print(f"❌ Set statistics error: {e}")
    
    # Test with API error
    with patch('request_db.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        try:
            error_stats = get_set_stats("INVALID")
            if error_stats is None:
                print("✅ Handles API errors gracefully")
            else:
                print(f"❌ Should return None for API error, got: {error_stats}")
        except Exception as e:
            print(f"❌ API error handling failed: {e}")


def test_rarity_comparison():
    """Test rarity comparison functionality."""
    print("\n💎 Testing Rarity Comparison...")
    
    sample_collection = [
        {"Name": "Lightning Bolt", "Set": "MH3", "Rarity": "Common", "Owner": "TestUser"},
        {"Name": "Force of Will", "Set": "MH3", "Rarity": "Mythic", "Owner": "TestUser"},
        {"Name": "Counterspell", "Set": "MH3", "Rarity": "Uncommon", "Owner": "OtherUser"},
        {"Name": "Giant Growth", "Set": "MH3", "Rarity": "Common", "Owner": "TestUser"},
    ]
    
    try:
        comparison = quick_rarity_comparison_by_owner(sample_collection, "MH3", "TestUser")
        
        if comparison:
            print("✅ Rarity comparison executes successfully")
            
            # Check if it has expected structure
            if isinstance(comparison, dict):
                print("✅ Returns structured comparison data")
            else:
                print(f"❌ Unexpected comparison format: {type(comparison)}")
        else:
            print("❌ Rarity comparison returned no results")
            
    except Exception as e:
        print(f"❌ Rarity comparison error: {e}")


def test_edge_cases():
    """Test edge cases and error conditions."""
    print("\n🔧 Testing Edge Cases...")
    
    # Test with empty database
    empty_result = check_card_in_db([], "Lightning Bolt")
    if not empty_result:
        print("✅ Handles empty database correctly")
    else:
        print("❌ Found card in empty database")
    
    # Test with None inputs
    try:
        none_result = check_card_in_db(None, "Lightning Bolt")
        print("❌ Should handle None database gracefully")
    except (TypeError, AttributeError):
        print("✅ Properly handles None database input")
    
    # Test line cleaner with empty input
    empty_cleaned = line_cleaner([])
    if empty_cleaned == []:
        print("✅ Handles empty line list correctly")
    else:
        print(f"❌ Empty line handling failed: {empty_cleaned}")
    
    # Test with malformed data
    malformed_collection = [
        {"Name": "Card1"},  # Missing Owner
        {"Owner": "User1"},  # Missing Name
        {},  # Empty entry
    ]
    
    try:
        malformed_owners = get_known_owners(malformed_collection)
        print("✅ Handles malformed collection data gracefully")
    except Exception as e:
        print(f"❌ Malformed data caused error: {e}")


def main():
    """Run all request_db tests."""
    print("💾 Starting Request DB Tests...\n")
    
    test_card_checking()
    test_line_cleaner()
    test_file_processing()
    test_owner_operations()
    test_set_statistics()
    test_rarity_comparison()
    test_edge_cases()
    
    print("\n🎉 Request DB tests complete!")


if __name__ == "__main__":
    main()
