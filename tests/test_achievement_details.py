#!/usr/bin/env python3
"""
Test script for the new achievement detail command functionality.
Demonstrates the new !commander achievements info <achievement> command.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from achievements import achievement_manager, create_achievement_detail_embed
import asyncio

async def test_achievement_detail_command():
    """Test the achievement detail functionality."""
    print("🧪 Testing Achievement Detail Command")
    print("=" * 50)
    
    # Test finding different types of achievements
    test_cases = [
        "first_win",           # Test by ID
        "Victory Royale",      # Test by exact name
        "legendary",           # Test partial name match
        "nonexistent"          # Test not found case
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Searching for: '{test_case}'")
        achievement = achievement_manager.find_achievement(test_case)
        
        if achievement:
            print(f"✅ Found: {achievement.emoji} {achievement.name}")
            print(f"   ID: {achievement.id}")
            print(f"   Description: {achievement.description}")
            print(f"   Category: {achievement.category}")
            print(f"   Rarity: {achievement.rarity}")
            print(f"   Points: {achievement.points}")
            print(f"   Hidden: {achievement.hidden}")
        else:
            print(f"❌ Not found: '{test_case}'")
    
    print("\n" + "=" * 50)
    print("🎯 Testing Embed Creation")
    print("=" * 50)
    
    # Test embed creation for a specific achievement
    achievement = achievement_manager.find_achievement("first_win")
    if achievement:
        # Test with user who has earned it
        user_id = 352817681654743041  # Test user from our corrected CSV
        player_data = achievement_manager.get_player_achievements(user_id)
        user_has_earned = achievement.id in player_data['earned']
        earned_date = None
        
        if user_has_earned:
            earned_info = player_data['earned'][achievement.id]
            earned_date = earned_info.get('earned_at') or earned_info.get('date')
        
        # Calculate stats
        total_players = len(achievement_manager.player_achievements)
        earned_by_count = 0
        for player_data_item in achievement_manager.player_achievements.values():
            if achievement.id in player_data_item['earned']:
                earned_by_count += 1
        
        print(f"📊 Achievement: {achievement.name}")
        print(f"   User has earned: {user_has_earned}")
        print(f"   Earned date: {earned_date}")
        print(f"   Earned by {earned_by_count}/{total_players} players")
        
        if total_players > 0:
            percentage = (earned_by_count / total_players) * 100
            print(f"   Completion rate: {percentage:.1f}%")
    
    print("\n✅ Achievement detail command testing complete!")

if __name__ == "__main__":
    asyncio.run(test_achievement_detail_command())
