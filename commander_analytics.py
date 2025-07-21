"""
Enhanced game analytics for Commander games.
Provides detailed statistics and trends analysis.
"""

import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
import discord
from config import EMBED_COLORS, COLOR_EMOJIS


class CommanderAnalytics:
    """Advanced analytics for commander games."""
    
    def __init__(self, stats_file: str):
        self.stats_file = stats_file
    
    def get_server_meta_analysis(self, channel_id: Optional[int] = None, days: int = 30) -> Dict:
        """Get meta analysis for server or channel."""
        try:
            if not os.path.exists(self.stats_file):
                return {}
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            stats = {
                'total_games': 0,
                'total_players': set(),
                'commander_popularity': Counter(),
                'color_popularity': Counter(),
                'color_combinations': Counter(),
                'win_rates_by_commander': defaultdict(list),
                'average_game_size': 0,
                'most_active_players': Counter(),
                'recent_trends': {},
                'meta_tier_list': []
            }
            
            game_sizes = []
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                games_by_id = defaultdict(list)
                
                for row in reader:
                    game_date = datetime.strptime(f"{row['date']} {row['time']}", '%Y-%m-%d %H:%M')
                    if game_date < cutoff_date:
                        continue
                    
                    # Collect data for analysis
                    games_by_id[f"{row['date']}_{row['time']}_{row['total_players']}"].append(row)
                    stats['total_players'].add(int(row['user_id']))
                    stats['most_active_players'][row['username']] += 1
                    
                    commander = row['commander']
                    placement = int(row['placement'])
                    colors = row['colors'].split(',') if row['colors'] != '?' else []
                    
                    stats['commander_popularity'][commander] += 1
                    stats['win_rates_by_commander'][commander].append(placement)
                    
                    # Color analysis
                    if colors and colors != ['?']:
                        for color in colors:
                            if color != '?':
                                stats['color_popularity'][color] += 1
                        
                        color_combo = ','.join(sorted(colors))
                        stats['color_combinations'][color_combo] += 1
                
                # Calculate game statistics
                stats['total_games'] = len(games_by_id)
                for game_players in games_by_id.values():
                    game_sizes.append(len(game_players))
                
                if game_sizes:
                    stats['average_game_size'] = sum(game_sizes) / len(game_sizes)
                
                # Calculate win rates and create tier list
                commander_win_rates = {}
                for commander, placements in stats['win_rates_by_commander'].items():
                    if len(placements) >= 3:  # Minimum games for tier list
                        wins = sum(1 for p in placements if p == 1)
                        win_rate = wins / len(placements) * 100
                        commander_win_rates[commander] = {
                            'win_rate': win_rate,
                            'games_played': len(placements),
                            'average_placement': sum(placements) / len(placements)
                        }
                
                # Create tier list (sorted by win rate with minimum games filter)
                stats['meta_tier_list'] = sorted(
                    commander_win_rates.items(),
                    key=lambda x: x[1]['win_rate'],
                    reverse=True
                )[:10]  # Top 10
            
            stats['total_players'] = len(stats['total_players'])
            return stats
            
        except Exception as e:
            print(f"Error in meta analysis: {e}")
            return {}
    
    def get_player_trends(self, user_id: int, days: int = 30) -> Dict:
        """Get trending data for a specific player."""
        try:
            if not os.path.exists(self.stats_file):
                return {}
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            trends = {
                'recent_performance': [],
                'favorite_colors_trend': Counter(),
                'commander_success_rate': defaultdict(list),
                'improvement_trend': 0,
                'current_streak': {'type': None, 'count': 0},
                'weekly_activity': defaultdict(int)
            }
            
            recent_games = []
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) != user_id:
                        continue
                    
                    game_date = datetime.strptime(f"{row['date']} {row['time']}", '%Y-%m-%d %H:%M')
                    if game_date < cutoff_date:
                        continue
                    
                    placement = int(row['placement'])
                    commander = row['commander']
                    colors = row['colors'].split(',') if row['colors'] != '?' else []
                    
                    recent_games.append({
                        'date': game_date,
                        'placement': placement,
                        'commander': commander,
                        'colors': colors
                    })
                    
                    # Track color trends
                    for color in colors:
                        if color != '?':
                            trends['favorite_colors_trend'][color] += 1
                    
                    # Track commander success
                    trends['commander_success_rate'][commander].append(placement)
                    
                    # Weekly activity
                    week = game_date.strftime('%Y-W%U')
                    trends['weekly_activity'][week] += 1
            
            # Sort games by date
            recent_games.sort(key=lambda x: x['date'])
            
            # Calculate performance trend
            if len(recent_games) >= 5:
                recent_placements = [g['placement'] for g in recent_games[-10:]]
                early_avg = sum(recent_placements[:5]) / 5
                late_avg = sum(recent_placements[-5:]) / 5
                trends['improvement_trend'] = early_avg - late_avg  # Positive = improving
            
            # Calculate current streak
            if recent_games:
                last_placement = recent_games[-1]['placement']
                streak_count = 1
                streak_type = 'win' if last_placement == 1 else 'loss' if last_placement > 2 else 'podium'
                
                for game in reversed(recent_games[:-1]):
                    if streak_type == 'win' and game['placement'] == 1:
                        streak_count += 1
                    elif streak_type == 'podium' and game['placement'] <= 3:
                        streak_count += 1
                    elif streak_type == 'loss' and game['placement'] > 2:
                        streak_count += 1
                    else:
                        break
                
                trends['current_streak'] = {'type': streak_type, 'count': streak_count}
            
            trends['recent_performance'] = recent_games[-10:]  # Last 10 games
            return trends
            
        except Exception as e:
            print(f"Error in player trends: {e}")
            return {}
    
    def get_matchup_analysis(self, commander1: str, commander2: str) -> Dict:
        """Analyze head-to-head matchups between commanders."""
        try:
            if not os.path.exists(self.stats_file):
                return {}
            
            matchups = {
                'total_games': 0,
                'commander1_wins': 0,
                'commander2_wins': 0,
                'games_details': []
            }
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                games_by_id = defaultdict(list)
                
                for row in reader:
                    games_by_id[f"{row['date']}_{row['time']}_{row['total_players']}"].append(row)
                
                # Find games with both commanders
                for game_id, players in games_by_id.items():
                    commanders_in_game = [p['commander'] for p in players]
                    
                    if commander1 in commanders_in_game and commander2 in commanders_in_game:
                        matchups['total_games'] += 1
                        
                        # Find who won
                        winner_commander = None
                        for player in players:
                            if int(player['placement']) == 1:
                                winner_commander = player['commander']
                                break
                        
                        if winner_commander == commander1:
                            matchups['commander1_wins'] += 1
                        elif winner_commander == commander2:
                            matchups['commander2_wins'] += 1
                        
                        # Store game details
                        game_details = {
                            'game_id': game_id,
                            'winner': winner_commander,
                            'players': len(players),
                            'date': players[0]['game_date']
                        }
                        matchups['games_details'].append(game_details)
            
            return matchups
            
        except Exception as e:
            print(f"Error in matchup analysis: {e}")
            return {}


