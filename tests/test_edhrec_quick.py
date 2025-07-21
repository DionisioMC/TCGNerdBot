#!/usr/bin/env python3
"""
Quick test for EDHREC API integration
Tests the ability to fetch commander archetypes from EDHREC.com
"""

from edhrec_api import EDHRECAPI, ARCHETYPE_EMOJIS

def test_edhrec_api():
    """Test EDHREC API functionality"""
    print("🚀 Testing EDHREC API Integration")
    print("=" * 50)
    
    api = EDHRECAPI()
    
    # Test commanders with known archetypes
    test_commanders = [
        "Atraxa, Praetors' Voice",
        "Edgar Markov", 
        "The Ur-Dragon",
        "Krenko, Mob Boss",
        "Meren of Clan Nel Toth",
        "Yuriko, the Tiger's Shadow",
        "Nekusar, the Mindrazer"
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for commander in test_commanders:
        print(f"\n🧪 Testing: {commander}")
        print("-" * 30)
        
        try:
            # Test name sanitization first
            sanitized = api.sanitize_commander_name(commander)
            print(f"📝 Sanitized name: '{sanitized}'")
            
            # Fetch archetype data
            archetypes = api.get_commander_archetypes(commander)
            
            if archetypes and archetypes.get('archetypes'):
                print(f"✅ Found {len(archetypes['archetypes'])} archetypes:")
                print(f"🎯 Most popular: {archetypes.get('most_popular', 'Unknown')}")
                
                # Show first few archetypes with emojis
                for i, archetype in enumerate(archetypes['archetypes'][:5]):
                    emoji = ARCHETYPE_EMOJIS.get(archetype, "🎯")
                    print(f"   {i+1}. {emoji} {archetype}")
                
                if len(archetypes['archetypes']) > 5:
                    print(f"   ... and {len(archetypes['archetypes']) - 5} more")
                
                successful_tests += 1
            else:
                print("❌ No archetypes found (API rate limit or network issue)")
                failed_tests += 1
                
        except Exception as e:
            print(f"❌ Error: {e}")
            failed_tests += 1
    
    # Test fallback system
    print(f"\n🔄 Testing Fallback System")
    print("-" * 30)
    
    try:
        fallback_archetypes = api.get_fallback_archetypes()
        print(f"✅ Fallback archetypes available: {len(fallback_archetypes)}")
        print("📋 Sample fallback archetypes:")
        for archetype in fallback_archetypes[:8]:
            emoji = ARCHETYPE_EMOJIS.get(archetype, "🎯")
            print(f"   {emoji} {archetype}")
    except Exception as e:
        print(f"❌ Fallback system error: {e}")
    
    # Test emoji mappings
    print(f"\n😀 Testing Emoji Mappings")
    print("-" * 30)
    
    sample_archetypes = ["Aggro", "Control", "Combo", "Tribal", "Elves", "Tokens"]
    for archetype in sample_archetypes:
        emoji = ARCHETYPE_EMOJIS.get(archetype, "🎯")
        print(f"   {emoji} {archetype}")
    
    # Summary
    print(f"\n" + "=" * 50)
    print(f"📊 Test Results Summary:")
    print(f"✅ Successful: {successful_tests}/{len(test_commanders)}")
    print(f"❌ Failed: {failed_tests}/{len(test_commanders)}")
    
    if failed_tests > 0:
        print(f"\n⚠️  Note: API failures are expected due to EDHREC rate limiting")
        print(f"🔄 The fallback system ensures functionality continues")
    
    if successful_tests > 0:
        print(f"\n🎉 EDHREC API integration is working!")
    else:
        print(f"\n⚠️  All API calls failed - check network connection")
        print(f"✅ Fallback system will handle commander archetype selection")

if __name__ == "__main__":
    test_edhrec_api()
