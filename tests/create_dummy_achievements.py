#!/usr/bin/env python3
"""
Script to create dummy achievements for testing Discord display.
Adds achievements for user "InFeRMuS".
"""

import json
import csv
from datetime import datetime, timedelta
from achievements import achievement_manager, Achievement, create_achievement_embed
import random

def create_dummy_user_data():
    """Create dummy data for InFeRMuS user."""
    
    # Use a dummy Discord user ID (Discord IDs are typically 17-18 digit snowflakes)
    infermus_user_id = 123456789012345678  # Dummy ID for InFeRMuS
    
    print(f"🎮 Creating dummy achievements for InFeRMuS (ID: {infermus_user_id})")
    
    # Create some dummy game stats first
    create_dummy_commander_stats(infermus_user_id)
    
    # Manually award some interesting achievements
    achievements_to_award = [
        'first_game',
        'first_win', 
        'games_10',
        'wins_5',
        'win_streak_3',
        'mono_red',
        'mono_blue',
        'different_commanders_10',
        'speed_demon',
        'night_owl',
        'comeback_king'  # This one is hidden!
    ]
    
    # Initialize player achievements if not exists
    if infermus_user_id not in achievement_manager.player_achievements:
        achievement_manager.player_achievements[infermus_user_id] = {
            'earned': {},
            'progress': {},
            'total_points': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    player_data = achievement_manager.player_achievements[infermus_user_id]
    total_points = 0
    
    print(f"\n🏆 Awarding {len(achievements_to_award)} achievements:")
    
    for achievement_id in achievements_to_award:
        if achievement_id in achievement_manager.achievements:
            achievement = achievement_manager.achievements[achievement_id]
            
            # Award the achievement
            player_data['earned'][achievement_id] = {
                'earned_at': datetime.now().isoformat(),
                'progress': 100
            }
            
            total_points += achievement.points
            
            print(f"  {achievement.emoji} {achievement.name} - {achievement.points} pts")
            print(f"     \"{achievement.description}\"")
        else:
            print(f"  ❌ Achievement '{achievement_id}' not found!")
    
    # Update total points
    player_data['total_points'] = total_points
    player_data['last_updated'] = datetime.now().isoformat()
    
    # Save the achievements
    achievement_manager._save_player_achievements()
    
    print(f"\n✅ Successfully awarded {len(achievements_to_award)} achievements!")
    print(f"💎 Total points earned: {total_points}")
    print(f"📁 Achievements saved to: {achievement_manager.achievements_file}")
    
    return infermus_user_id

def create_dummy_commander_stats(user_id):
    """Create dummy commander game stats for the user."""
    
    # Create some realistic game data
    games_data = []
    
    # Generate 15 games over the past month
    base_date = datetime.now() - timedelta(days=30)
    
    commanders = [
        ("Krenko, Mob Boss", "Goblins", "red"),
        ("Talrand, Sky Summoner", "Tokens", "blue"), 
        ("Ghalta, Primal Hunger", "Stompy", "green"),
        ("Krenko, Tin Street Kingpin", "Aggro", "red"),
        ("Braids, Conjurer Adept", "Group Hug", "blue"),
        ("Alesha, Who Smiles at Death", "Reanimator", "mardu"),
        ("Yuriko, the Tiger's Shadow", "Ninjas", "dimir"),
        ("Edgar Markov", "Vampires", "mardu"),
        ("Atraxa, Praetors' Voice", "Superfriends", "glint"),
        ("The Ur-Dragon", "Dragons", "wubrg")
    ]
    
    for i in range(15):
        game_date = base_date + timedelta(days=random.randint(0, 30))
        commander, archetype, colors = random.choice(commanders)
        
        # Create a mix of placements (some wins, some losses)
        if i < 5:  # First 5 games: learning period
            placement = random.choice([2, 3, 4])
        elif i < 10:  # Middle games: getting better
            placement = random.choice([1, 2, 3])
        else:  # Recent games: doing well, including a win streak
            if i >= 12:  # Last 3 games are a win streak
                placement = 1
            else:
                placement = random.choice([1, 2])
        
        # Some games late at night for "Night Owl" achievement
        hour = random.choice([2, 14, 20, 22]) if i % 5 == 0 else random.randint(10, 23)
        game_time = game_date.replace(hour=hour, minute=random.randint(0, 59))
        
        game_data = {
            'date': game_time.strftime('%Y-%m-%d'),
            'time': game_time.strftime('%H:%M'),
            'user_id': user_id,
            'username': 'InFeRMuS',
            'commander': commander,
            'archetype': archetype,
            'colors': colors,
            'placement': placement,
            'total_players': 4,
            'game_length': random.randint(45, 120),  # minutes
            'notes': f"Game {i+1} - {'Win!' if placement == 1 else f'Placed {placement}'}"
        }
        
        games_data.append(game_data)
    
    # Write to CSV file
    csv_file = achievement_manager.stats_file
    
    # Check if file exists and read existing data
    existing_data = []
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = [row for row in reader if int(row.get('user_id', 0)) != user_id]
    except FileNotFoundError:
        pass
    
    # Combine with new data
    all_data = existing_data + games_data
    
    # Write all data back
    if all_data:
        fieldnames = ['date', 'time', 'user_id', 'username', 'commander', 'archetype', 
                     'colors', 'placement', 'total_players', 'game_length', 'notes']
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
    
    print(f"📊 Created {len(games_data)} dummy games for InFeRMuS")
    print(f"📁 Stats saved to: {csv_file}")

def test_achievement_display(user_id):
    """Test the achievement display functionality."""
    print(f"\n🎨 Testing Achievement Display for user {user_id}:")
    
    # Get some achievements to display
    player_data = achievement_manager.player_achievements.get(user_id, {})
    earned_achievements = player_data.get('earned', {})
    
    if not earned_achievements:
        print("❌ No achievements found for user!")
        return
    
    print(f"🏆 Found {len(earned_achievements)} earned achievements")
    
    # Display a few different types of achievements
    sample_achievements = list(earned_achievements.keys())[:3]
    
    for achievement_id in sample_achievements:
        if achievement_id in achievement_manager.achievements:
            achievement = achievement_manager.achievements[achievement_id]
            print(f"\n{achievement.emoji} {achievement.name}")
            print(f"   Description: {achievement.description}")
            print(f"   Rarity: {achievement.rarity}")
            print(f"   Points: {achievement.points}")
            print(f"   Category: {achievement.category}")
            
            # Show what the Discord embed would look like
            print(f"   📱 Discord Embed Preview:")
            print(f"      Title: 🎉 Achievement Unlocked!")
            print(f"      Color: Based on {achievement.rarity} rarity")
            print(f"      Fields: Name, Description, Rarity, Points, Category")

def main():
    """Main function to create dummy achievements."""
    print("🚀 Starting Dummy Achievement Creation for InFeRMuS")
    print("=" * 60)
    
    try:
        # Create the dummy data
        user_id = create_dummy_user_data()
        
        # Test the display
        test_achievement_display(user_id)
        
        print("\n" + "=" * 60)
        print("✅ DUMMY ACHIEVEMENTS CREATION COMPLETE!")
        print(f"🎮 User 'InFeRMuS' (ID: {user_id}) now has achievements!")
        print("💡 You can now test Discord commands like:")
        print("   !commander achievements")
        print("   !commander achievements check") 
        print("   !commander leaderboard")
        
    except Exception as e:
        print(f"❌ Error creating dummy achievements: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
