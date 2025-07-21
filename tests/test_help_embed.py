#!/usr/bin/env python3
"""
Test the updated help embed
"""

from discord_helpers import create_help_embed

def test_help_embed():
    """Test the help embed creation"""
    print("🧪 Testing Updated Help Embed")
    print("=" * 40)
    
    try:
        embed = create_help_embed()
        
        print(f"✅ Embed created successfully")
        print(f"📝 Title: {embed.title}")
        print(f"📄 Description: {embed.description}")
        print(f"🏷️ Fields: {len(embed.fields)}")
        
        print(f"\n📋 Field Names:")
        for i, field in enumerate(embed.fields, 1):
            print(f"  {i}. {field.name}")
        
        # Check for new archetype features
        archetype_field = None
        for field in embed.fields:
            if "Archetype Tracking" in field.name:
                archetype_field = field
                break
        
        if archetype_field:
            print(f"\n✅ Found archetype tracking field: {archetype_field.name}")
        else:
            print(f"\n❌ Archetype tracking field not found")
        
        # Check for achievement mentions
        achievement_mentions = 0
        for field in embed.fields:
            if "achievement" in field.value.lower():
                achievement_mentions += 1
        
        print(f"🏆 Achievement mentions: {achievement_mentions}")
        
        # Check for new emoji indicators
        new_features = 0
        for field in embed.fields:
            new_features += field.value.count("🆕")
        
        print(f"🆕 New feature indicators: {new_features}")
        
        print(f"\n✅ Help embed test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error creating help embed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_help_embed()
