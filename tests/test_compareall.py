#!/usr/bin/env python3
"""
Test script for the new compareall functionality
"""

from request_db import get_cards_from_csv, compare_all_sets_by_owner


def test_compareall():
    """Test the compareall functionality with the actual collection"""
    try:
        # Load the collection
        file_path = 'Collections/final_collection.csv'
        collection = get_cards_from_csv(file_path)

        print(f"Loaded {len(collection)} cards from collection")

        # Test with InFeRMuS (from the CSV data)
        username = "InFeRMuS"
        print(f"\nTesting compareall for user: {username}")

        # Get comparison for all sets
        comparisons = compare_all_sets_by_owner(collection, username)

        print(f"Found {len(comparisons)} sets for {username}")

        # Display results
        for i, comp in enumerate(comparisons[:5], 1):  # Show top 5
            print(f"{i}. {comp['set_name']} ({comp['set_code']})")
            print(
                f"   Completion: {comp['your_total']}/{comp['set_total']} cards ({comp['completion_percentage']:.1f}%)")
            print()

        return True

    except Exception as e:
        print(f"Error testing compareall: {e}")
        return False


if __name__ == "__main__":
    test_compareall()
