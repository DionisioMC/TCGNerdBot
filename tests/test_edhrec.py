#!/usr/bin/env python3
"""Quick test for EDHREC API integration"""

try:
    from edhrec_api import EDHRECAPI
    
    print("✅ EDHREC API module loaded successfully")
    
    api = EDHRECAPI()
    
    # Test with a popular commander
    test_commander = "Atraxa, Praetors' Voice"
    print(f"\n🧪 Testing with commander: {test_commander}")
    
    archetypes = api.get_commander_archetypes(test_commander)
    
    if archetypes:
        print(f"✅ Found {len(archetypes)} archetypes:")
        for archetype in archetypes:
            emoji = api.ARCHETYPE_EMOJIS.get(archetype, "🎯")
            print(f"  {emoji} {archetype}")
    else:
        print("❌ No archetypes found or API error")
        
    # Test sanitization
    print(f"\n🧹 Testing name sanitization:")
    test_names = [
        "Atraxa, Praetor's Voice",
        "Atraxa, Praetors' Voice", 
        "Krenko, Mob Boss"
    ]
    
    for name in test_names:
        sanitized = api.sanitize_commander_name(name)
        print(f"  '{name}' -> '{sanitized}'")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
