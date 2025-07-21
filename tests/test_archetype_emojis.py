"""
Test archetype emoji functionality.
"""

from commander_games import get_archetype_emojis, get_archetype_from_emoji

def test_archetype_emojis():
    """Test archetype emoji functions."""
    print("🧪 Testing Archetype Emoji Functions...")
    
    # Test sample archetype list
    test_archetypes = ["Infect", "Planeswalkers", "Counters", "Control", "Aggro"]
    
    # Test emoji generation
    emojis = get_archetype_emojis(test_archetypes)
    print(f"✅ Generated emojis for {len(test_archetypes)} archetypes: {emojis}")
    
    if len(emojis) == len(test_archetypes):
        print("✅ Correct number of emojis generated")
    else:
        print(f"❌ Expected {len(test_archetypes)} emojis, got {len(emojis)}")
    
    # Test emoji-to-archetype mapping
    for i, (archetype, emoji) in enumerate(zip(test_archetypes, emojis)):
        mapped_archetype = get_archetype_from_emoji(emoji, test_archetypes)
        if mapped_archetype == archetype:
            print(f"✅ {emoji} correctly maps to '{archetype}'")
        else:
            print(f"❌ {emoji} maps to '{mapped_archetype}', expected '{archetype}'")
    
    print("\n🎉 Archetype emoji test complete!")

if __name__ == "__main__":
    test_archetype_emojis()
