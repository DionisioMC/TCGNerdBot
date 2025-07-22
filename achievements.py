"""
Achievement system for Commander games.
Tracks various achievements and milestones for players.
"""

import json
import os
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, Counter
import discord
from config import EMBED_COLORS


class Achievement:
    """Represents a single achievement."""
    
    def __init__(self, achievement_id: str, name: str, description: str, 
                 emoji: str, category: str, rarity: str = "common", 
                 points: int = 10, hidden: bool = False):
        self.id = achievement_id
        self.name = name
        self.description = description
        self.emoji = emoji
        self.category = category
        self.rarity = rarity
        self.points = points
        self.hidden = hidden


class AchievementManager:
    """Manages player achievements and tracking."""
    
    def __init__(self, achievements_file: str, stats_file: str):
        self.achievements_file = achievements_file
        self.stats_file = stats_file
        self.achievements = self._initialize_achievements()
        self.player_achievements = self._load_player_achievements()
    
    def _initialize_achievements(self) -> Dict[str, Achievement]:
        """Initialize all available achievements."""
        achievements = {}
        
        # First Game Achievements
        achievements['first_game'] = Achievement(
            'first_game', 'First Blood', 'Play your first commander game',
            '🎮', 'milestone', 'common', 5
        )
        
        achievements['first_win'] = Achievement(
            'first_win', 'Victory Royale', 'Win your first commander game',
            '🏆', 'milestone', 'common', 15
        )
        
        # Game Count Achievements
        achievements['games_5'] = Achievement(
            'games_5', 'Getting Started', 'Play 5 commander games',
            '🎯', 'milestone', 'common', 25
        )
        
        achievements['games_10'] = Achievement(
            'games_10', 'Regular Player', 'Play 10 commander games',
            '🎲', 'milestone', 'common', 50
        )
        
        achievements['games_25'] = Achievement(
            'games_25', 'Dedicated Gamer', 'Play 25 commander games',
            '🎖️', 'milestone', 'uncommon', 100
        )
        
        achievements['games_50'] = Achievement(
            'games_50', 'Commander Veteran', 'Play 50 commander games',
            '⭐', 'milestone', 'rare', 200
        )
        
        achievements['games_100'] = Achievement(
            'games_100', 'Century Club', 'Play 100 commander games',
            '💯', 'milestone', 'epic', 500
        )
        
        # Win Achievements
        achievements['wins_5'] = Achievement(
            'wins_5', 'Rising Star', 'Win 5 commander games',
            '🌟', 'performance', 'uncommon', 75
        )
        
        achievements['wins_10'] = Achievement(
            'wins_10', 'Champion', 'Win 10 commander games',
            '👑', 'performance', 'rare', 150
        )
        
        achievements['wins_25'] = Achievement(
            'wins_25', 'Commander Master', 'Win 25 commander games',
            '🔥', 'performance', 'epic', 400
        )
        
        # Streak Achievements
        achievements['win_streak_3'] = Achievement(
            'win_streak_3', 'Hot Streak', 'Win 3 games in a row',
            '🔥', 'performance', 'uncommon', 100
        )
        
        achievements['win_streak_5'] = Achievement(
            'win_streak_5', 'Unstoppable', 'Win 5 games in a row',
            '⚡', 'performance', 'rare', 250
        )
        
        achievements['podium_streak_5'] = Achievement(
            'podium_streak_5', 'Consistent Player', 'Finish top 3 five times in a row',
            '🎯', 'performance', 'rare', 200
        )
        
        # Color Achievements
        achievements['mono_white'] = Achievement(
            'mono_white', 'Law and Order', 'Win with a mono-white commander',
            '⚪', 'color', 'common', 30
        )
        
        achievements['mono_blue'] = Achievement(
            'mono_blue', 'Master of Mind', 'Win with a mono-blue commander',
            '🔵', 'color', 'common', 30
        )
        
        achievements['mono_black'] = Achievement(
            'mono_black', 'Dark Arts', 'Win with a mono-black commander',
            '⚫', 'color', 'common', 30
        )
        
        achievements['mono_red'] = Achievement(
            'mono_red', 'Chaos Theory', 'Win with a mono-red commander',
            '🔴', 'color', 'common', 30
        )
        
        achievements['mono_green'] = Achievement(
            'mono_green', 'Nature\'s Fury', 'Win with a mono-green commander',
            '🟢', 'color', 'common', 30
        )
        
        achievements['all_mono_colors'] = Achievement(
            'all_mono_colors', 'Rainbow Warrior', 'Win with all five mono-colored commanders',
            '🌈', 'color', 'epic', 300
        )
        
        achievements['five_color'] = Achievement(
            'five_color', 'WUBRG Master', 'Win with a five-color commander',
            '🎨', 'color', 'rare', 150
        )
        
        achievements['colorless'] = Achievement(
            'colorless', 'Eldrazi Overlord', 'Win with a colorless commander',
            '◆', 'color', 'rare', 125
        )
        
        # Special Achievements
        achievements['different_commanders_10'] = Achievement(
            'different_commanders_10', 'Versatile Player', 'Play 10 different commanders',
            '🎭', 'variety', 'uncommon', 100
        )
        
        achievements['different_commanders_25'] = Achievement(
            'different_commanders_25', 'Commander Collector', 'Play 25 different commanders',
            '📚', 'variety', 'rare', 250
        )
        
        achievements['comeback_king'] = Achievement(
            'comeback_king', 'Comeback King', 'Win a game after being in last place',
            '🎪', 'special', 'rare', 200, hidden=True
        )
        
        achievements['speed_demon'] = Achievement(
            'speed_demon', 'Speed Demon', 'Play 5 games in one day',
            '💨', 'special', 'uncommon', 150
        )
        
        achievements['night_owl'] = Achievement(
            'night_owl', 'Night Owl', 'Play a game between midnight and 6 AM',
            '🦉', 'special', 'uncommon', 75
        )
        
        achievements['early_bird'] = Achievement(
            'early_bird', 'Early Bird', 'Play a game between 6 AM and 9 AM',
            '🐦', 'special', 'uncommon', 75
        )
        
        # Social Achievements
        achievements['play_with_5_different'] = Achievement(
            'play_with_5_different', 'Social Butterfly', 'Play with 5 different players',
            '🦋', 'social', 'uncommon', 100
        )
        
        achievements['play_with_10_different'] = Achievement(
            'play_with_10_different', 'Community Leader', 'Play with 10 different players',
            '🤝', 'social', 'rare', 200
        )
        
        # Performance Achievements
        achievements['high_winrate'] = Achievement(
            'high_winrate', 'Dominant Force', 'Maintain a 50%+ win rate over 20+ games',
            '💪', 'performance', 'epic', 400
        )
        
        achievements['improvement'] = Achievement(
            'improvement', 'Getting Better', 'Improve average placement by 1.5+ over 10 games',
            '📈', 'performance', 'rare', 150
        )
        
        # Additional Win Achievements
        achievements['wins_50'] = Achievement(
            'wins_50', 'Commander Legend', 'Win 50 commander games',
            '👑', 'performance', 'epic', 750
        )
        
        achievements['wins_100'] = Achievement(
            'wins_100', 'Planeswalker', 'Win 100 commander games',
            '⚡', 'performance', 'legendary', 1500
        )
        
        # Extended Streak Achievements
        achievements['win_streak_10'] = Achievement(
            'win_streak_10', 'Legendary Streak', 'Win 10 games in a row',
            '🌟', 'performance', 'epic', 500
        )
        
        achievements['podium_streak_10'] = Achievement(
            'podium_streak_10', 'Podium Master', 'Finish top 3 ten times in a row',
            '🎖️', 'performance', 'epic', 400
        )
        
        achievements['win_streak_2'] = Achievement(
            'win_streak_2', 'Double Victory', 'Win 2 games in a row',
            '🔥', 'performance', 'common', 50
        )
        
        # Color Combination Achievements
        achievements['guild_colors'] = Achievement(
            'guild_colors', 'Guild Master', 'Win with commanders from all 10 two-color combinations',
            '🏛️', 'color', 'legendary', 1000
        )
        
        achievements['azorius_win'] = Achievement(
            'azorius_win', 'Senate Control', 'Win with a White-Blue commander',
            '⚖️', 'color', 'common', 25
        )
        
        achievements['dimir_win'] = Achievement(
            'dimir_win', 'House Secrets', 'Win with a Blue-Black commander',
            '🕵️', 'color', 'common', 25
        )
        
        achievements['rakdos_win'] = Achievement(
            'rakdos_win', 'Carnival of Chaos', 'Win with a Black-Red commander',
            '🎭', 'color', 'common', 25
        )
        
        achievements['gruul_win'] = Achievement(
            'gruul_win', 'Wild Rampage', 'Win with a Red-Green commander',
            '🐗', 'color', 'common', 25
        )
        
        achievements['selesnya_win'] = Achievement(
            'selesnya_win', 'Conclave Unity', 'Win with a Green-White commander',
            '🌱', 'color', 'common', 25
        )
        
        achievements['orzhov_win'] = Achievement(
            'orzhov_win', 'Syndicate Power', 'Win with a White-Black commander',
            '⛪', 'color', 'common', 25
        )
        
        achievements['izzet_win'] = Achievement(
            'izzet_win', 'Mad Science', 'Win with a Blue-Red commander',
            '🧪', 'color', 'common', 25
        )
        
        achievements['golgari_win'] = Achievement(
            'golgari_win', 'Life and Death', 'Win with a Black-Green commander',
            '🌿', 'color', 'common', 25
        )
        
        achievements['boros_win'] = Achievement(
            'boros_win', 'Legion March', 'Win with a Red-White commander',
            '⚔️', 'color', 'common', 25
        )
        
        achievements['simic_win'] = Achievement(
            'simic_win', 'Evolution Chamber', 'Win with a Green-Blue commander',
            '🧬', 'color', 'common', 25
        )
        
        # Three-Color Achievements
        achievements['shard_master'] = Achievement(
            'shard_master', 'Shard Master', 'Win with commanders from all 5 three-color shards',
            '💎', 'color', 'epic', 600
        )
        
        achievements['wedge_master'] = Achievement(
            'wedge_master', 'Wedge Master', 'Win with commanders from all 5 three-color wedges',
            '🔮', 'color', 'epic', 600
        )
        
        # Placement Achievements
        achievements['runner_up'] = Achievement(
            'runner_up', 'Silver Medal', 'Finish in 2nd place 5 times',
            '🥈', 'performance', 'common', 40
        )
        
        achievements['bronze_medal'] = Achievement(
            'bronze_medal', 'Bronze Medal', 'Finish in 3rd place 5 times',
            '🥉', 'performance', 'common', 30
        )
        
        achievements['fourth_place'] = Achievement(
            'fourth_place', 'Almost There', 'Finish in 4th place 5 times',
            '4️⃣', 'performance', 'common', 20
        )
        
        achievements['last_place'] = Achievement(
            'last_place', 'Learning Experience', 'Finish in last place 5 times',
            '📚', 'performance', 'common', 15
        )
        
        achievements['podium_finisher'] = Achievement(
            'podium_finisher', 'Podium Regular', 'Finish in top 3 a total of 25 times',
            '🏆', 'performance', 'rare', 200
        )
        
        # Special Circumstance Achievements
        achievements['comeback_victory'] = Achievement(
            'comeback_victory', 'Phoenix Rising', 'Win after finishing last in your previous game',
            '🔥', 'special', 'rare', 175, hidden=True
        )
        
        achievements['perfect_week'] = Achievement(
            'perfect_week', 'Perfect Week', 'Win every game played in a 7-day period (minimum 3 games)',
            '💯', 'special', 'epic', 300
        )
        
        achievements['tournament_winner'] = Achievement(
            'tournament_winner', 'Tournament Champion', 'Win 3 games in a single day',
            '🏆', 'special', 'rare', 200
        )
        
        achievements['marathon_player'] = Achievement(
            'marathon_player', 'Marathon Player', 'Play 10 games in one day',
            '🏃', 'special', 'epic', 400
        )
        
        achievements['weekend_warrior'] = Achievement(
            'weekend_warrior', 'Weekend Warrior', 'Play games on Saturday and Sunday',
            '⚡', 'special', 'uncommon', 100
        )
        
        achievements['consistency'] = Achievement(
            'consistency', 'Mr. Consistent', 'Play at least one game every day for 7 days',
            '📅', 'special', 'rare', 250
        )
        
        # Commander-Specific Achievements
        achievements['loyalty'] = Achievement(
            'loyalty', 'Commander Loyalty', 'Play the same commander 10 times',
            '💝', 'variety', 'uncommon', 125
        )
        
        achievements['devotion'] = Achievement(
            'devotion', 'True Devotion', 'Play the same commander 25 times',
            '❤️', 'variety', 'rare', 300
        )
        
        achievements['specialist'] = Achievement(
            'specialist', 'Specialist', 'Win 10 games with the same commander',
            '🎯', 'variety', 'rare', 250
        )
        
        achievements['master'] = Achievement(
            'master', 'Commander Master', 'Win 20 games with the same commander',
            '👑', 'variety', 'epic', 500
        )
        
        # Social & Community Achievements
        achievements['mentor'] = Achievement(
            'mentor', 'Mentor', 'Play with a new player (someone with <5 total games)',
            '👨‍🏫', 'social', 'uncommon', 150
        )
        
        achievements['ambassador'] = Achievement(
            'ambassador', 'Community Ambassador', 'Play with 25 different players',
            '🌍', 'social', 'epic', 400
        )
        
        achievements['frequent_player'] = Achievement(
            'frequent_player', 'Regular at the Table', 'Play with the same player 10 times',
            '🤝', 'social', 'uncommon', 100
        )
        
        achievements['table_variety'] = Achievement(
            'table_variety', 'Table Variety', 'Play in games of every size (3, 4, 5, 6+ players)',
            '🎲', 'social', 'rare', 200
        )
        
        # Game Length & Timing Achievements
        achievements['quick_games'] = Achievement(
            'quick_games', 'Speed Runner', 'Finish 5 games in under 2 hours',
            '💨', 'special', 'uncommon', 125, hidden=True
        )
        
        achievements['late_night'] = Achievement(
            'late_night', 'Night Shift', 'Play a game after 10 PM',
            '🌙', 'special', 'common', 50
        )
        
        achievements['early_morning'] = Achievement(
            'early_morning', 'Dawn Patrol', 'Play a game before 8 AM',
            '🌅', 'special', 'uncommon', 75
        )
        
        achievements['lunch_break'] = Achievement(
            'lunch_break', 'Lunch Break', 'Play a game between 11 AM and 2 PM',
            '🍽️', 'special', 'common', 50
        )
        
        # Win Rate & Performance Achievements
        achievements['perfectionist'] = Achievement(
            'perfectionist', 'Perfectionist', 'Maintain a 75%+ win rate over 12+ games',
            '💎', 'performance', 'legendary', 1000
        )
        
        achievements['solid_player'] = Achievement(
            'solid_player', 'Solid Player', 'Maintain a 33%+ win rate over 15+ games',
            '🗿', 'performance', 'uncommon', 125
        )
        
        achievements['comeback_artist'] = Achievement(
            'comeback_artist', 'Comeback Artist', 'Win 3 games after being in last place',
            '🎪', 'performance', 'rare', 225, hidden=True
        )
        
        # Milestone & Anniversary Achievements
        achievements['birthday'] = Achievement(
            'birthday', 'Birthday Winner', 'Win a game on your birthday',
            '🎂', 'special', 'rare', 200, hidden=True
        )
        
        achievements['new_year'] = Achievement(
            'new_year', 'New Year Champion', 'Win your first game of the year',
            '🎊', 'special', 'uncommon', 150
        )
        
        achievements['monthly_winner'] = Achievement(
            'monthly_winner', 'Monthly Champion', 'Win at least 5 games in a single month',
            '📅', 'performance', 'uncommon', 150
        )
        
        # Meta & Strategy Achievements
        achievements['meta_breaker'] = Achievement(
            'meta_breaker', 'Meta Breaker', 'Win with a commander that has <10% server win rate',
            '🔨', 'strategy', 'rare', 300, hidden=True
        )
        
        achievements['trend_setter'] = Achievement(
            'trend_setter', 'Trend Setter', 'Be the first to win with a new commander on the server',
            '🌟', 'strategy', 'epic', 400, hidden=True
        )
        
        achievements['underdog'] = Achievement(
            'underdog', 'Underdog Victory', 'Win in a 6+ player game',
            '🐕', 'strategy', 'uncommon', 125
        )
        
        achievements['giant_killer'] = Achievement(
            'giant_killer', 'Giant Killer', 'Win against a player with 50+ total wins',
            '⚔️', 'strategy', 'rare', 200, hidden=True
        )
        
        # Collection & Variety Achievements
        achievements['color_collector'] = Achievement(
            'color_collector', 'Color Collector', 'Play commanders of every color combination',
            '🎨', 'variety', 'legendary', 800
        )
        
        achievements['tribal_master'] = Achievement(
            'tribal_master', 'Tribal Master', 'Win with 5 different tribal commanders',
            '🏺', 'variety', 'rare', 275
        )
        
        achievements['artifact_lover'] = Achievement(
            'artifact_lover', 'Artifact Enthusiast', 'Win with 3 different artifact-based commanders',
            '⚙️', 'variety', 'uncommon', 150
        )
        
        # Fun & Flavor Achievements
        achievements['lucky_seven'] = Achievement(
            'lucky_seven', 'Lucky Seven', 'Win exactly 7 games',
            '🍀', 'milestone', 'common', 77
        )
        
        achievements['unlucky'] = Achievement(
            'unlucky', 'Thirteen Club', 'Play exactly 13 games without winning',
            '🖤', 'milestone', 'uncommon', 130, hidden=True
        )
        
        achievements['round_numbers'] = Achievement(
            'round_numbers', 'Round Numbers', 'Reach exactly 10, 25, 50, or 100 total games',
            '🔢', 'milestone', 'common', 25
        )
        
        achievements['hat_trick'] = Achievement(
            'hat_trick', 'Hat Trick', 'Win 3 games in a single day',
            '🎩', 'performance', 'uncommon', 150
        )
        
        achievements['grand_slam'] = Achievement(
            'grand_slam', 'Grand Slam', 'Finish 1st, 2nd, 3rd, and 4th in separate games',
            '⚾', 'performance', 'rare', 200
        )
        
        # Archetype & Strategy Achievements
        achievements['aggro_master'] = Achievement(
            'aggro_master', 'Aggro Master', 'Win 5 games with Aggro archetype',
            '⚡', 'strategy', 'uncommon', 125
        )
        
        achievements['control_master'] = Achievement(
            'control_master', 'Control Master', 'Win 5 games with Control archetype',
            '🛡️', 'strategy', 'uncommon', 125
        )
        
        achievements['combo_master'] = Achievement(
            'combo_master', 'Combo Master', 'Win 5 games with Combo archetype',
            '🔄', 'strategy', 'uncommon', 125
        )
        
        achievements['midrange_master'] = Achievement(
            'midrange_master', 'Midrange Master', 'Win 5 games with Midrange archetype',
            '⚖️', 'strategy', 'uncommon', 125
        )
        
        achievements['tokens_master'] = Achievement(
            'tokens_master', 'Token Army', 'Win 3 games with Tokens archetype',
            '👥', 'strategy', 'common', 75
        )
        
        achievements['voltron_master'] = Achievement(
            'voltron_master', 'Voltron Pilot', 'Win 3 games with Voltron archetype',
            '🤖', 'strategy', 'uncommon', 100
        )
        
        achievements['reanimator_master'] = Achievement(
            'reanimator_master', 'Death and Taxes', 'Win 3 games with Reanimator archetype',
            '☠️', 'strategy', 'uncommon', 100
        )
        
        achievements['aristocrats_master'] = Achievement(
            'aristocrats_master', 'Noble Sacrifice', 'Win 3 games with Aristocrats archetype',
            '🎩', 'strategy', 'uncommon', 100
        )
        
        achievements['archetype_explorer'] = Achievement(
            'archetype_explorer', 'Archetype Explorer', 'Win with 5 different archetypes',
            '🗺️', 'variety', 'rare', 200
        )
        
        achievements['archetype_master'] = Achievement(
            'archetype_master', 'Master Strategist', 'Win with 10 different archetypes',
            '🎓', 'variety', 'epic', 400
        )
        
        achievements['archetype_specialist'] = Achievement(
            'archetype_specialist', 'Specialist', 'Win 10 games with the same archetype',
            '🏅', 'strategy', 'rare', 250
        )
        
        achievements['archetype_purist'] = Achievement(
            'archetype_purist', 'Purist', 'Play 25 games with the same archetype',
            '💎', 'strategy', 'epic', 350
        )
        
        return achievements
    
    def _load_player_achievements(self) -> Dict[int, Dict]:
        """Load player achievements from file."""
        if not os.path.exists(self.achievements_file):
            return {}
        
        try:
            with open(self.achievements_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert string keys back to int
                return {int(user_id): achievements for user_id, achievements in data.items()}
        except Exception:
            return {}
    
    def _save_player_achievements(self):
        """Save player achievements to file."""
        try:
            # Convert int keys to string for JSON
            data = {str(user_id): achievements for user_id, achievements in self.player_achievements.items()}
            
            with open(self.achievements_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving achievements: {e}")
    
    def check_achievements(self, user_id: int) -> List[Achievement]:
        """Check and award new achievements for a player."""
        if user_id not in self.player_achievements:
            self.player_achievements[user_id] = {
                'earned': {},
                'progress': {},
                'total_points': 0,
                'last_updated': datetime.now().isoformat()
            }
        
        player_data = self.player_achievements[user_id]
        new_achievements = []
        
        # Get player stats
        stats = self._get_player_stats(user_id)
        if not stats:
            return new_achievements
        
        # Check each achievement
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in player_data['earned']:
                continue  # Already earned
            
            if self._check_achievement_condition(achievement_id, user_id, stats):
                # Award achievement
                player_data['earned'][achievement_id] = {
                    'date': datetime.now().isoformat(),
                    'points': achievement.points
                }
                player_data['total_points'] += achievement.points
                new_achievements.append(achievement)
        
        player_data['last_updated'] = datetime.now().isoformat()
        self._save_player_achievements()
        
        return new_achievements
    
    def _check_achievement_condition(self, achievement_id: str, user_id: int, stats: Dict) -> bool:
        """Check if a specific achievement condition is met."""
        try:
            # Milestone achievements
            if achievement_id == 'first_game':
                return stats['total_games'] >= 1
            elif achievement_id == 'first_win':
                return stats['total_wins'] >= 1
            elif achievement_id == 'games_5':
                return stats['total_games'] >= 5
            elif achievement_id == 'games_10':
                return stats['total_games'] >= 10
            elif achievement_id == 'games_25':
                return stats['total_games'] >= 25
            elif achievement_id == 'games_50':
                return stats['total_games'] >= 50
            elif achievement_id == 'games_100':
                return stats['total_games'] >= 100
            
            # Win achievements
            elif achievement_id == 'wins_5':
                return stats['total_wins'] >= 5
            elif achievement_id == 'wins_10':
                return stats['total_wins'] >= 10
            elif achievement_id == 'wins_25':
                return stats['total_wins'] >= 25
            
            # Streak achievements
            elif achievement_id == 'win_streak_3':
                return self._check_win_streak(user_id, 3)
            elif achievement_id == 'win_streak_5':
                return self._check_win_streak(user_id, 5)
            elif achievement_id == 'podium_streak_5':
                return self._check_podium_streak(user_id, 5)
            
            # Color achievements
            elif achievement_id.startswith('mono_'):
                color = achievement_id.split('_')[1]
                return self._check_mono_color_win(user_id, color)
            elif achievement_id == 'all_mono_colors':
                return self._check_all_mono_colors(user_id)
            elif achievement_id == 'five_color':
                return self._check_five_color_win(user_id)
            elif achievement_id == 'colorless':
                return self._check_colorless_win(user_id)
            
            # Variety achievements
            elif achievement_id == 'different_commanders_10':
                return len(stats.get('commanders_played', set())) >= 10
            elif achievement_id == 'different_commanders_25':
                return len(stats.get('commanders_played', set())) >= 25
            
            # Special achievements
            elif achievement_id == 'speed_demon':
                return self._check_games_in_day(user_id, 5)
            elif achievement_id == 'night_owl':
                return self._check_time_range_game(user_id, 0, 6)
            elif achievement_id == 'early_bird':
                return self._check_time_range_game(user_id, 6, 9)
            
            # Social achievements
            elif achievement_id == 'play_with_5_different':
                return len(stats.get('players_played_with', set())) >= 5
            elif achievement_id == 'play_with_10_different':
                return len(stats.get('players_played_with', set())) >= 10
            
            # Performance achievements
            elif achievement_id == 'high_winrate':
                if stats['total_games'] >= 20:
                    return (stats['total_wins'] / stats['total_games']) >= 0.5
            elif achievement_id == 'improvement':
                return self._check_improvement_trend(user_id)
            
            # Additional win achievements
            elif achievement_id == 'wins_50':
                return stats['total_wins'] >= 50
            elif achievement_id == 'wins_100':
                return stats['total_wins'] >= 100
            
            # Extended streak achievements
            elif achievement_id == 'win_streak_2':
                return self._check_win_streak(user_id, 2)
            elif achievement_id == 'win_streak_10':
                return self._check_win_streak(user_id, 10)
            elif achievement_id == 'podium_streak_10':
                return self._check_podium_streak(user_id, 10)
            
            # Two-color guild achievements
            elif achievement_id.endswith('_win') and achievement_id in [
                'azorius_win', 'dimir_win', 'rakdos_win', 'gruul_win', 'selesnya_win',
                'orzhov_win', 'izzet_win', 'golgari_win', 'boros_win', 'simic_win'
            ]:
                guild_colors = {
                    'azorius_win': ['W', 'U'],
                    'dimir_win': ['U', 'B'],
                    'rakdos_win': ['B', 'R'],
                    'gruul_win': ['R', 'G'],
                    'selesnya_win': ['G', 'W'],
                    'orzhov_win': ['W', 'B'],
                    'izzet_win': ['U', 'R'],
                    'golgari_win': ['B', 'G'],
                    'boros_win': ['R', 'W'],
                    'simic_win': ['G', 'U']
                }
                return self._check_color_combination_win(user_id, guild_colors[achievement_id])
            
            # Guild and color combination mastery
            elif achievement_id == 'guild_colors':
                return self._check_all_guild_wins(user_id)
            elif achievement_id == 'shard_master':
                return self._check_shard_master(user_id)
            elif achievement_id == 'wedge_master':
                return self._check_wedge_master(user_id)
            
            # Placement achievements
            elif achievement_id == 'runner_up':
                return self._check_placement_count(user_id, 2, 5)
            elif achievement_id == 'bronze_medal':
                return self._check_placement_count(user_id, 3, 5)
            elif achievement_id == 'fourth_place':
                return self._check_placement_count(user_id, 4, 5)
            elif achievement_id == 'last_place':
                return self._check_last_place_count(user_id, 5)
            elif achievement_id == 'podium_finisher':
                return self._check_podium_total(user_id, 25)
            
            # Commander loyalty achievements
            elif achievement_id == 'loyalty':
                return self._check_commander_games(user_id, 10)
            elif achievement_id == 'devotion':
                return self._check_commander_games(user_id, 25)
            elif achievement_id == 'specialist':
                return self._check_commander_wins(user_id, 10)
            elif achievement_id == 'master':
                return self._check_commander_wins(user_id, 20)
            
            # Extended social achievements
            elif achievement_id == 'mentor':
                return self._check_mentor_achievement(user_id)
            elif achievement_id == 'ambassador':
                return len(stats.get('players_played_with', set())) >= 25
            elif achievement_id == 'frequent_player':
                return self._check_frequent_player(user_id)
            elif achievement_id == 'table_variety':
                return self._check_table_variety(user_id)
            
            # Special timing achievements
            elif achievement_id == 'weekend_warrior':
                return self._check_weekend_games(user_id)
            elif achievement_id == 'late_night':
                return self._check_time_range_game(user_id, 22, 24)
            elif achievement_id == 'early_morning':
                return self._check_time_range_game(user_id, 5, 8)
            elif achievement_id == 'lunch_break':
                return self._check_time_range_game(user_id, 11, 14)
            
            # Performance and win rate achievements
            elif achievement_id == 'perfectionist':
                if stats['total_games'] >= 12:
                    return (stats['total_wins'] / stats['total_games']) >= 0.75
            elif achievement_id == 'solid_player':
                if stats['total_games'] >= 15:
                    return (stats['total_wins'] / stats['total_games']) >= 0.33
            
            # Special circumstance achievements
            elif achievement_id == 'comeback_victory':
                return self._check_comeback_victory(user_id)
            elif achievement_id == 'comeback_artist':
                return self._check_comeback_artist(user_id)
            elif achievement_id == 'perfect_week':
                return self._check_perfect_week(user_id)
            elif achievement_id == 'tournament_winner':
                return self._check_games_in_day(user_id, 3) and self._check_wins_in_day(user_id, 3)
            elif achievement_id == 'marathon_player':
                return self._check_games_in_day(user_id, 10)
            elif achievement_id == 'hat_trick':
                return self._check_wins_in_day(user_id, 3)
            elif achievement_id == 'consistency':
                return self._check_daily_consistency(user_id)
            
            # Milestone achievements
            elif achievement_id == 'lucky_seven':
                return stats['total_wins'] == 7
            elif achievement_id == 'monthly_winner':
                return self._check_monthly_wins(user_id, 5)
            elif achievement_id == 'round_numbers':
                return stats['total_games'] in [10, 25, 50, 100]
            elif achievement_id == 'grand_slam':
                return self._check_grand_slam(user_id)
            elif achievement_id == 'underdog':
                return self._check_large_game_win(user_id, 6)
            
            # Strategy and meta achievements
            elif achievement_id == 'meta_breaker':
                return self._check_meta_breaker(user_id)
            elif achievement_id == 'trend_setter':
                return self._check_trend_setter(user_id)
            elif achievement_id == 'giant_killer':
                return self._check_giant_killer(user_id)
            
            # Collection variety achievements
            elif achievement_id == 'color_collector':
                return self._check_color_collector(user_id)
            elif achievement_id == 'tribal_master':
                return self._check_tribal_master(user_id)
            elif achievement_id == 'artifact_lover':
                return self._check_artifact_lover(user_id)
            
            # Archetype achievements
            elif achievement_id == 'aggro_master':
                return self._check_archetype_wins(user_id, 'Aggro', 5)
            elif achievement_id == 'control_master':
                return self._check_archetype_wins(user_id, 'Control', 5)
            elif achievement_id == 'combo_master':
                return self._check_archetype_wins(user_id, 'Combo', 5)
            elif achievement_id == 'midrange_master':
                return self._check_archetype_wins(user_id, 'Midrange', 5)
            elif achievement_id == 'tokens_master':
                return self._check_archetype_wins(user_id, 'Tokens', 3)
            elif achievement_id == 'voltron_master':
                return self._check_archetype_wins(user_id, 'Voltron', 3)
            elif achievement_id == 'reanimator_master':
                return self._check_archetype_wins(user_id, 'Reanimator', 3)
            elif achievement_id == 'aristocrats_master':
                return self._check_archetype_wins(user_id, 'Aristocrats', 3)
            elif achievement_id == 'archetype_explorer':
                return self._check_different_archetype_wins(user_id, 5)
            elif achievement_id == 'archetype_master':
                return self._check_different_archetype_wins(user_id, 10)
            elif achievement_id == 'archetype_specialist':
                return self._check_same_archetype_wins(user_id, 10)
            elif achievement_id == 'archetype_purist':
                return self._check_same_archetype_games(user_id, 25)
            
            return False
            
        except Exception as e:
            print(f"Error checking achievement {achievement_id}: {e}")
            return False
    
    def _get_player_stats(self, user_id: int) -> Dict:
        """Get comprehensive player statistics."""
        if not os.path.exists(self.stats_file):
            return {}
        
        stats = {
            'total_games': 0,
            'total_wins': 0,
            'commanders_played': set(),
            'players_played_with': set(),
            'archetypes_played': set(),
            'archetype_wins': defaultdict(int),
            'recent_games': []
        }
        
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        stats['total_games'] += 1
                        if int(row['placement']) == 1:
                            stats['total_wins'] += 1
                            # Track archetype wins with normalization
                            archetype = row.get('commander_archetype', 'Unknown')
                            if archetype and archetype != 'Unknown':
                                normalized_archetype = self._normalize_archetype(archetype)
                                stats['archetype_wins'][normalized_archetype] += 1
                        
                        stats['commanders_played'].add(row['commander'])
                        
                        # Track archetypes played with normalization
                        archetype = row.get('commander_archetype', 'Unknown')
                        if archetype and archetype != 'Unknown':
                            normalized_archetype = self._normalize_archetype(archetype)
                            stats['archetypes_played'].add(normalized_archetype)
                        
                        stats['recent_games'].append(row)
                    
                    # Find players played with - group by game_date to identify same games
                    if int(row['user_id']) != user_id:
                        # Check if this player was in same game (same game_date and player count)
                        for user_game in stats['recent_games']:
                            if (user_game['game_date'] == row['game_date'] and
                                user_game['total_players'] == row['total_players']):
                                stats['players_played_with'].add(int(row['user_id']))
                                break
        
        except Exception as e:
            print(f"Error getting player stats: {e}")
            return {}
        
        return stats
    
    def _check_win_streak(self, user_id: int, required_streak: int) -> bool:
        """Check if player has a win streak of required length."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games = []
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        games.append({
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S'),
                            'placement': int(row['placement'])
                        })
            
            games.sort(key=lambda x: x['date'], reverse=True)
            
            current_streak = 0
            for game in games:
                if game['placement'] == 1:
                    current_streak += 1
                    if current_streak >= required_streak:
                        return True
                else:
                    break
            
            return False
            
        except Exception:
            return False
    
    def _check_podium_streak(self, user_id: int, required_streak: int) -> bool:
        """Check if player has a podium streak of required length."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games = []
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        games.append({
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S'),
                            'placement': int(row['placement'])
                        })
            
            games.sort(key=lambda x: x['date'], reverse=True)
            
            current_streak = 0
            for game in games:
                if game['placement'] <= 3:
                    current_streak += 1
                    if current_streak >= required_streak:
                        return True
                else:
                    break
            
            return False
            
        except Exception:
            return False
    
    def _check_mono_color_win(self, user_id: int, color: str) -> bool:
        """Check if player has won with a mono-colored commander."""
        try:
            color_map = {
                'white': 'W',
                'blue': 'U', 
                'black': 'B',
                'red': 'R',
                'green': 'G'
            }
            
            target_color = color_map.get(color, color.upper())
            
            if not os.path.exists(self.stats_file):
                return False
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1 and 
                        row['commander_colors'] == target_color):
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_all_mono_colors(self, user_id: int) -> bool:
        """Check if player has won with all five mono-colored commanders."""
        colors = ['W', 'U', 'B', 'R', 'G']
        for color in colors:
            if not self._check_mono_color_win(user_id, color):
                return False
        return True
    
    def _check_five_color_win(self, user_id: int) -> bool:
        """Check if player has won with a five-color commander."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        colors = row['commander_colors'].split(',')
                        if len(colors) == 5 and set(colors) == {'W', 'U', 'B', 'R', 'G'}:
                            return True
            
            return False
            
        except Exception:
            return False
    
    def _check_colorless_win(self, user_id: int) -> bool:
        """Check if player has won with a colorless commander."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1 and 
                        row['commander_colors'] in ['C', '']):
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_games_in_day(self, user_id: int, required_games: int) -> bool:
        """Check if player has played required number of games in one day."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games_by_date = defaultdict(int)
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        game_date = datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S').date()
                        games_by_date[game_date] += 1
            
            return max(games_by_date.values(), default=0) >= required_games
            
        except Exception:
            return False
    
    def _check_time_range_game(self, user_id: int, start_hour: int, end_hour: int) -> bool:
        """Check if player has played a game in specified time range."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        game_time = datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S')
                        hour = game_time.hour
                        if start_hour <= hour < end_hour:
                            return True
            
            return False
            
        except Exception:
            return False
    
    def _check_improvement_trend(self, user_id: int) -> bool:
        """Check if player has improved their average placement."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games = []
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        games.append({
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S'),
                            'placement': int(row['placement'])
                        })
            
            if len(games) < 20:  # Need at least 20 games
                return False
            
            games.sort(key=lambda x: x['date'])
            
            # Compare first 10 vs last 10 games
            first_10 = [g['placement'] for g in games[:10]]
            last_10 = [g['placement'] for g in games[-10:]]
            
            first_avg = sum(first_10) / len(first_10)
            last_avg = sum(last_10) / len(last_10)
            
            improvement = first_avg - last_avg
            return improvement >= 1.5
            
        except Exception:
            return False
    
    def _check_color_combination_win(self, user_id: int, target_colors: List[str]) -> bool:
        """Check if player has won with a specific color combination."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        colors = row['commander_colors'].split(',')
                        if set(colors) == set(target_colors):
                            return True
            
            return False
            
        except Exception:
            return False
    
    def _check_all_guild_wins(self, user_id: int) -> bool:
        """Check if player has won with all 10 two-color guild combinations."""
        guild_combinations = [
            ['W', 'U'], ['U', 'B'], ['B', 'R'], ['R', 'G'], ['G', 'W'],  # Allied
            ['W', 'B'], ['U', 'R'], ['B', 'G'], ['R', 'W'], ['G', 'U']   # Enemy
        ]
        
        for colors in guild_combinations:
            if not self._check_color_combination_win(user_id, colors):
                return False
        return True
    
    def _check_placement_count(self, user_id: int, placement: int, required_count: int) -> bool:
        """Check if player has achieved a specific placement a certain number of times."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            count = 0
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == placement):
                        count += 1
                        if count >= required_count:
                            return True
            
            return False
            
        except Exception:
            return False
    
    def _check_last_place_count(self, user_id: int, required_count: int) -> bool:
        """Check if player has finished last place a certain number of times."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            count = 0
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                games_by_key = defaultdict(list)
                
                # Group by game using date, time, and player count as composite key
                for row in reader:
                    game_key = f"{row['game_date']}_{row['total_players']}"
                    games_by_key[game_key].append(row)
                
                for game_key, players in games_by_key.items():
                    max_placement = max(int(p['placement']) for p in players)
                    
                    for player in players:
                        if (int(player['user_id']) == user_id and 
                            int(player['placement']) == max_placement):
                            count += 1
                            if count >= required_count:
                                return True
            
            return False
            
        except Exception:
            return False
    
    def _check_podium_total(self, user_id: int, required_count: int) -> bool:
        """Check if player has finished in top 3 a total number of times."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            count = 0
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) <= 3):
                        count += 1
                        if count >= required_count:
                            return True
            
            return False
            
        except Exception:
            return False
    
    def _check_commander_games(self, user_id: int, required_games: int) -> bool:
        """Check if player has played the same commander a certain number of times."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            commander_counts = Counter()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        commander_counts[row['commander']] += 1
            
            return max(commander_counts.values(), default=0) >= required_games
            
        except Exception:
            return False
    
    def _check_commander_wins(self, user_id: int, required_wins: int) -> bool:
        """Check if player has won with the same commander a certain number of times."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            commander_wins = Counter()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        commander_wins[row['commander']] += 1
            
            return max(commander_wins.values(), default=0) >= required_wins
            
        except Exception:
            return False
    
    def _check_weekend_games(self, user_id: int) -> bool:
        """Check if player has played on both Saturday and Sunday."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            weekend_days = set()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        game_date = datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S')
                        if game_date.weekday() in [5, 6]:  # Saturday=5, Sunday=6
                            weekend_days.add(game_date.weekday())
            
            return len(weekend_days) >= 2
            
        except Exception:
            return False
    
    def _check_wins_in_day(self, user_id: int, required_wins: int) -> bool:
        """Check if player has won a certain number of games in one day."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            wins_by_date = defaultdict(int)
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        game_date = datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S').date()
                        wins_by_date[game_date] += 1
            
            return max(wins_by_date.values(), default=0) >= required_wins
            
        except Exception:
            return False
    
    def _check_grand_slam(self, user_id: int) -> bool:
        """Check if player has finished 1st, 2nd, 3rd, and 4th in separate games."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            placements_achieved = set()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        placements_achieved.add(int(row['placement']))
            
            return {1, 2, 3, 4}.issubset(placements_achieved)
            
        except Exception:
            return False
    
    def _check_large_game_win(self, user_id: int, min_players: int) -> bool:
        """Check if player has won in a game with minimum number of players."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1 and 
                        int(row['total_players']) >= min_players):
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_comeback_victory(self, user_id: int) -> bool:
        """Check if player won after finishing last in previous game."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games = []
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        games.append({
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S'),
                            'placement': int(row['placement']),
                            'total_players': int(row['total_players'])
                        })
            
            games.sort(key=lambda x: x['date'])
            
            for i in range(1, len(games)):
                prev_game = games[i-1]
                curr_game = games[i]
                
                # Check if won after being last
                if (curr_game['placement'] == 1 and 
                    prev_game['placement'] == prev_game['total_players']):
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _check_comeback_artist(self, user_id: int) -> bool:
        """Check if player has won 3+ games after being in last place."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games = []
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        games.append({
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S'),
                            'placement': int(row['placement']),
                            'total_players': int(row['total_players'])
                        })
            
            games.sort(key=lambda x: x['date'])
            comeback_wins = 0
            
            for i in range(1, len(games)):
                prev_game = games[i-1]
                curr_game = games[i]
                
                if (curr_game['placement'] == 1 and 
                    prev_game['placement'] == prev_game['total_players']):
                    comeback_wins += 1
                    if comeback_wins >= 3:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_perfect_week(self, user_id: int) -> bool:
        """Check if player won every game in a 7-day period (min 3 games)."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            games = []
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        games.append({
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S'),
                            'placement': int(row['placement'])
                        })
            
            games.sort(key=lambda x: x['date'])
            
            for i in range(len(games)):
                week_start = games[i]['date']
                week_end = week_start + timedelta(days=7)
                
                week_games = [g for g in games 
                             if week_start <= g['date'] < week_end]
                
                if len(week_games) >= 3:
                    all_wins = all(g['placement'] == 1 for g in week_games)
                    if all_wins:
                        return True
            
            return False
            
        except Exception:
            return False
    
    # Simplified implementations for complex achievements
    def _check_mentor_achievement(self, user_id: int) -> bool:
        """Check if player has played with someone who has <5 total games."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # First, calculate total games for all players
            player_game_counts = defaultdict(int)
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    player_game_counts[int(row['user_id'])] += 1
            
            # Then check games where this player participated
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Group games by game_id
                games_data = defaultdict(list)
                for row in reader:
                    games_data[f"{row['game_date']}_{row['total_players']}"].append(row)
                
                # Check each game where this player participated
                for game_id, players in games_data.items():
                    user_in_game = False
                    new_player_in_game = False
                    
                    for player_data in players:
                        player_id = int(player_data['user_id'])
                        
                        if player_id == user_id:
                            user_in_game = True
                        elif player_game_counts[player_id] < 5:
                            new_player_in_game = True
                    
                    if user_in_game and new_player_in_game:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_frequent_player(self, user_id: int) -> bool:
        """Check if player has played with the same person 10+ times."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # Track co-players
            co_player_counts = defaultdict(int)
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Group games by game_id
                games_data = defaultdict(list)
                for row in reader:
                    games_data[f"{row['game_date']}_{row['total_players']}"].append(row)
                
                # For each game, find co-players
                for game_id, players in games_data.items():
                    user_in_game = False
                    other_players = []
                    
                    for player_data in players:
                        player_id = int(player_data['user_id'])
                        
                        if player_id == user_id:
                            user_in_game = True
                        else:
                            other_players.append(player_id)
                    
                    # If user was in this game, count all other players
                    if user_in_game:
                        for other_player in other_players:
                            co_player_counts[other_player] += 1
            
            # Check if played with any player 10+ times
            return max(co_player_counts.values(), default=0) >= 10
            
        except Exception:
            return False
    
    def _check_table_variety(self, user_id: int) -> bool:
        """Check if player has played in games of various sizes."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            game_sizes = set()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        game_sizes.add(int(row['total_players']))
            
            # Check for 3, 4, 5, and 6+ player games
            required_sizes = {3, 4, 5}
            has_large_game = any(size >= 6 for size in game_sizes)
            
            return required_sizes.issubset(game_sizes) and has_large_game
            
        except Exception:
            return False
    
    def _check_daily_consistency(self, user_id: int) -> bool:
        """Check if player played at least one game every day for 7 days."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            game_dates = set()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        game_date = datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S').date()
                        game_dates.add(game_date)
            
            # Check for any 7-day consecutive period
            sorted_dates = sorted(game_dates)
            
            for i in range(len(sorted_dates)):
                consecutive_days = 1
                current_date = sorted_dates[i]
                
                for j in range(i + 1, len(sorted_dates)):
                    next_date = sorted_dates[j]
                    if next_date == current_date + timedelta(days=1):
                        consecutive_days += 1
                        current_date = next_date
                        if consecutive_days >= 7:
                            return True
                    else:
                        break
            
            return False
            
        except Exception:
            return False
    
    def _check_monthly_wins(self, user_id: int, required_wins: int) -> bool:
        """Check if player has won a certain number of games in a single month."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            wins_by_month = defaultdict(int)
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        game_date = datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S')
                        month_key = (game_date.year, game_date.month)
                        wins_by_month[month_key] += 1
            
            return max(wins_by_month.values(), default=0) >= required_wins
            
        except Exception:
            return False
    
    # Simplified placeholders for complex achievements
    def _check_shard_master(self, user_id: int) -> bool:
        """Check if player has won with all 5 three-color shards."""
        try:
            # Shard combinations (allied three-color)
            shards = [
                ['G', 'W', 'U'],  # Bant
                ['W', 'U', 'B'],  # Esper
                ['U', 'B', 'R'],  # Grixis
                ['B', 'R', 'G'],  # Jund
                ['R', 'G', 'W']   # Naya
            ]
            
            for shard in shards:
                if not self._check_color_combination_win(user_id, shard):
                    return False
            return True
            
        except Exception:
            return False
    
    def _check_wedge_master(self, user_id: int) -> bool:
        """Check if player has won with all 5 three-color wedges."""
        try:
            # Wedge combinations (enemy three-color)
            wedges = [
                ['W', 'B', 'G'],  # Abzan
                ['U', 'R', 'W'],  # Jeskai
                ['B', 'G', 'U'],  # Sultai
                ['R', 'W', 'B'],  # Mardu
                ['G', 'U', 'R']   # Temur
            ]
            
            for wedge in wedges:
                if not self._check_color_combination_win(user_id, wedge):
                    return False
            return True
            
        except Exception:
            return False
    
    def _check_meta_breaker(self, user_id: int) -> bool:
        """Check if player won with a low-win-rate commander."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # Calculate commander win rates across all players
            commander_stats = defaultdict(lambda: {'wins': 0, 'games': 0})
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    commander = row['commander']
                    commander_stats[commander]['games'] += 1
                    if int(row['placement']) == 1:
                        commander_stats[commander]['wins'] += 1
            
            # Check if this player won with a commander that has <10% win rate
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        commander = row['commander']
                        stats = commander_stats[commander]
                        
                        if stats['games'] >= 10:  # Only consider commanders played enough
                            win_rate = stats['wins'] / stats['games']
                            if win_rate < 0.10:  # Less than 10% win rate
                                return True
            
            return False
            
        except Exception:
            return False
    
    def _check_trend_setter(self, user_id: int) -> bool:
        """Check if player was first to win with a commander on server."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # Find first win for each commander
            first_wins = {}
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                wins = []
                
                for row in reader:
                    if int(row['placement']) == 1:
                        wins.append({
                            'commander': row['commander'],
                            'user_id': int(row['user_id']),
                            'date': datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S')
                        })
                
                # Sort by date to find first wins
                wins.sort(key=lambda x: x['date'])
                
                for win in wins:
                    commander = win['commander']
                    if commander not in first_wins:
                        first_wins[commander] = win['user_id']
            
            # Check if this player was first to win with any commander
            for commander, first_player in first_wins.items():
                if first_player == user_id:
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _check_giant_killer(self, user_id: int) -> bool:
        """Check if player beat someone with 50+ wins."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # First, calculate total wins for all players
            player_wins = defaultdict(int)
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['placement']) == 1:
                        player_wins[int(row['user_id'])] += 1
            
            # Then check games where this player won
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Group games by game_id
                games_data = defaultdict(list)
                for row in reader:
                    games_data[f"{row['game_date']}_{row['total_players']}"].append(row)
                
                # Check each game where this player won
                for game_id, players in games_data.items():
                    user_won = False
                    opponents_with_50_wins = False
                    
                    for player_data in players:
                        player_id = int(player_data['user_id'])
                        placement = int(player_data['placement'])
                        
                        if player_id == user_id and placement == 1:
                            user_won = True
                        elif player_id != user_id and player_wins[player_id] >= 50:
                            opponents_with_50_wins = True
                    
                    if user_won and opponents_with_50_wins:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _check_color_collector(self, user_id: int) -> bool:
        """Check if player has played every possible color combination."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            color_combinations = set()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        colors = row['commander_colors']
                        if colors:  # Make sure not empty
                            # Normalize color combination (sort and join)
                            color_list = sorted(colors.split(','))
                            color_combinations.add(tuple(color_list))
            
            # Expected combinations: 5 mono + 10 guilds + 10 three-color + 5 four-color + 1 five-color + colorless
            # That's 32 total combinations, but let's be realistic and require at least 20
            return len(color_combinations) >= 20
            
        except Exception:
            return False
    
    def _check_tribal_master(self, user_id: int) -> bool:
        """Check if player won with tribal commanders."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # Common tribal keywords to look for in commander names
            tribal_keywords = [
                'elf', 'elves', 'goblin', 'goblins', 'zombie', 'zombies',
                'dragon', 'dragons', 'angel', 'angels', 'demon', 'demons',
                'vampire', 'vampires', 'werewolf', 'werewolves', 'human', 'humans',
                'soldier', 'soldiers', 'warrior', 'warriors', 'wizard', 'wizards',
                'beast', 'beasts', 'cat', 'cats', 'bird', 'birds',
                'tribal', 'chieftain', 'lord', 'king', 'queen'
            ]
            
            tribal_commanders = set()
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        commander_name = row['commander'].lower()
                        
                        # Check if commander name contains tribal keywords
                        for keyword in tribal_keywords:
                            if keyword in commander_name:
                                tribal_commanders.add(row['commander'])
                                break
            
            return len(tribal_commanders) >= 5
            
        except Exception:
            return False
    
    def _check_artifact_lover(self, user_id: int) -> bool:
        """Check if player won with artifact commanders."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # Common artifact-related keywords
            artifact_keywords = [
                'artifact', 'artifacts', 'construct', 'constructs',
                'golem', 'golems', 'thopter', 'thopters',
                'myr', 'servo', 'servos', 'automaton', 'automatons',
                'steel', 'metal', 'gear', 'clockwork',
                'workshop', 'forge', 'foundry', 'inventor'
            ]
            
            artifact_commanders = set()
            
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        commander_name = row['commander'].lower()
                        
                        # Check if commander name contains artifact keywords
                        for keyword in artifact_keywords:
                            if keyword in commander_name:
                                artifact_commanders.add(row['commander'])
                                break
            
            return len(artifact_commanders) >= 3
            
        except Exception:
            return False
    
    def get_player_achievements(self, user_id: int) -> Dict:
        """Get all achievements for a player."""
        if user_id not in self.player_achievements:
            return {
                'earned': {},
                'progress': {},
                'total_points': 0,
                'total_earned': 0
            }
        
        player_data = self.player_achievements[user_id].copy()
        player_data['total_earned'] = len(player_data['earned'])
        return player_data
    
    def get_achievement_leaderboard(self, limit: int = 10) -> List[Tuple[int, Dict]]:
        """Get achievement leaderboard by points."""
        leaderboard = []
        
        for user_id, data in self.player_achievements.items():
            leaderboard.append((user_id, {
                'total_points': data['total_points'],
                'total_achievements': len(data['earned'])
            }))
        
        leaderboard.sort(key=lambda x: x[1]['total_points'], reverse=True)
        return leaderboard[:limit]
    
    def find_achievement(self, search_term: str) -> Optional[Achievement]:
        """Find an achievement by ID or name (case-insensitive)."""
        search_lower = search_term.lower()
        
        # First try exact ID match
        if search_term in self.achievements:
            return self.achievements[search_term]
        
        # Try case-insensitive ID match
        for achievement_id, achievement in self.achievements.items():
            if achievement_id.lower() == search_lower:
                return achievement
        
        # Try name match (case-insensitive)
        for achievement in self.achievements.values():
            if achievement.name.lower() == search_lower:
                return achievement
        
        # Try partial name match
        for achievement in self.achievements.values():
            if search_lower in achievement.name.lower():
                return achievement
        
        return None
    
    def get_all_achievements_by_category(self) -> Dict[str, List[Achievement]]:
        """Get all achievements grouped by category."""
        categories = defaultdict(list)
        for achievement in self.achievements.values():
            categories[achievement.category].append(achievement)
        
        # Sort achievements within each category by rarity then points
        rarity_order = {'common': 1, 'uncommon': 2, 'rare': 3, 'epic': 4, 'legendary': 5}
        for category in categories:
            categories[category].sort(key=lambda x: (rarity_order.get(x.rarity, 0), x.points))
        
        return dict(categories)
    
    def _normalize_archetype(self, archetype: str) -> str:
        """Normalize archetype names for consistent comparison."""
        if not archetype:
            return ""
        
        archetype_lower = archetype.lower()
        # Treat 'Elves' the same as 'Tribal'
        if archetype_lower == 'elves':
            return 'Tribal'
        
        # Return the original archetype with proper capitalization
        return archetype.title()
    
    def _check_archetype_wins(self, user_id: int, archetype: str, required_wins: int) -> bool:
        """Check if player has won required number of games with specific archetype."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            # Normalize archetype names (treat Elves the same as Tribal)
            normalized_archetype = self._normalize_archetype(archetype)
            
            wins_count = 0
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        # Normalize the stored archetype for comparison
                        stored_archetype = self._normalize_archetype(row.get('archetype', ''))
                        if stored_archetype == normalized_archetype:
                            wins_count += 1
                            if wins_count >= required_wins:
                                return True
            
            return False
            
        except Exception:
            return False
    
    def _check_different_archetype_wins(self, user_id: int, required_different: int) -> bool:
        """Check if player has won with different archetypes."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            archetypes_won = set()
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        archetype = row.get('archetype')
                        if archetype and archetype != 'Unknown':
                            # Normalize archetype names for consistent counting
                            normalized_archetype = self._normalize_archetype(archetype)
                            archetypes_won.add(normalized_archetype)
            
            return len(archetypes_won) >= required_different
            
        except Exception:
            return False
    
    def _check_same_archetype_wins(self, user_id: int, required_wins: int) -> bool:
        """Check if player has won required number of games with the same archetype."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            archetype_wins = defaultdict(int)
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if (int(row['user_id']) == user_id and 
                        int(row['placement']) == 1):
                        archetype = row.get('archetype')
                        if archetype and archetype != 'Unknown':
                            # Normalize archetype names for consistent counting
                            normalized_archetype = self._normalize_archetype(archetype)
                            archetype_wins[normalized_archetype] += 1
            
            return max(archetype_wins.values(), default=0) >= required_wins
            
        except Exception:
            return False
    
    def _check_same_archetype_games(self, user_id: int, required_games: int) -> bool:
        """Check if player has played required number of games with the same archetype."""
        try:
            if not os.path.exists(self.stats_file):
                return False
            
            archetype_games = defaultdict(int)
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['user_id']) == user_id:
                        archetype = row.get('archetype')
                        if archetype and archetype != 'Unknown':
                            archetype_games[archetype] += 1
            
            return max(archetype_games.values(), default=0) >= required_games
            
        except Exception:
            return False


