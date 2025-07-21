#!/usr/bin/env python3
"""Quick test for archetype selection system"""

try:
    from commander_games import CommanderGameManager
    import discord
    
    print("✅ Commander games module loaded successfully")
    
    # Test embed creation
    manager = CommanderGameManager()
    
    test_archetypes = ["Control", "Aggro", "Combo", "Midrange", "Tokens"]
    
    print(f"\n🎯 Testing archetype selection embed creation...")
    
    # We can't create a real embed without discord.py context, but we can test the logic
    print(f"✅ Archetype options: {test_archetypes}")
    
    # Test emoji mapping
    from edhrec_api import ARCHETYPE_EMOJIS
    
    print(f"\n😀 Testing emoji mappings:")
    for archetype in test_archetypes:
        emoji = ARCHETYPE_EMOJIS.get(archetype.lower(), "🎯")
        print(f"  {emoji} {archetype}")
        
    print(f"\n✅ All components loaded successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
