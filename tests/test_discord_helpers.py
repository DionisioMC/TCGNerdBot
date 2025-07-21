"""
Test Discord helpers functionality - Embed creation and message utilities.
"""

import sys
from unittest.mock import MagicMock

# Fix imports for tests directory
from test_utils import fix_test_imports
fix_test_imports()

from discord_helpers import (
    create_daily_card_embed,
    create_set_stats_embed, 
    create_collection_overview_embed,
    create_collection_comparison_embed,
    create_help_embed,
    create_help_embed_page,
    split_message_into_chunks
)


def test_daily_card_embed():
    """Test daily card embed creation."""
    print("🧪 Testing Daily Card Embed Creation...")
    
    # Test with complete card data
    complete_card = {
        "name": "Lightning Bolt",
        "mana_cost": "{R}",
        "type_line": "Instant",
        "oracle_text": "Lightning Bolt deals 3 damage to any target.",
        "image_uris": {
            "normal": "https://cards.scryfall.io/normal/front/sample.jpg"
        },
        "set_name": "Alpha",
        "prices": {
            "eur": "5.50"
        }
    }
    
    try:
        embed = create_daily_card_embed(complete_card)
        
        if embed and hasattr(embed, 'title'):
            print("✅ Daily card embed created successfully")
            
            if "Lightning Bolt" in str(embed.title):
                print("✅ Card name included in embed")
            else:
                print("❌ Card name missing from embed title")
                
        else:
            print("❌ Daily card embed creation failed")
            
    except Exception as e:
        print(f"❌ Daily card embed creation error: {e}")
    
    # Test with minimal card data
    minimal_card = {
        "name": "Test Card"
    }
    
    try:
        minimal_embed = create_daily_card_embed(minimal_card)
        if minimal_embed:
            print("✅ Handles minimal card data gracefully")
        else:
            print("❌ Failed with minimal card data")
    except Exception as e:
        print(f"❌ Minimal card data error: {e}")


def test_set_stats_embed():
    """Test set statistics embed creation."""
    print("\n📊 Testing Set Stats Embed Creation...")
    
    sample_stats = {
        "set_code": "MH3",
        "set_name": "Modern Horizons 3",
        "total_cards": 303,
        "mythic_count": 15,
        "rare_count": 60,
        "uncommon_count": 100,
        "common_count": 128
    }
    
    try:
        embed = create_set_stats_embed(sample_stats)
        
        if embed and hasattr(embed, 'title'):
            print("✅ Set stats embed created successfully")
            
            if "MH3" in str(embed.title) or "Modern Horizons 3" in str(embed.title):
                print("✅ Set information included in embed")
            else:
                print("❌ Set information missing from embed")
                
        else:
            print("❌ Set stats embed creation failed")
            
    except Exception as e:
        print(f"❌ Set stats embed creation error: {e}")


def test_collection_overview_embed():
    """Test collection overview embed creation."""
    print("\n📚 Testing Collection Overview Embed Creation...")
    
    sample_comparisons = [
        {
            "set_code": "MH3",
            "completion": 85.5,
            "owned": 259,
            "total": 303
        },
        {
            "set_code": "OTJ", 
            "completion": 92.3,
            "owned": 278,
            "total": 301
        }
    ]
    
    try:
        embed = create_collection_overview_embed("TestUser", sample_comparisons)
        
        if embed and hasattr(embed, 'title'):
            print("✅ Collection overview embed created successfully")
            
            if "TestUser" in str(embed.title):
                print("✅ Username included in embed")
            else:
                print("❌ Username missing from embed")
                
        else:
            print("❌ Collection overview embed creation failed")
            
    except Exception as e:
        print(f"❌ Collection overview embed creation error: {e}")


def test_collection_comparison_embed():
    """Test collection comparison embed creation."""
    print("\n⚖️ Testing Collection Comparison Embed Creation...")
    
    sample_comparison = {
        "set_code": "MH3",
        "set_name": "Modern Horizons 3",
        "owned_cards": 259,
        "total_cards": 303,
        "completion_percentage": 85.5,
        "missing_mythics": 2,
        "missing_rares": 8,
        "missing_uncommons": 15,
        "missing_commons": 19
    }
    
    try:
        embed = create_collection_comparison_embed("MH3", sample_comparison)
        
        if embed and hasattr(embed, 'title'):
            print("✅ Collection comparison embed created successfully")
            
            if "MH3" in str(embed.title):
                print("✅ Set code included in embed")
            else:
                print("❌ Set code missing from embed")
                
        else:
            print("❌ Collection comparison embed creation failed")
            
    except Exception as e:
        print(f"❌ Collection comparison embed creation error: {e}")