def create_achievement_detail_embed(achievement: Achievement, user_has_earned: bool = False, 
                                  earned_date: str = None, earned_by_count: int = 0, 
                                  total_players: int = 0) -> discord.Embed:
    """Create detailed embed for a specific achievement."""
    rarity_colors = {
        'common': 0x95a5a6,
        'uncommon': 0x2ecc71,
        'rare': 0x3498db,
        'epic': 0x9b59b6,
        'legendary': 0xf39c12
    }
    
    rarity_emojis = {
        'common': '⚪',
        'uncommon': '🟢', 
        'rare': '🔵',
        'epic': '🟣',
        'legendary': '🟠'
    }
    
    status_emoji = "✅" if user_has_earned else "🔒"
    title = f"{status_emoji} {achievement.emoji} {achievement.name}"
    
    embed = discord.Embed(
        title=title,
        description=achievement.description,
        color=rarity_colors.get(achievement.rarity, 0x95a5a6)
    )
    
    # Basic info section
    embed.add_field(
        name="📋 Basic Info",
        value=(
            f"**ID:** `{achievement.id}`\n"
            f"**Category:** {achievement.category.title()}\n"
            f"**Rarity:** {rarity_emojis.get(achievement.rarity, '⚪')} {achievement.rarity.title()}\n"
            f"**Points:** 🏆 {achievement.points}\n"
            f"**Hidden:** {'Yes' if achievement.hidden else 'No'}"
        ),
        inline=True
    )
    
    # Progress/Status section
    if user_has_earned and earned_date:
        try:
            earned_dt = datetime.fromisoformat(earned_date.replace('Z', '+00:00'))
            date_str = earned_dt.strftime("%B %d, %Y")
        except:
            date_str = "Unknown"
        
        embed.add_field(
            name="🎯 Your Progress",
            value=f"**Status:** Earned ✅\n**Date Earned:** {date_str}",
            inline=True
        )
    else:
        embed.add_field(
            name="🎯 Your Progress",
            value="**Status:** Not Earned 🔒\n**Date Earned:** N/A",
            inline=True
        )
    
    # Statistics section
    if total_players > 0:
        percentage = (earned_by_count / total_players) * 100
        rarity_desc = "Very Common" if percentage >= 75 else \
                     "Common" if percentage >= 50 else \
                     "Uncommon" if percentage >= 25 else \
                     "Rare" if percentage >= 10 else "Very Rare"
        
        embed.add_field(
            name="📊 Server Statistics",
            value=(
                f"**Earned by:** {earned_by_count}/{total_players} players\n"
                f"**Completion Rate:** {percentage:.1f}%\n"
                f"**Actual Rarity:** {rarity_desc}"
            ),
            inline=False
        )
    
    return embed


