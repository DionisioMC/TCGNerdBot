#!/usr/bin/env python3

"""
Test script to simulate the Discord achievements check command
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from achievements import AchievementManager

def simulate_discord_achievements_check():
    """Simulate the Discord !commander achievements check command."""
    print("🎮 Simulating Discord command: !commander achievements check")
    print("=" * 60)
    
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
            # Format message like Discord bot would
            message = f"🎉 **New achievements unlocked!** 🎉\n\n"
            for achievement in new_achievements:
                rarity_emoji = {
                    'common': '⚪',
                    'uncommon': '🟢', 
                    'rare': '🔵',
                    'epic': '🟣',
                    'legendary': '🟡'
                }.get(achievement.rarity, '⚪')
                
                message += f"{rarity_emoji} **{achievement.name}** {achievement.emoji}\n"
                message += f"*{achievement.description}*\n"
                message += f"**+{achievement.points} points** • {achievement.category.title()}\n\n"
            
            # Add summary
            player_data = achievement_manager.player_achievements.get(user_id, {})
            total_points = player_data.get('total_points', 0)
            message += f"📊 **Total: {total_points} achievement points**"
            
            print(message)
        else:
            print("✅ No new achievements to unlock!")
            print("Keep playing to earn more achievements! 🎯")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR in achievements check: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simulate_discord_achievements_check()
    sys.exit(0 if success else 1)
