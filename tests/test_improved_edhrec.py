"""
Test the improved EDHREC API implementation based on pyedhrec library.
"""

import asyncio
from edhrec_api import edhrec_api, get_archetype_emoji, normalize_archetype


async def test_new_edhrec_api():
    """Test the new EDHREC API implementation."""
    print("🧪 Testing Improved EDHREC API Implementation...")
    
    # Test commanders to try
    test_commanders = [
        "Atraxa, Praetors' Voice",
        "Edgar Markov", 
        "Korvold, Fae-Cursed King",
        "Rhystic Study"  # This should fail - not a commander
    ]
    
    for commander in test_commanders:
        print(f"\n🎯 Testing: {commander}")
        
        try:
            # Test commander data fetching
            commander_data = edhrec_api.get_commander_data(commander)
            if commander_data:
                print(f"   ✅ Commander data found")
                print(commander_data)
                # Print some basic info
                container = commander_data.get("container", {})
                if container:
                    print(f"   📊 Container data available")
                
            # Test archetype extraction
            archetype_data = edhrec_api.get_commander_archetypes(commander)
            if archetype_data:
                archetypes = archetype_data.get('archetypes', [])
                most_popular = archetype_data.get('most_popular', 'Unknown')
                
                print(f"   🎭 Most Popular: {most_popular}")
                print(f"   📋 Available Archetypes: {archetypes[:5]}...")  # Show first 5
                
                # Test emoji mapping
                emoji = get_archetype_emoji(most_popular)
                print(f"   {emoji} Emoji for '{most_popular}': {emoji}")
                
                # Test normalization
                normalized = normalize_archetype(most_popular)
                print(f"   🔄 Normalized: {normalized}")
                
            else:
                print(f"   ❌ No archetype data found")
                
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    # Test special normalization cases
    print(f"\n🧝 Testing Elves normalization:")
    elves_normalized = normalize_archetype("Elves")
    print(f"   'Elves' → '{elves_normalized}'")
    
    print(f"\n🎉 EDHREC API testing complete!")


def test_formatting():
    """Test card name formatting."""
    print("\n🔤 Testing Card Name Formatting...")
    
    test_names = [
        "Atraxa, Praetors' Voice",
        "The Ur-Dragon",
        "Jace, the Mind Sculptor",
        "Lightning Bolt"
    ]
    
    for name in test_names:
        formatted = edhrec_api.format_card_name(name)
        print(f"   '{name}' → '{formatted}'")


if __name__ == "__main__":
    # Test formatting (synchronous)
    test_formatting()
    
    # Test API (asynchronous)
    asyncio.run(test_new_edhrec_api())
