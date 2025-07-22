"""
Test achievements system with the corrected CSV field names
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.abspath('.'))

from achievements import achievement_manager

# Test with user ID from CSV
user_id = 412306053070585857  # Nite

print("🧪 Testing Achievement System")
print(f"📊 User ID: {user_id}")

try:
    # Test getting player stats first
    stats = achievement_manager._get_player_stats(user_id)
    print(f"✅ Stats retrieved successfully:")
    print(f"   Total games: {stats.get('total_games', 0)}")
    print(f"   Total wins: {stats.get('total_wins', 0)}")
    print(f"   Commanders played: {len(stats.get('commanders_played', set()))}")
    
    # Test checking achievements
    new_achievements = achievement_manager.check_achievements(user_id)
    
    if new_achievements:
        print(f"\n🎉 New achievements earned ({len(new_achievements)}):")
        for achievement in new_achievements:
            print(f"   🏆 {achievement.name}: {achievement.description}")
    else:
        print("\n📊 No new achievements (might already be earned)")
    
    # Show player achievements data
    player_data = achievement_manager.get_player_achievements(user_id)
    print(f"\n📈 Total achievement points: {player_data.get('total_points', 0)}")
    print(f"📊 Earned achievements: {len(player_data.get('earned', {}))}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