def create_meta_analysis_embed(stats: Dict, days: int = 30) -> discord.Embed:
    """Create embed for server meta analysis."""
    embed = discord.Embed(
        title="📊 Server Commander Meta Analysis",
        color=EMBED_COLORS.get('commander_stats', 0x8B4513),
        description=f"Analysis of the last {days} days"
    )
    
    if not stats:
        embed.add_field(
            name="📝 No Data",
            value="No games found in the specified time period.",
            inline=False
        )
        return embed
    
    # Overview stats
    embed.add_field(
        name="🎮 Overview",
        value=(
            f"**Games Played:** {stats['total_games']}\n"
            f"**Active Players:** {stats['total_players']}\n"
            f"**Average Game Size:** {stats['average_game_size']:.1f} players"
        ),
        inline=True
    )
    
    # Most popular commanders
    if stats['commander_popularity']:
        top_commanders = stats['commander_popularity'].most_common(5)
        commanders_text = ""
        for i, (commander, count) in enumerate(top_commanders, 1):
            commanders_text += f"{i}. **{commander}** - {count} games\n"
        
        embed.add_field(
            name="🎯 Most Popular Commanders",
            value=commanders_text,
            inline=True
        )
    
    # Color popularity
    if stats['color_popularity']:
        color_map = {
            'W': COLOR_EMOJIS.get('white', '⚪'),
            'U': COLOR_EMOJIS.get('blue', '🔵'),
            'B': COLOR_EMOJIS.get('black', '⚫'),
            'R': COLOR_EMOJIS.get('red', '🔴'),
            'G': COLOR_EMOJIS.get('green', '🟢'),
            'C': COLOR_EMOJIS.get('colorless', '⚪')
        }
        
        colors_text = ""
        for color, count in stats['color_popularity'].most_common(5):
            emoji = color_map.get(color, '❓')
            colors_text += f"{emoji} **{count}** games\n"
        
        embed.add_field(
            name="🌈 Color Popularity",
            value=colors_text,
            inline=True
        )
    
    # Meta tier list
    if stats['meta_tier_list']:
        tier_text = ""
        for i, (commander, data) in enumerate(stats['meta_tier_list'][:5], 1):
            tier_text += f"{i}. **{commander}**\n   Win Rate: {data['win_rate']:.1f}% ({data['games_played']} games)\n"
        
        embed.add_field(
            name="🏆 Meta Tier List (Top 5)",
            value=tier_text,
            inline=False
        )
    
    # Most active players
    if stats['most_active_players']:
        active_text = ""
        for player, games in stats['most_active_players'].most_common(3):
            active_text += f"**{player}** - {games} games\n"
        
        embed.add_field(
            name="🔥 Most Active Players",
            value=active_text,
            inline=True
        )
    
    embed.set_footer(text=f"📈 Analyzed {stats['total_games']} games from {stats['total_players']} players")
    
    return embed


