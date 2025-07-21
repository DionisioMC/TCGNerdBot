#!/usr/bin/env python3
"""
Script to test and display achievement embeds as they would appear in Discord.
Shows the visual representation of InFeRMuS's achievements.
"""

from achievements import achievement_manager, create_achievement_embed, create_achievements_overview_embed
import discord
from datetime import datetime

def test_achievement_embeds():
    """Test what the achievement embeds look like."""
    
    infermus_user_id = 123456789012345678
    username = "InFeRMuS"
    
    print("🎨 DISCORD ACHIEVEMENT EMBED PREVIEW")
    print("=" * 60)
    
    # Get player data
    player_data = achievement_manager.player_achievements.get(infermus_user_id, {})
    if not player_data:
        print("❌ No achievement data found for InFeRMuS!")
        return
        
    earned_achievements = player_data.get('earned', {})
    
    print(f"👤 User: {username}")
    print(f"🆔 ID: {infermus_user_id}")
    print(f"🏆 Achievements Earned: {len(earned_achievements)}")
    print(f"💎 Total Points: {player_data.get('total_points', 0)}")
    print("\n" + "=" * 60)
    
    # Show individual achievement embeds
    print("🎯 INDIVIDUAL ACHIEVEMENT EMBEDS:")
    print("-" * 40)
    
    # Show a variety of achievements
    showcase_achievements = [
        'first_game',      # Common milestone
        'win_streak_3',    # Uncommon performance  
        'comeback_king',   # Rare special (hidden!)
        'versatile_player' # Uncommon variety
    ]
    
    for i, achievement_id in enumerate(showcase_achievements, 1):
        if achievement_id in earned_achievements and achievement_id in achievement_manager.achievements:
            achievement = achievement_manager.achievements[achievement_id]
            
            print(f"\n{i}. {achievement.emoji} {achievement.name}")
            print("   " + "─" * 30)
            
            # Simulate embed fields
            rarity_colors = {
                'common': '🔘 Gray',
                'uncommon': '🟢 Green', 
                'rare': '🔵 Blue',
                'epic': '🟣 Purple',
                'legendary': '🟡 Gold'
            }
            
            color = rarity_colors.get(achievement.rarity, '🔘 Gray')
            
            print(f"   📱 Discord Embed:")
            print(f"      🎉 Title: Achievement Unlocked!")
            print(f"      🎨 Color: {color}")
            print(f"      📝 Description: {achievement.description}")
            print(f"      💎 Rarity: {achievement.rarity.title()}")
            print(f"      🏆 Points: {achievement.points} pts")
            print(f"      📂 Category: {achievement.category.title()}")
            
            if achievement.hidden:
                print(f"      🤫 Special: Hidden Achievement!")
    
    print("\n" + "=" * 60)
    print("📊 ACHIEVEMENTS OVERVIEW EMBED:")
    print("-" * 40)
    
    # Calculate overview stats
    total_achievements = len(achievement_manager.achievements)
    earned_count = len(earned_achievements)
    progress_percentage = (earned_count / total_achievements) * 100
    
    # Category breakdown
    categories = {}
    points_by_rarity = {}
    
    for achievement_id in earned_achievements:
        if achievement_id in achievement_manager.achievements:
            achievement = achievement_manager.achievements[achievement_id]
            categories[achievement.category] = categories.get(achievement.category, 0) + 1
            points_by_rarity[achievement.rarity] = points_by_rarity.get(achievement.rarity, 0) + achievement.points
    
    print(f"\n🏆 {username}'s Achievement Overview")
    print("   " + "─" * 35)
    print(f"   📱 Discord Embed:")
    print(f"      🎨 Color: 🟡 Gold (Achievement theme)")
    print(f"      📊 Progress: {earned_count}/{total_achievements} ({progress_percentage:.1f}%)")
    print(f"      💎 Total Points: {player_data.get('total_points', 0)}")
    print(f"      📈 Progress Bar: {'█' * int(progress_percentage/10)}{'░' * (10-int(progress_percentage/10))}")
    
    print(f"\n      📂 Categories Completed:")
    for category, count in categories.items():
        print(f"         • {category.title()}: {count} achievements")
    
    print(f"\n      💎 Points by Rarity:")
    for rarity, points in points_by_rarity.items():
        print(f"         • {rarity.title()}: {points} points")
    
    print("\n" + "=" * 60)
    print("🎮 RECENT ACHIEVEMENT NOTIFICATIONS:")
    print("-" * 40)
    
    # Show what recent achievement notifications would look like
    recent_achievements = list(earned_achievements.keys())[-3:]  # Last 3 earned
    
    for i, achievement_id in enumerate(recent_achievements, 1):
        if achievement_id in achievement_manager.achievements:
            achievement = achievement_manager.achievements[achievement_id]
            
            print(f"\n{i}. 🎉 Achievement Notification:")
            print(f"   💬 Message: \"🎉 **InFeRMuS**, you've earned a new achievement!\"")
            print(f"   📱 Embed: {achievement.emoji} {achievement.name}")
            print(f"   ✨ Rarity: {achievement.rarity.title()} ({achievement.points} points)")
            if achievement.hidden:
                print(f"   🤫 Hidden achievement revealed!")

def show_leaderboard_preview():
    """Show what the leaderboard would look like."""
    print("\n" + "=" * 60)
    print("🏅 ACHIEVEMENT LEADERBOARD PREVIEW:")
    print("-" * 40)
    
    # Get leaderboard data
    leaderboard = achievement_manager.get_achievement_leaderboard(10)
    
    if leaderboard:
        print(f"\n🏆 Top Achievement Earners")
        print("   " + "─" * 30)
        print(f"   📱 Discord Embed:")
        print(f"      🎨 Color: 🟡 Gold")
        
        for i, (user_id, data) in enumerate(leaderboard, 1):
            username = "InFeRMuS" if user_id == 123456789012345678 else f"User{user_id}"
            points = data.get('total_points', 0)
            count = data.get('total_earned', 0)
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            print(f"      {medal} **{username}**: {points} pts ({count} achievements)")
    
    else:
        print("   📱 No leaderboard data available yet")

def main():
    """Main function to display achievement previews."""
    print("🚀 DISCORD ACHIEVEMENT PREVIEW FOR InFeRMuS")
    print("🎯 This shows how achievements will appear in Discord")
    print()
    
    try:
        test_achievement_embeds()
        show_leaderboard_preview()
        
        print("\n" + "=" * 60)
        print("✅ PREVIEW COMPLETE!")
        print("💡 These embeds will appear in Discord when using:")
        print("   • !commander achievements - Shows overview")
        print("   • !commander achievements check - Checks for new ones")
        print("   • !commander leaderboard - Shows rankings")
        print("   • Automatic notifications when achievements are earned")
        
    except Exception as e:
        print(f"❌ Error generating preview: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
