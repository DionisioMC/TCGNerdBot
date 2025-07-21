#!/usr/bin/env python3

"""
Test script to verify commander analytics functionality after fixing column issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commander_analytics import analytics

def test_commander_analytics():
    """Test the commander analytics functionality."""
    print("Testing commander analytics after column fixes...")
    
    try:
        # Test server meta analysis
        print("\n🔍 Testing server meta analysis...")
        meta_stats = analytics.get_server_meta_analysis(days=30)
        
        if meta_stats:
            print(f"✅ Meta analysis successful!")
            print(f"📊 Total games: {meta_stats.get('total_games', 0)}")
            print(f"👥 Total players: {meta_stats.get('total_players', 0)}")
            print(f"🎯 Average game size: {meta_stats.get('average_game_size', 0):.1f}")
            
            if meta_stats.get('commander_popularity'):
                top_commanders = list(meta_stats['commander_popularity'].most_common(3))
                print(f"🏆 Top commanders: {[cmd[0] for cmd in top_commanders]}")
        
        # Test player trends
        print("\n📈 Testing player trends...")
        user_id = 123456789012345678
        trends = analytics.get_player_trends(user_id, days=30)
        
        if trends:
            print(f"✅ Player trends successful!")
            print(f"🎮 Recent performance: {len(trends.get('recent_performance', []))} games")
            print(f"🔥 Current streak: {trends.get('current_streak', {})}")
            
        # Test matchup analysis
        print("\n⚔️ Testing matchup analysis...")
        matchup = analytics.get_matchup_analysis("Yuriko, the Tiger's Shadow", "Edgar Markov")
        
        if matchup:
            print(f"✅ Matchup analysis successful!")
            print(f"🎯 Total matchups: {matchup.get('total_games', 0)}")
            
        return True
        
    except Exception as e:
        print(f"❌ ERROR in analytics: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_commander_analytics()
    sys.exit(0 if success else 1)
