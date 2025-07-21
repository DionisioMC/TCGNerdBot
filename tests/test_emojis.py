#!/usr/bin/env python3
"""Test emoji mappings with correct case"""

try:
    from edhrec_api import ARCHETYPE_EMOJIS
    
    print("✅ EDHREC emoji mappings loaded")
    
    test_archetypes = ["Control", "Aggro", "Combo", "Midrange", "Tokens"]
    
    print(f"\n😀 Testing emoji mappings with correct case:")
    for archetype in test_archetypes:
        emoji = ARCHETYPE_EMOJIS.get(archetype, "🎯")  # Use original case
        print(f"  {emoji} {archetype}")
        
    print(f"\n📋 All available emojis:")
    for archetype, emoji in ARCHETYPE_EMOJIS.items():
        print(f"  {emoji} {archetype}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