def create_player_trends_embed(user_id: int, username: str, trends: Dict) -> discord.Embed:
    """Create embed for player trends analysis."""
    embed = discord.Embed(
        title=f"📈 Trends Analysis for {username}",
        color=EMBED_COLORS.get('commander_stats', 0x8B4513),
        description="Your recent performance and trends"
    )
    
    if not trends or not trends.get('recent_performance'):
        embed.add_field(
            name="📝 No Recent Data",
            value="No games found in the last 30 days.",
            inline=False
        )
        return embed
    
    # Performance trend
    if trends['improvement_trend'] != 0:
        trend_emoji = "📈" if trends['improvement_trend'] > 0 else "📉"
        trend_text = "improving" if trends['improvement_trend'] > 0 else "declining"
        
        embed.add_field(
            name=f"{trend_emoji} Performance Trend",
            value=f"Your average placement is **{trend_text}** by {abs(trends['improvement_trend']):.1f} positions",
            inline=True
        )
    
    # Current streak
    if trends['current_streak']['count'] > 1:
        streak = trends['current_streak']
        streak_emojis = {'win': '🔥', 'podium': '🎯', 'loss': '💀'}
        emoji = streak_emojis.get(streak['type'], '📊')
        
        embed.add_field(
            name=f"{emoji} Current Streak",
            value=f"{streak['count']} {streak['type']}{'s' if streak['count'] > 1 else ''} in a row",
            inline=True
        )
    
    # Recent color trends
    if trends['favorite_colors_trend']:
        color_map = {
            'W': COLOR_EMOJIS.get('white', '⚪'),
            'U': COLOR_EMOJIS.get('blue', '🔵'),
            'B': COLOR_EMOJIS.get('black', '⚫'),
            'R': COLOR_EMOJIS.get('red', '🔴'),
            'G': COLOR_EMOJIS.get('green', '🟢'),
            'C': COLOR_EMOJIS.get('colorless', '⚪')
        }
        
        colors_text = ""
        for color, count in trends['favorite_colors_trend'].most_common(3):
            emoji = color_map.get(color, '❓')
            colors_text += f"{emoji} {count} games  "
        
        embed.add_field(
            name="🎨 Recent Color Preference",
            value=colors_text,
            inline=True
        )
    
    # Recent performance summary
    recent_games = trends['recent_performance'][-5:]  # Last 5 games
    performance_text = ""
    
    for i, game in enumerate(recent_games):
        place_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"][game['placement'] - 1]
        performance_text += f"{place_emoji} {game['commander']}\n"
    
    embed.add_field(
        name="🎯 Last 5 Games",
        value=performance_text,
        inline=False
    )
    
    # Weekly activity
    if trends['weekly_activity']:
        total_weeks = len(trends['weekly_activity'])
        total_games = sum(trends['weekly_activity'].values())
        avg_games_per_week = total_games / total_weeks
        
        embed.add_field(
            name="📅 Activity Level",
            value=f"**{avg_games_per_week:.1f}** games per week on average",
            inline=True
        )
    
    embed.set_footer(text=f"📊 Based on {len(trends['recent_performance'])} recent games")
    
    return embed


# Initialize global analytics instance
analytics = CommanderAnalytics('commander_stats.csv')