def create_achievement_embed(achievement: Achievement, is_new: bool = False) -> discord.Embed:
    """Create embed for displaying an achievement."""
    title = f"🎉 Achievement Unlocked!" if is_new else f"{achievement.emoji} {achievement.name}"
    
    rarity_colors = {
        'common': 0x95a5a6,
        'uncommon': 0x2ecc71,
        'rare': 0x3498db,
        'epic': 0x9b59b6,
        'legendary': 0xf39c12
    }
    
    embed = discord.Embed(
        title=title,
        color=rarity_colors.get(achievement.rarity, 0x95a5a6)
    )
    
    embed.add_field(
        name=f"{achievement.emoji} {achievement.name}",
        value=achievement.description,
        inline=False
    )
    
    embed.add_field(
        name="💎 Rarity",
        value=achievement.rarity.title(),
        inline=True
    )
    
    embed.add_field(
        name="🏆 Points",
        value=f"{achievement.points} pts",
        inline=True
    )
    
    embed.add_field(
        name="📂 Category",
        value=achievement.category.title(),
        inline=True
    )
    
    return embed


def create_achievements_overview_embed(user_id: int, username: str, player_data: Dict, 
                                     total_achievements: int) -> discord.Embed:
    """Create overview embed for player achievements."""
    embed = discord.Embed(
        title=f"🏆 {username}'s Achievements",
        color=EMBED_COLORS.get('achievements', 0xf39c12),
        description=f"Achievement progress and statistics"
    )
    
    progress_percentage = (player_data['total_earned'] / total_achievements) * 100
    
    embed.add_field(
        name="📊 Progress",
        value=(
            f"**Unlocked:** {player_data['total_earned']}/{total_achievements} "
            f"({progress_percentage:.1f}%)\n"
            f"**Total Points:** {player_data['total_points']}"
        ),
        inline=False
    )
    
    # Group achievements by category
    categories = defaultdict(list)
    for achievement_id in player_data['earned']:
        achievement = achievement_manager.achievements.get(achievement_id)
        if achievement:
            categories[achievement.category].append(achievement)
    
    for category, achievements in categories.items():
        if achievements:
            achievement_text = ""
            for achievement in sorted(achievements, key=lambda x: x.points, reverse=True):
                achievement_text += f"{achievement.emoji} {achievement.name}\n"
            
            embed.add_field(
                name=f"📂 {category.title()} ({len(achievements)})",
                value=achievement_text,
                inline=True
            )
    
    embed.set_footer(text="🎯 Keep playing to unlock more achievements!")
    
    return embed


# Initialize global achievement manager
achievement_manager = AchievementManager('player_achievements.json', 'commander_stats.csv')