def test_help_embed():
    """Test help embed creation."""
    print("\n❓ Testing Help Embed Creation...")
    
    try:
        embed = create_help_embed()
        
        if embed and hasattr(embed, 'title'):
            print("✅ Help embed created successfully")
            
            if "help" in str(embed.title).lower() or "command" in str(embed.title).lower():
                print("✅ Help-related title included")
            else:
                print("❌ Help title missing or unclear")
                
        else:
            print("❌ Help embed creation failed")
            
    except Exception as e:
        print(f"❌ Help embed creation error: {e}")


def test_help_embed_pagination():
    """Test paginated help embed creation."""
    print("\n📄 Testing Help Embed Pagination...")
    
    # Test different pages
    for page in [1, 2, 3, 4]:
        try:
            embed = create_help_embed_page(page)
            
            if embed and hasattr(embed, 'title'):
                print(f"✅ Help page {page} created successfully")
            else:
                print(f"❌ Help page {page} creation failed")
                
        except Exception as e:
            print(f"❌ Help page {page} creation error: {e}")
    
    # Test invalid page number
    try:
        invalid_embed = create_help_embed_page(999)
        if invalid_embed:
            print("✅ Invalid page number handled gracefully")
        else:
            print("❌ Invalid page number not handled")
    except Exception as e:
        print(f"❌ Invalid page number error: {e}")


def test_message_splitting():
    """Test message splitting functionality."""
    print("\n✂️ Testing Message Splitting...")
    
    # Test short message (should not be split)
    short_message = "This is a short message."
    short_chunks = split_message_into_chunks(short_message, max_length=100)
    
    if len(short_chunks) == 1 and short_chunks[0] == short_message:
        print("✅ Short message handled correctly")
    else:
        print(f"❌ Short message splitting failed: {short_chunks}")
    
    # Test long message (should be split)
    long_message = "A" * 500  # 500 character message
    long_chunks = split_message_into_chunks(long_message, max_length=100)
    
    if len(long_chunks) > 1:
        print("✅ Long message split correctly")
        
        # Check that no chunk exceeds max length
        all_valid = all(len(chunk) <= 100 for chunk in long_chunks)
        if all_valid:
            print("✅ All chunks within length limit")
        else:
            print("❌ Some chunks exceed length limit")
            
        # Check that all content is preserved
        reconstructed = "".join(long_chunks)
        if reconstructed == long_message:
            print("✅ Message content preserved after splitting")
        else:
            print("❌ Message content lost during splitting")
            
    else:
        print(f"❌ Long message not split: {len(long_chunks)} chunks")
    
    # Test empty message
    empty_chunks = split_message_into_chunks("", max_length=100)
    if len(empty_chunks) == 1 and empty_chunks[0] == "":
        print("✅ Empty message handled correctly")
    else:
        print(f"❌ Empty message handling failed: {empty_chunks}")


def test_embed_structure():
    """Test general embed structure and properties."""
    print("\n🏗️ Testing Embed Structure...")
    
    # Test that embeds have expected properties
    sample_card = {"name": "Test Card", "mana_cost": "{1}"}
    
    try:
        embed = create_daily_card_embed(sample_card)
        
        # Check for common embed properties
        properties = ['title', 'description', 'color']
        missing_props = []
        
        for prop in properties:
            if not hasattr(embed, prop):
                missing_props.append(prop)
        
        if not missing_props:
            print("✅ Embed has all expected properties")
        else:
            print(f"❌ Embed missing properties: {missing_props}")
            
    except Exception as e:
        print(f"❌ Embed structure test error: {e}")


def main():
    """Run all Discord helpers tests."""
    print("🎨 Starting Discord Helpers Tests...\n")
    
    test_daily_card_embed()
    test_set_stats_embed()
    test_collection_overview_embed()
    test_collection_comparison_embed()
    test_help_embed()
    test_help_embed_pagination()
    test_message_splitting()
    test_embed_structure()
    
    print("\n🎉 Discord helpers tests complete!")


if __name__ == "__main__":
    main()
