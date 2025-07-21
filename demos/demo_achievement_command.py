#!/usr/bin/env python3
"""
Demo script showing the new achievement detail command in action.
This simulates what users will see when using the command.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from achievements import achievement_manager, create_achievement_detail_embed

def demo_achievement_command():
    """Demonstrate the new achievement detail command."""
    print("🎮 TCG Nerd Bot - Achievement Detail Command Demo")
    print("=" * 60)
    
    # Simulate different user commands
    commands = [
        "!c achievements info first_win",
        "!c achievements detail victory royale", 
        "!c achievements info legendary",
        "!c achievements detail combo_master",
        "!c achievements info invalid_achievement"
    ]
    
    user_id = 352817681654743041  # Our test user
    
    for command in commands:
        print(f"\n💬 User types: {command}")
        print("-" * 40)
        
        # Parse the command
        parts = command.split()
        if len(parts) >= 4:
            search_term = " ".join(parts[3:])
            achievement = achievement_manager.find_achievement(search_term)
            
            if achievement:
                # Get user progress
                player_data = achievement_manager.get_player_achievements(user_id)
                user_has_earned = achievement.id in player_data['earned']
                earned_date = None
                
                if user_has_earned:
                    earned_info = player_data['earned'][achievement.id]
                    earned_date = earned_info.get('earned_at') or earned_info.get('date')
                
                # Calculate server stats
                total_players = len(achievement_manager.player_achievements)
                earned_by_count = 0
                for player_data_item in achievement_manager.player_achievements.values():
                    if achievement.id in player_data_item['earned']:
                        earned_by_count += 1
                
                # Show what the bot would respond with
                status = "✅ Earned" if user_has_earned else "🔒 Locked"
                percentage = (earned_by_count / total_players) * 100 if total_players > 0 else 0
                
                print(f"🤖 Bot Response:")
                print(f"   {status} {achievement.emoji} {achievement.name}")
                print(f"   📝 {achievement.description}")
                print(f"   💎 {achievement.rarity.title()} • 🏆 {achievement.points} points")
                print(f"   📊 Earned by {earned_by_count}/{total_players} players ({percentage:.1f}%)")
                
                if user_has_earned and earned_date:
                    try:
                        from datetime import datetime
                        earned_dt = datetime.fromisoformat(earned_date.replace('Z', '+00:00'))
                        date_str = earned_dt.strftime("%B %d, %Y")
                        print(f"   🎯 You earned this on {date_str}")
                    except:
                        print(f"   🎯 You have earned this achievement")
                else:
                    print(f"   🎯 You haven't earned this yet - keep playing!")
                    
            else:
                print(f"🤖 Bot Response:")
                print(f"   ❌ Achievement '{search_term}' not found.")
                print(f"   💡 Tip: Use `!c achievements` to see all available achievements.")
        else:
            print(f"🤖 Bot Response:")
            print(f"   ❌ Please specify an achievement to view!")
            print(f"   Usage: `!c achievements info <achievement_name_or_id>`")
    
    print("\n" + "=" * 60)
    print("🎉 Achievement Detail Command Demo Complete!")
    print("\nNew Features Added:")
    print("✅ Smart search by ID, name, or partial match")
    print("✅ Detailed achievement information with rarity colors")
    print("✅ Personal progress tracking (earned date)")
    print("✅ Server-wide statistics and completion rates")
    print("✅ Helpful error messages and guidance")
    print("✅ Support for multiple command aliases (info/detail/details)")

if __name__ == "__main__":
    demo_achievement_command()
