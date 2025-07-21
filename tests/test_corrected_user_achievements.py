#!/usr/bin/env python3

"""
Test script to check achievements for the corrected user ID
"""

import sys
import os
# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from achievements import AchievementManager

def test_achievements_for_corrected_user():
    """Test achievements for user ID 352817681654743042."""
    print("Testing achievements for corrected user ID...")
    
    # Initialize achievement manager
    achievement_manager = AchievementManager(
        achievements_file='player_achievements.json',
        stats_file='commander_stats.csv'
    )
    
    # Test the corrected user ID (matching CSV data)
    user_id = 352817681654743041
    
    try:
        # Check for new achievements
        new_achievements = achievement_manager.check_achievements(user_id)
        
        if new_achievements:
            print(f"🎉 New achievements earned!")
            for achievement in new_achievements:
                print(f"  🏆 {achievement.name} - {achievement.description} ({achievement.points} points)")
        else:
            print("✅ No new achievements (or already earned)")
        
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
    success = test_achievements_for_corrected_user()
    sys.exit(0 if success else 1)
