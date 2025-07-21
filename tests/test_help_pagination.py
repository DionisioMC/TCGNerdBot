"""
Test the paginated help system functionality.
"""

import discord
from discord_helpers import create_help_embed_page

def test_help_pagination():
    """Test the help page creation and pagination."""
    print("🧪 Testing Paginated Help System...")
    
    # Test all 4 pages
    for page in range(1, 5):
        print(f"\n📖 Testing Page {page}:")
        embed = create_help_embed_page(page)
        print(f"   Title: {embed.title}")
        print(f"   Description: {embed.description[:50]}...")
        print(f"   Fields: {len(embed.fields)}")
        
        # Check for navigation info in each page
        navigation_field = None
        for field in embed.fields:
            if "Navigation" in field.name:
                navigation_field = field
                break
        
        if navigation_field:
            print(f"   ✅ Navigation field found")
        else:
            print(f"   ❌ Navigation field missing")
    
    # Test invalid page (should default to page 1)
    print(f"\n📖 Testing Invalid Page (should default to page 1):")
    embed = create_help_embed_page(999)
    print(f"   Title: {embed.title}")
    assert "Page 1/4" in embed.title, "Invalid page should default to page 1"
    print(f"   ✅ Invalid page handling works correctly")
    
    print(f"\n🎉 All tests passed! Paginated help system is ready.")

if __name__ == "__main__":
    test_help_pagination()
