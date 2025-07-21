#!/usr/bin/env python3

"""
Test script to verify commander stats functionality after fixing column issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commander_games import commander_manager

def test_commander_stats():
    """Test the commander stats functionality."""
    print("Testing commander stats after column fixes...")
    
    # Test InFeRMuS user (ID from dummy data)
    user_id = 123456789012345678
    username = "InFeRMuS"
    
    try:
        # Get player stats
        stats = commander_manager.get_player_stats(user_id)
        
        if stats:
            print("✅ SUCCESS! Stats retrieved successfully")
            print(f"📊 Total games: {stats.get('total_games', 0)}")
            print(f"🏆 Wins: {stats.get('wins', 0)}")
            print(f"📈 Win rate: {stats.get('win_rate', 0):.1f}%")
            print(f"🎯 Average placement: {stats.get('avg_placement', 0):.1f}")
            print(f"🎴 Commanders played: {len(stats.get('commanders_played', []))}")
            print(f"🌈 Colors played: {len(stats.get('colors_played', []))}")
            
            if stats.get('favorite_commander'):
                print(f"⭐ Favorite commander: {stats['favorite_commander']}")
            
            return True
        else:
            print("❌ No stats found for user")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_commander_stats()
    sys.exit(0 if success else 1)
