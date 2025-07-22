"""
Test commander stats functionality
"""
from commander_games import commander_manager

# Test with user ID from the CSV
user_id = 412306053070585857  # Nite
stats = commander_manager.get_player_stats(user_id)

print("🧪 Testing Commander Stats for user ID:", user_id)
print("📊 Raw stats returned:")
for key, value in stats.items():
    print(f"   {key}: {value}")

print(f"\n📈 Summary:")
print(f"   Total Games: {stats.get('total_games', 0)}")
print(f"   Wins: {stats.get('wins', 0)}")
print(f"   Win Rate: {stats.get('win_rate', 0):.1f}%")
print(f"   Average Placement: {stats.get('avg_placement', 0):.1f}")
print(f"   Favorite Commander: {stats.get('favorite_commander', 'None')}")
