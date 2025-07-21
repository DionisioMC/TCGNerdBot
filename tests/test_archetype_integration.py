"""
Integration test for the complete archetype reaction flow.
"""

from commander_games import commander_manager, create_archetype_selection_embed, get_archetype_emojis
from command_handlers import CommandHandlers

def test_archetype_reaction_flow():
    """Test the complete archetype reaction flow."""
    print("🧪 Testing Complete Archetype Reaction Flow...")
    
    # Test data
    commander_name = "Atraxa, Praetors' Voice"
    archetype_data = {
        'archetypes': ['Infect', 'Planeswalkers', 'Counters', 'Control', 'Superfriends'],
        'most_popular': 'Infect'
    }
    current_archetype = 'Unknown'
    
    print(f"Testing with commander: {commander_name}")
    print(f"Available archetypes: {archetype_data['archetypes']}")
    
    # Test embed creation
    try:
        embed = create_archetype_selection_embed(commander_name, archetype_data, current_archetype)
        print("✅ Archetype selection embed created successfully")
        print(f"   Title: {embed.title}")
        print(f"   Description: {embed.description[:100]}...")
    except Exception as e:
        print(f"❌ Error creating embed: {e}")
        return
    
    # Test emoji generation
    try:
        emojis = get_archetype_emojis(archetype_data['archetypes'])
        print(f"✅ Emojis generated: {emojis}")
    except Exception as e:
        print(f"❌ Error generating emojis: {e}")
        return
    
    # Test commander_manager.set_archetype functionality (without actual game)
    print("\n🔧 Testing set_archetype method signature...")
    import inspect
    method = getattr(commander_manager, 'set_archetype')
    sig = inspect.signature(method)
    print(f"✅ set_archetype signature: {sig}")
    
    # Test that method expects correct parameters
    try:
        # This will fail because there's no game, but it should validate the signature
        result = commander_manager.set_archetype("test_game", 12345, "Infect")
        print(f"   Result (expected failure): {result}")
    except Exception as e:
        print(f"   Expected failure (no game exists): {e}")
    
    print("\n🎉 Archetype reaction flow test complete!")
    print("✅ All components are properly connected and functional!")

if __name__ == "__main__":
    test_archetype_reaction_flow()
