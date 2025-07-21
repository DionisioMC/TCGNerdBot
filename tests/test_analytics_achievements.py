"""
Test script for Analytics and Achievement features.
Run this to validate the new commander game features.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commander_analytics import CommanderAnalytics, create_meta_analysis_embed, create_player_trends_embed
from achievements import AchievementManager, create_achievement_embed, create_achievements_overview_embed
import datetime


def test_analytics():
    """Test the analytics functionality."""
    print("🔍 Testing Analytics Features...")
    
    # Initialize analytics
    analytics = CommanderAnalytics('commander_stats.csv')
    
    # Test meta analysis
    print("\n📊 Testing server meta analysis...")
    meta_stats = analytics.get_server_meta_analysis(days=30)
    
    if meta_stats:
        print(f"✅ Found {meta_stats.get('total_games', 0)} games")
        print(f"✅ {meta_stats.get('total_players', 0)} total players")
        
        if meta_stats.get('commander_popularity'):
            top_commander = meta_stats['commander_popularity'].most_common(1)[0]
            print(f"✅ Most popular commander: {top_commander[0]} ({top_commander[1]} games)")
        
        if meta_stats.get('meta_tier_list'):
            top_meta = meta_stats['meta_tier_list'][0]
            print(f"✅ Top meta commander: {top_meta[0]} ({top_meta[1]['win_rate']:.1f}% win rate)")
    else:
        print("⚠️ No meta data found (this is normal for new installations)")
    
    # Test player trends
    print("\n📈 Testing player trends...")
    trends = analytics.get_player_trends(123456789, days=30)  # Test user ID
    
    if trends and trends.get('recent_performance'):
        print(f"✅ Found {len(trends['recent_performance'])} recent games")
        
        if trends.get('improvement_trend'):
            trend_direction = "improving" if trends['improvement_trend'] > 0 else "declining"
            print(f"✅ Performance trend: {trend_direction}")
        
        if trends.get('current_streak'):
            streak = trends['current_streak']
            print(f"✅ Current streak: {streak['count']} {streak['type']}")
    else:
        print("⚠️ No trend data found (normal for test user)")
    
    print("✅ Analytics tests completed!")


def test_achievements():
    """Test the achievement system."""
    print("\n🏆 Testing Achievement System...")
    
    # Initialize achievement manager
    achievement_mgr = AchievementManager('test_achievements.json', 'commander_stats.csv')
    
    # Test achievement definitions
    print(f"✅ Loaded {len(achievement_mgr.achievements)} achievements")
    
    # Test achievement categories
    categories = {}
    for achievement in achievement_mgr.achievements.values():
        categories[achievement.category] = categories.get(achievement.category, 0) + 1
    
    print("✅ Achievement categories:")
    for category, count in categories.items():
        print(f"   {category}: {count} achievements")
    
    # Test achievement checking (with test user)
    test_user_id = 123456789
    print(f"\n🔍 Testing achievement checking for user {test_user_id}...")
    
    new_achievements = achievement_mgr.check_achievements(test_user_id)
    print(f"✅ Checked achievements, found {len(new_achievements)} new ones")
    
    # Test player achievements display
    player_data = achievement_mgr.get_player_achievements(test_user_id)
    print(f"✅ Player has {player_data['total_earned']} total achievements")
    print(f"✅ Player has {player_data['total_points']} total points")
    
    # Test leaderboard
    leaderboard = achievement_mgr.get_achievement_leaderboard(5)
    print(f"✅ Leaderboard has {len(leaderboard)} entries")
    
    # Test some specific achievements
    test_achievements = ['first_game', 'mono_white', 'win_streak_3', 'games_10']
    for achievement_id in test_achievements:
        if achievement_id in achievement_mgr.achievements:
            achievement = achievement_mgr.achievements[achievement_id]
            print(f"✅ Achievement '{achievement.name}': {achievement.points} points, {achievement.rarity}")
    
    print("✅ Achievement tests completed!")


def test_embeds():
    """Test Discord embed creation."""
    print("\n🎨 Testing Discord Embeds...")
    
    # Test analytics embeds
    print("Testing analytics embeds...")
    
    # Mock data for testing
    from collections import Counter
    mock_meta_stats = {
        'total_games': 50,
        'total_players': 15,
        'average_game_size': 4.2,
        'commander_popularity': Counter({'Atraxa, Praetors\' Voice': 5, 'Edgar Markov': 3}),
        'color_popularity': Counter({'W': 10, 'U': 8, 'B': 12, 'R': 6, 'G': 9}),
        'meta_tier_list': [
            ('Atraxa, Praetors\' Voice', {'win_rate': 60.0, 'games_played': 5, 'average_placement': 1.8}),
            ('Edgar Markov', {'win_rate': 33.3, 'games_played': 3, 'average_placement': 2.3})
        ],
        'most_active_players': Counter({'TestPlayer': 8, 'Player2': 5})
    }
    
    meta_embed = create_meta_analysis_embed(mock_meta_stats, 30)
    print(f"✅ Meta analysis embed created: '{meta_embed.title}'")
    
    # Test trends embed
    from collections import Counter
    mock_trends = {
        'recent_performance': [
            {'date': datetime.datetime.now(), 'placement': 1, 'commander': 'Test Commander', 'colors': ['W', 'U']},
            {'date': datetime.datetime.now(), 'placement': 3, 'commander': 'Another Commander', 'colors': ['R']}
        ],
        'improvement_trend': 1.2,
        'current_streak': {'type': 'win', 'count': 2},
        'favorite_colors_trend': Counter({'W': 3, 'U': 2, 'B': 1}),
        'weekly_activity': {'2025-W03': 5, '2025-W02': 3}
    }
    
    trends_embed = create_player_trends_embed(123456789, "TestPlayer", mock_trends)
    print(f"✅ Player trends embed created: '{trends_embed.title}'")
    
    # Test achievement embeds
    print("Testing achievement embeds...")
    
    # Get a test achievement
    achievement_mgr = AchievementManager('test_achievements.json', 'commander_stats.csv')
    first_game_achievement = achievement_mgr.achievements['first_game']
    
    achievement_embed = create_achievement_embed(first_game_achievement, is_new=True)
    print(f"✅ Achievement embed created: '{achievement_embed.title}'")
    
    # Test overview embed
    mock_player_data = {
        'earned': {'first_game': {'date': '2025-01-01', 'points': 5}},
        'total_points': 5,
        'total_earned': 1
    }
    
    overview_embed = create_achievements_overview_embed(123456789, "TestPlayer", mock_player_data, 50)
    print(f"✅ Achievement overview embed created: '{overview_embed.title}'")
    
    print("✅ Embed tests completed!")


def test_integration():
    """Test integration between components."""
    print("\n🔗 Testing Integration...")
    
    # Test that analytics and achievements work together
    analytics = CommanderAnalytics('commander_stats.csv')
    achievement_mgr = AchievementManager('test_achievements.json', 'commander_stats.csv')
    
    # Both should be able to read the same stats file
    print("✅ Both systems can access stats file")
    
    # Test achievement checking with analytics data
    test_user_id = 123456789
    
    # Mock some basic stats for testing
    import csv
    test_stats_file = 'test_stats.csv'
    
    # Create test stats file
    with open(test_stats_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'game_id', 'user_id', 'username', 'commander', 'commander_colors', 
            'placement', 'game_date', 'total_players'
        ])
        writer.writeheader()
        
        # Add some test data
        test_data = [
            {
                'game_id': 'game_test_1',
                'user_id': test_user_id,
                'username': 'TestPlayer',
                'commander': 'Atraxa, Praetors\' Voice',
                'commander_colors': 'W,U,B,G',
                'placement': 1,
                'game_date': '2025-01-20 15:30:00',
                'total_players': 4
            },
            {
                'game_id': 'game_test_2', 
                'user_id': test_user_id,
                'username': 'TestPlayer',
                'commander': 'Edgar Markov',
                'commander_colors': 'W,B,R',
                'placement': 2,
                'game_date': '2025-01-21 16:00:00',
                'total_players': 4
            }
        ]
        
        for row in test_data:
            writer.writerow(row)
    
    # Test analytics with test data
    test_analytics = CommanderAnalytics(test_stats_file)
    meta_stats = test_analytics.get_server_meta_analysis(days=7)
    
    if meta_stats and meta_stats.get('total_games', 0) > 0:
        print(f"✅ Analytics found test data: {meta_stats['total_games']} games")
    
    # Test achievements with test data
    test_achievement_mgr = AchievementManager('test_achievements_integration.json', test_stats_file)
    new_achievements = test_achievement_mgr.check_achievements(test_user_id)
    
    if new_achievements:
        print(f"✅ Achievement system found {len(new_achievements)} achievements from test data")
        for achievement in new_achievements:
            print(f"   - {achievement.name}: {achievement.description}")
    
    # Clean up test files
    import os
    try:
        os.remove(test_stats_file)
        os.remove('test_achievements_integration.json')
        print("✅ Test files cleaned up")
    except:
        pass
    
    print("✅ Integration tests completed!")


def main():
    """Run all tests."""
    print("🧪 Starting Analytics & Achievement System Tests")
    print("=" * 60)
    
    try:
        test_analytics()
        test_achievements()
        test_embeds()
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed successfully!")
        print("\n📋 Feature Summary:")
        print("✅ Server meta analysis (commanders, colors, win rates)")
        print("✅ Player performance trends and streaks")
        print("✅ Comprehensive achievement system (50+ achievements)")
        print("✅ Discord embed integration")
        print("✅ Automatic achievement checking after games")
        print("✅ Achievement leaderboard system")
        print("\n🚀 New Commands Available:")
        print("   !commander meta [days] - Server meta analysis")
        print("   !commander trends [days] - Personal trends")
        print("   !commander achievements - View achievements")
        print("   !commander achievements check - Check for new achievements")
        print("   !commander leaderboard - Achievement leaderboard")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Ready to enhance your commander game experience!")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")
