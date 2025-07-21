#!/usr/bin/env python3
"""
Quick test for the specific commander achievements check command.
"""

from achievements import achievement_manager

def test_achievements_check():
    """Test the achievements check command specifically."""
    infermus_user_id = 123456789012345678
    username = "InFeRMuS"
    
    print("🧪 Testing: !commander achievements check")
    print("=" * 50)
    
    try:
        # This is exactly what happens in the Discord command
        new_achievements = achievement_manager.check_achievements(infermus_user_id)
        
        if new_achievements:
            print(f"✅ SUCCESS! Found {len(new_achievements)} new achievements:")
            print(f"📱 Discord would send: \"🎉 **{username}**, you've earned {len(new_achievements)} new achievement{'s' if len(new_achievements) > 1 else ''}!\"")
            
            for achievement in new_achievements:
                print(f"   🏆 {achievement.emoji} {achievement.name} ({achievement.points} pts)")
                print(f"      📝 {achievement.description}")
                print(f"      💎 Rarity: {achievement.rarity}")
        else:
            print("✅ SUCCESS! No new achievements found")
            print("📱 Discord would send: \"✅ No new achievements at this time. Keep playing to unlock more!\"")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_achievements_check()
