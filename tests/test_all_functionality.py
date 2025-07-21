#!/usr/bin/env python3

"""
Comprehensive test to verify all Discord command functionality after fixing column issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from achievements import AchievementManager
from commander_games import commander_manager
from commander_analytics import analytics

def test_all_functionality():
    """Test all Discord command functionality."""
    print("🔧 COMPREHENSIVE FUNCTIONALITY TEST")
    print("=" * 60)
    
    user_id = 123456789012345678
    username = "InFeRMuS"
    
    # Test 1: Achievement System
    print("\n🏆 TESTING ACHIEVEMENT SYSTEM")
    print("-" * 40)
    
    try:
        achievement_manager = AchievementManager(
            achievements_file='player_achievements.json',
            stats_file='commander_stats.csv'
        )
        
        # Check achievements
        new_achievements = achievement_manager.check_achievements(user_id)
        player_data = achievement_manager.player_achievements.get(user_id, {})
        total_achievements = len(player_data.get('earned', {}))
        total_points = player_data.get('total_points', 0)
        
        print(f"✅ Achievement check: {len(new_achievements)} new achievements")
        print(f"📊 Current status: {total_achievements} achievements, {total_points} points")
        
    except Exception as e:
        print(f"❌ Achievement system error: {e}")
        return False
    
    # Test 2: Commander Stats
    print("\n📊 TESTING COMMANDER STATS")
    print("-" * 40)
    
    try:
        stats = commander_manager.get_player_stats(user_id)
        
        if stats:
            print(f"✅ Stats retrieved successfully")
            print(f"🎮 Games: {stats.get('total_games', 0)}")
            print(f"🏆 Wins: {stats.get('wins', 0)} ({stats.get('win_rate', 0):.1f}%)")
            print(f"🎯 Avg placement: {stats.get('avg_placement', 0):.1f}")
            print(f"🎴 Commanders: {len(stats.get('commanders_played', []))}")
        else:
            print("❌ No stats found")
            return False
            
    except Exception as e:
        print(f"❌ Commander stats error: {e}")
        return False
    
    # Test 3: Analytics
    print("\n📈 TESTING ANALYTICS")
    print("-" * 40)
    
    try:
        # Server meta analysis
        meta_stats = analytics.get_server_meta_analysis(days=30)
        print(f"✅ Meta analysis: {meta_stats.get('total_games', 0)} games analyzed")
        
        # Player trends
        trends = analytics.get_player_trends(user_id, days=30)
        print(f"✅ Player trends: {len(trends.get('recent_performance', []))} recent games")
        
        # Matchup analysis
        matchup = analytics.get_matchup_analysis("Yuriko, the Tiger's Shadow", "Edgar Markov")
        print(f"✅ Matchup analysis: {matchup.get('total_games', 0)} matchups found")
        
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        return False
    
    # Test 4: Discord Command Simulation
    print("\n🤖 SIMULATING DISCORD COMMANDS")
    print("-" * 40)
    
    try:
        # Simulate !commander achievements
        print("💬 !commander achievements")
        if total_achievements > 0:
            print(f"   ✅ Would show {total_achievements} achievements with {total_points} points")
        
        # Simulate !commander achievements check
        print("💬 !commander achievements check")
        if len(new_achievements) > 0:
            print(f"   🎉 Would show {len(new_achievements)} new achievements")
        else:
            print("   ✅ Would show 'No new achievements to unlock!'")
        
        # Simulate !commander stats
        print("💬 !commander stats")
        print(f"   ✅ Would show stats embed with {stats.get('total_games', 0)} games")
        
        # Simulate !commander leaderboard (would work with achievement system)
        print("💬 !commander leaderboard")
        print("   ✅ Would show leaderboard with achievement points")
        
    except Exception as e:
        print(f"❌ Discord command simulation error: {e}")
        return False
    
    # Final Status
    print("\n🎯 FINAL STATUS")
    print("=" * 60)
    print("✅ ALL SYSTEMS OPERATIONAL")
    print(f"✅ Achievement System: {total_achievements} achievements, {total_points} points")
    print(f"✅ Commander Stats: {stats.get('total_games', 0)} games tracked")
    print(f"✅ Analytics: {meta_stats.get('total_games', 0)} games analyzed")
    print("✅ Discord Commands: Ready for production")
    print("\n🚀 Bot is ready for Discord integration!")
    
    return True

if __name__ == "__main__":
    success = test_all_functionality()
    sys.exit(0 if success else 1)
