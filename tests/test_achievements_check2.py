#!/usr/bin/env python3

"""
Test script to verify achievements check functionality after fixing game_id issue
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from achievements import AchievementManager

def test_achievements_check():
    """Test the achievements check functionality."""
    print("Testing achievements check after game_id fix...")
    
    # Initialize achievement manager
    achievement_manager = AchievementManager(
        achievements_file='player_achievements.json',
        stats_file='commander_stats.csv'
    )
    
    # Test InFeRMuS user (ID from dummy data)
    user_id = 123456789012345678
    
    try:
        # Check for new achievements
        new_achievements = achievement_manager.check_achievements(user_id)
        
        if new_achievements:
            print(f"🎉 New achievements earned!")
            for achievement in new_achievements:
                print(f"  🏆 {achievement.name} - {achievement.description} ({achievement.points} points)")
        else:
            print("✅ SUCCESS! No new achievements found (working correctly)")
        
        # Get player's current achievements for verification
        player_data = achievement_manager.player_achievements.get(user_id, {})
        total_achievements = len(player_data.get('earned', {}))
        total_points = player_data.get('total_points', 0)
        
        print(f"📊 Player Status: {total_achievements} achievements, {total_points} points")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_achievements_check()
    sys.exit(0 if success else 1)
