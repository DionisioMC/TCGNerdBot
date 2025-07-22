"""
Test commander stats embed creation
"""
from commander_games import commander_manager, create_player_stats_embed

# Test with user ID from the CSV
user_id = 352817681654743041  # Xôr Vitor
username = "Xôr Vitor"
stats = commander_manager.get_player_stats(user_id)

print("🧪 Testing Commander Stats Embed Creation")
print("📊 Stats found:", stats)

if stats.get('total_games', 0) > 0:
    embed = create_player_stats_embed(user_id, username, stats)
    print("\n✅ Embed created successfully!")
    print(f"   Title: {embed.title}")
    print(f"   Color: {embed.color}")
    print(f"   Number of fields: {len(embed.fields)}")
    
    for i, field in enumerate(embed.fields):
        print(f"   Field {i+1}: {field.name}")
        print(f"      Value: {field.value[:100]}{'...' if len(field.value) > 100 else ''}")
else:
    print("❌ No stats found - embed cannot be created")
