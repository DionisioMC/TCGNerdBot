"""
Commander game tracking module for the TCG Nerd Bot.
Handles commander game sessions, player tracking, and statistics.
"""

import csv
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import discord
from config import EMBED_COLORS, COLOR_EMOJIS
from scryfall_api import ScryfallAPI
from edhrec_api import edhrec_api, get_archetype_emoji


class CommanderGame:
    """Class to represent a commander game session."""

    def __init__(self, game_id: str, creator_id: int, channel_id: int):
        self.game_id = game_id
        self.creator_id = creator_id
        self.channel_id = channel_id
        self.players: Dict[int, Dict] = {}  # user_id -> player_data
        self.start_time = datetime.now()
        self.is_active = True
        self.is_finished = False
        self.results_submitted = False

    def add_player(self, user_id: int, username: str) -> bool:
        """Add a player to the game."""
        if user_id not in self.players and len(self.players) < 8:  # Max 8 players
            self.players[user_id] = {
                'username': username,
                'commander': None,
                'commander_colors': [],
                'commander_archetype': None,
                'placement': None,
                'joined_at': datetime.now()
            }
            return True
        return False

    def remove_player(self, user_id: int) -> bool:
        """Remove a player from the game."""
        if user_id in self.players:
            del self.players[user_id]
            return True
        return False

    def set_commander(self, user_id: int, commander_name: str) -> bool:
        """Set a player's commander."""
        if user_id in self.players:
            self.players[user_id]['commander'] = commander_name
            # Note: Color and archetype fetching will be handled by the manager class
            return True
        return False
    
    def set_commander_archetype(self, user_id: int, archetype: str) -> bool:
        """Set a player's commander archetype."""
        if user_id in self.players:
            self.players[user_id]['commander_archetype'] = archetype
            return True
        return False

    def set_placement(self, user_id: int, placement: int) -> bool:
        """Set a player's final placement."""
        if user_id in self.players and 1 <= placement <= len(self.players):
            self.players[user_id]['placement'] = placement
            return True
        return False

    def can_finish_game(self) -> bool:
        """Check if the game can be finished (all players have commanders and placements)."""
        if len(self.players) < 2:
            return False

        for player_data in self.players.values():
            if not player_data['commander'] or player_data['placement'] is None:
                return False

        # Check if placements are unique and complete
        placements = [p['placement'] for p in self.players.values()]
        return len(set(placements)) == len(placements) and set(placements) == set(range(1, len(self.players) + 1))

    def finish_game(self) -> bool:
        """Finish the game and mark it as completed."""
        if self.can_finish_game():
            self.is_finished = True
            self.is_active = False
            return True
        return False


class CommanderGameManager:
    """Manager class for handling commander games."""

    def __init__(self):
        self.active_games: Dict[str, CommanderGame] = {}
        self.games_file = 'commander_games_data.json'
        self.stats_file = 'commander_stats.csv'
        self.load_games()

    def create_game(self, creator_id: int, channel_id: int, username: str) -> Tuple[bool, str, Optional[CommanderGame]]:
        """Create a new commander game."""
        # Check if user already has an active game in this channel
        for game in self.active_games.values():
            if game.creator_id == creator_id and game.channel_id == channel_id and game.is_active:
                return False, "You already have an active game in this channel!", None

        # Generate simple unique game ID (e.g., "A1", "B2", "C3")
        import string
        import random
        
        # Create a short, memorable game ID
        letter = random.choice(string.ascii_uppercase)
        number = len(self.active_games) + 1
        game_id = f"{letter}{number}"
        
        # Ensure uniqueness (very unlikely collision but safety first)
        while game_id in self.active_games:
            letter = random.choice(string.ascii_uppercase)
            number = random.randint(1, 99)
            game_id = f"{letter}{number}"

        game = CommanderGame(game_id, creator_id, channel_id)
        game.add_player(creator_id, username)

        self.active_games[game_id] = game
        self.save_games()

        return True, f"Commander game **{game_id}** created! You've been automatically added as a player.", game

    def join_game(self, game_id: str, user_id: int, username: str) -> Tuple[bool, str]:
        """Join an existing game."""
        if game_id not in self.active_games:
            return False, "Game not found!"

        game = self.active_games[game_id]

        if not game.is_active:
            return False, "This game is no longer active!"

        if user_id in game.players:
            return False, "You're already in this game!"

        if game.add_player(user_id, username):
            self.save_games()
            return True, f"Successfully joined game **{game_id}**!"
        else:
            return False, "Game is full (max 8 players) or another error occurred!"

    def leave_game(self, game_id: str, user_id: int) -> Tuple[bool, str]:
        """Leave a game."""
        if game_id not in self.active_games:
            return False, "Game not found!"

        game = self.active_games[game_id]

        if user_id not in game.players:
            return False, "You're not in this game!"

        # If creator leaves, transfer ownership to another player or end game
        if game.creator_id == user_id:
            if len(game.players) > 1:
                # Transfer to another player
                other_players = [
                    pid for pid in game.players.keys() if pid != user_id]
                game.creator_id = other_players[0]
                game.remove_player(user_id)
                self.save_games()
                return True, f"Left the game. Ownership transferred to <@{game.creator_id}>."
            else:
                # End the game if creator is the only player
                game.is_active = False
                self.save_games()
                return True, "Game ended as you were the only player."
        else:
            game.remove_player(user_id)
            self.save_games()
            return True, "Successfully left the game!"

    def leave_game_by_user(self, user_id: int) -> Tuple[bool, str, Optional[CommanderGame]]:
        """Leave a game without needing game_id (finds user's active game)."""
        # Find user's active game
        game = self.get_user_unfinished_game(user_id)

        if not game:
            return False, "You're not in any active commander games!", None

        if user_id not in game.players:
            return False, "You're not in this game!", None

        game_id = game.game_id

        # If creator leaves, transfer ownership to another player or end game
        if game.creator_id == user_id:
            if len(game.players) > 1:
                # Transfer to another player
                other_players = [
                    pid for pid in game.players.keys() if pid != user_id]
                game.creator_id = other_players[0]
                game.remove_player(user_id)
                self.save_games()
                return True, f"Left the game. Ownership transferred to <@{game.creator_id}>.", game
            else:
                # End the game if creator is the only player
                game.is_active = False
                self.save_games()
                return True, "Game ended as you were the only player.", game
        else:
            game.remove_player(user_id)
            self.save_games()
            return True, "Successfully left the game!", game

    async def set_commander(self, game_id: str, user_id: int, commander_name: str) -> Tuple[bool, str, Optional[Dict]]:
        """Set a player's commander and return archetype selection data."""
        if game_id not in self.active_games:
            return False, "Game not found!", None

        game = self.active_games[game_id]

        if not game.is_active:
            return False, "This game is no longer active!", None

        if user_id not in game.players:
            return False, "You're not in this game!", None

        # Fetch commander color information from Scryfall API
        try:
            card_data = await ScryfallAPI.get_card_by_name(commander_name)
            colors = []
            if card_data:
                # Get color identity (better for commanders than regular colors)
                color_identity = card_data.get('color_identity', [])
                colors = color_identity if color_identity else ['C']  # 'C' for colorless
            else:
                # If card not found, default to unknown
                colors = ['?']

            game.players[user_id]['commander_colors'] = colors
        except Exception as e:
            print(f"Error fetching commander colors: {e}")
            # Set colors as unknown if API call fails
            game.players[user_id]['commander_colors'] = ['?']

        # Fetch archetype information from EDHREC
        archetype_data = None
        try:
            archetype_data = edhrec_api.get_commander_archetypes(commander_name)
            if archetype_data and archetype_data.get('most_popular'):
                # Set the most popular archetype as default
                game.players[user_id]['commander_archetype'] = archetype_data['most_popular']
        except Exception as e:
            print(f"Error fetching archetype data: {e}")

        if game.set_commander(user_id, commander_name):
            self.save_games()

            # Create a color display string
            color_display = self._format_colors_display(
                game.players[user_id]['commander_colors'])
            
            success_msg = f"Commander set to **{commander_name}** {color_display}!"
            
            # Add archetype info if available
            if archetype_data and archetype_data.get('most_popular'):
                archetype = archetype_data['most_popular']
                emoji = get_archetype_emoji(archetype)
                success_msg += f"\nArchetype: {emoji} **{archetype}**"
            
            return True, success_msg, archetype_data
        else:
            return False, "Failed to set commander!", None

    async def set_commander_by_user(self, user_id: int, commander_name: str) -> Tuple[bool, str, Optional[CommanderGame], Optional[Dict]]:
        """Set a player's commander without needing game_id (finds user's active game)."""
        # Find user's active game
        game = self.get_user_unfinished_game(user_id)

        if not game:
            return False, "You're not in any active commander games!", None, None

        if not game.is_active:
            return False, "Your game is no longer active!", None, None

        if user_id not in game.players:
            return False, "You're not in this game!", None, None

        # Fetch commander color information from Scryfall API
        try:
            card_data = await ScryfallAPI.get_card_by_name(commander_name)
            colors = []
            if card_data:
                # Get color identity (better for commanders than regular colors)
                color_identity = card_data.get('color_identity', [])
                colors = color_identity if color_identity else ['C']  # 'C' for colorless
            else:
                # If card not found, default to unknown
                colors = ['?']

            game.players[user_id]['commander_colors'] = colors
        except Exception as e:
            print(f"Error fetching commander colors: {e}")
            # Set colors as unknown if API call fails
            game.players[user_id]['commander_colors'] = ['?']

        # Fetch archetype information from EDHREC
        archetype_data = None
        try:
            archetype_data = edhrec_api.get_commander_archetypes(commander_name)
            if archetype_data and archetype_data.get('most_popular'):
                # Set the most popular archetype as default
                game.players[user_id]['commander_archetype'] = archetype_data['most_popular']
        except Exception as e:
            print(f"Error fetching archetype data: {e}")

        if game.set_commander(user_id, commander_name):
            self.save_games()

            # Create a color display string
            color_display = self._format_colors_display(
                game.players[user_id]['commander_colors'])
            
            success_msg = f"Commander set to **{commander_name}** {color_display}!"
            
            # Add archetype info if available
            if archetype_data and archetype_data.get('most_popular'):
                archetype = archetype_data['most_popular']
                emoji = get_archetype_emoji(archetype)
                success_msg += f"\nArchetype: {emoji} **{archetype}**"
            
            return True, success_msg, game, archetype_data
        else:
            return False, "Failed to set commander!", None, None

    def set_commander_archetype_by_user(self, user_id: int, archetype: str) -> Tuple[bool, str, Optional[CommanderGame]]:
        """Set a player's commander archetype without needing game_id."""
        # Find user's active game
        game = self.get_user_unfinished_game(user_id)

        if not game:
            return False, "You're not in any active commander games!", None

        if not game.is_active:
            return False, "Your game is no longer active!", None

        if user_id not in game.players:
            return False, "You're not in this game!", None

        if not game.players[user_id]['commander']:
            return False, "You need to set a commander first!", None

        if game.set_commander_archetype(user_id, archetype):
            self.save_games()
            
            commander = game.players[user_id]['commander']
            emoji = get_archetype_emoji(archetype)
            return True, f"Archetype for **{commander}** changed to {emoji} **{archetype}**!", game
        else:
            return False, "Failed to set archetype!", None

    def _format_colors_display(self, colors: List[str]) -> str:
        """Format color list for display with emojis."""
        if not colors or colors == ['?']:
            return "❓"
        elif colors == ['C']:
            return COLOR_EMOJIS.get('colorless', '⚪')
        else:
            # Map color letters to emojis
            color_map = {
                'W': COLOR_EMOJIS.get('white', '⚪'),
                'U': COLOR_EMOJIS.get('blue', '🔵'),
                'B': COLOR_EMOJIS.get('black', '⚫'),
                'R': COLOR_EMOJIS.get('red', '🔴'),
                'G': COLOR_EMOJIS.get('green', '🟢')
            }

            emojis = [color_map.get(color, '❓') for color in colors]
            return ''.join(emojis)

    def set_placement(self, game_id: str, user_id: int, placement: int) -> Tuple[bool, str]:
        """Set a player's placement."""
        if game_id not in self.active_games:
            return False, "Game not found!"

        game = self.active_games[game_id]

        if not game.is_active:
            return False, "This game is no longer active!"

        if user_id not in game.players:
            return False, "You're not in this game!"

        # Check if placement is already taken
        for pid, pdata in game.players.items():
            if pid != user_id and pdata['placement'] == placement:
                return False, f"Placement {placement} is already taken by {pdata['username']}!"

        if game.set_placement(user_id, placement):
            self.save_games()
            return True, f"Placement set to **{placement}**!"
        else:
            return False, "Invalid placement! Must be between 1 and number of players."

    def set_archetype(self, game_id: str, user_id: int, archetype: str) -> Tuple[bool, str]:
        """Set a player's commander archetype."""
        if game_id not in self.active_games:
            return False, "Game not found!"

        game = self.active_games[game_id]

        if not game.is_active:
            return False, "This game is no longer active!"

        if user_id not in game.players:
            return False, "You're not in this game!"

        if not game.players[user_id]['commander']:
            return False, "You need to set a commander first!"

        if game.set_commander_archetype(user_id, archetype):
            self.save_games()
            
            commander = game.players[user_id]['commander']
            emoji = get_archetype_emoji(archetype)
            return True, f"Archetype for **{commander}** set to {emoji} **{archetype}**!"
        else:
            return False, "Failed to set archetype!"

    def finish_game(self, game_id: str, user_id: int) -> Tuple[bool, str, Optional[CommanderGame]]:
        """Finish a game and save results."""
        if game_id not in self.active_games:
            return False, "Game not found!", None

        game = self.active_games[game_id]

        if user_id != game.creator_id:
            return False, "Only the game creator can finish the game!", None

        if not game.can_finish_game():
            missing_info = []
            for pid, pdata in game.players.items():
                if not pdata['commander']:
                    missing_info.append(
                        f"{pdata['username']} needs to set their commander")
                if pdata['placement'] is None:
                    missing_info.append(
                        f"{pdata['username']} needs to set their placement")

            return False, f"Cannot finish game. Missing information:\n" + "\n".join(missing_info), None

        if game.finish_game():
            self.save_game_results(game)
            self.save_games()
            return True, "Game finished and results saved!", game
        else:
            return False, "Failed to finish game!", None

    def get_game_info(self, game_id: str) -> Optional[CommanderGame]:
        """Get game information."""
        return self.active_games.get(game_id)

    def get_user_active_games(self, user_id: int) -> List[CommanderGame]:
        """Get all active games for a user."""
        return [game for game in self.active_games.values()
                if user_id in game.players and game.is_active]

    def get_user_unfinished_game(self, user_id: int) -> Optional[CommanderGame]:
        """Get the user's active unfinished game (for reaction-based placement)."""
        active_games = self.get_user_active_games(user_id)
        # Return the first active game where user is a player
        for game in active_games:
            if user_id in game.players:
                return game
        return None

    def get_channel_games(self, channel_id: int) -> List[CommanderGame]:
        """Get all active games in a specific channel."""
        return [
            game for game in self.active_games.values()
            if game.channel_id == channel_id and game.is_active
        ]

    def get_joinable_games_for_user(self, channel_id: int, user_id: int) -> List[CommanderGame]:
        """Get all games in a channel that a user can join (not already in)."""
        channel_games = self.get_channel_games(channel_id)
        return [
            game for game in channel_games
            # Max 8 players
            if user_id not in game.players and len(game.players) < 8
        ]

    def get_available_placements(self, game: CommanderGame) -> List[int]:
        """Get list of available placement numbers for a game."""
        total_players = len(game.players)
        taken_placements = set()

        for player_data in game.players.values():
            if player_data['placement'] is not None:
                taken_placements.add(player_data['placement'])

        available = []
        for i in range(1, total_players + 1):
            if i not in taken_placements:
                available.append(i)

        return available

    def set_placement_by_reaction(self, user_id: int, placement: int) -> Tuple[bool, str, Optional[CommanderGame]]:
        """Set a player's placement using reaction (no game_id needed)."""
        # Find user's active game
        game = self.get_user_unfinished_game(user_id)

        if not game:
            return False, "You're not in any active commander games!", None

        if not game.is_active:
            return False, "Your game is no longer active!", None

        if user_id not in game.players:
            return False, "You're not in this game!", None

        # Check if placement is available
        available_placements = self.get_available_placements(game)
        if placement not in available_placements:
            return False, f"Placement {placement} is not available!", None

        # Check if user already has a placement
        if game.players[user_id]['placement'] is not None:
            old_placement = game.players[user_id]['placement']
            game.players[user_id]['placement'] = placement
            self.save_games()
            return True, f"Placement changed from {old_placement} to {placement}!", game
        else:
            game.players[user_id]['placement'] = placement
            self.save_games()
            return True, f"Placement set to {placement}!", game

    def get_channel_active_games(self, channel_id: int) -> List[CommanderGame]:
        """Get all active games in a channel."""
        return [game for game in self.active_games.values()
                if game.channel_id == channel_id and game.is_active]

    def save_games(self):
        """Save active games to file."""
        try:
            games_data = {}
            for game_id, game in self.active_games.items():
                # Convert player data for JSON serialization
                players_data = {}
                for user_id, player_data in game.players.items():
                    players_data[user_id] = {
                        'username': player_data['username'],
                        'commander': player_data['commander'],
                        'commander_colors': player_data.get('commander_colors', []),
                        'commander_archetype': player_data.get('commander_archetype'),
                        'placement': player_data['placement'],
                        'joined_at': player_data['joined_at'].isoformat()
                    }

                games_data[game_id] = {
                    'game_id': game.game_id,
                    'creator_id': game.creator_id,
                    'channel_id': game.channel_id,
                    'players': players_data,
                    'start_time': game.start_time.isoformat(),
                    'is_active': game.is_active,
                    'is_finished': game.is_finished,
                    'results_submitted': game.results_submitted
                }

            with open(self.games_file, 'w') as f:
                json.dump(games_data, f, indent=2)
        except Exception as e:
            print(f"Error saving games: {e}")

    def load_games(self):
        """Load active games from file."""
        try:
            if os.path.exists(self.games_file):
                with open(self.games_file, 'r') as f:
                    games_data = json.load(f)

                for game_id, data in games_data.items():
                    if data.get('is_active', False):  # Only load active games
                        game = CommanderGame(
                            data['game_id'], data['creator_id'], data['channel_id'])

                        # Load players data
                        for user_id_str, player_data in data['players'].items():
                            user_id = int(user_id_str)
                            game.players[user_id] = {
                                'username': player_data['username'],
                                'commander': player_data['commander'],
                                'commander_colors': player_data.get('commander_colors', []),
                                'commander_archetype': player_data.get('commander_archetype'),
                                'placement': player_data['placement'],
                                'joined_at': datetime.fromisoformat(player_data['joined_at'])
                            }

                        game.start_time = datetime.fromisoformat(
                            data['start_time'])
                        game.is_active = data['is_active']
                        game.is_finished = data['is_finished']
                        game.results_submitted = data.get(
                            'results_submitted', False)
                        self.active_games[game_id] = game
        except Exception as e:
            print(f"Error loading games: {e}")

    def save_game_results(self, game: CommanderGame):
        """Save game results to CSV for statistics."""
        try:
            # Create CSV file if it doesn't exist
            file_exists = os.path.exists(self.stats_file)

            with open(self.stats_file, 'a', newline='', encoding='utf-8') as f:
                fieldnames = ['game_id', 'player_id', 'username', 'commander',
                              'commander_colors', 'commander_archetype', 'placement', 'game_date', 'total_players']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                game_date = game.start_time.strftime('%Y-%m-%d %H:%M:%S')
                total_players = len(game.players)

                for user_id, player_data in game.players.items():
                    # Convert colors list to comma-separated string
                    colors_str = ','.join(
                        player_data.get('commander_colors', ['?']))

                    writer.writerow({
                        'game_id': game.game_id,
                        'player_id': user_id,
                        'username': player_data['username'],
                        'commander': player_data['commander'],
                        'commander_colors': colors_str,
                        'commander_archetype': player_data.get('commander_archetype', 'Unknown'),
                        'placement': player_data['placement'],
                        'game_date': game_date,
                        'total_players': total_players
                    })

                # Check achievements for all players after saving results
                self._check_achievements_for_all_players(game)

        except Exception as e:
            print(f"Error saving game results: {e}")

    def _check_achievements_for_all_players(self, game: CommanderGame):
        """Check achievements for all players in the finished game."""
        try:
            # Import here to avoid circular imports
            from achievements import achievement_manager

            for user_id in game.players.keys():
                new_achievements = achievement_manager.check_achievements(
                    user_id)
                # Store new achievements for later notification
                # (You can extend this to send immediate notifications if needed)
                if new_achievements:
                    print(
                        f"Player {user_id} earned {len(new_achievements)} new achievements!")

        except ImportError:
            # Achievements module not available
            pass
        except Exception as e:
            print(f"Error checking achievements: {e}")

    def get_player_stats(self, user_id: int) -> Dict:
        """Get statistics for a specific player."""
        try:
            if not os.path.exists(self.stats_file):
                return {}

            stats = {
                'total_games': 0,
                'wins': 0,
                'top_2': 0,
                'top_3': 0,
                'commanders_played': set(),
                'favorite_commander': None,
                'win_rate': 0.0,
                'avg_placement': 0.0,
                'colors_played': set(),
                'color_combinations': {},
                'favorite_colors': None,
                'mono_color_games': 0,
                'multicolor_games': 0
            }

            placements = []
            commander_counts: Dict[str, int] = {}
            color_combo_counts: Dict[str, int] = {}

            with open(self.stats_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if int(row['player_id']) == user_id:
                        stats['total_games'] += 1
                        placement = int(row['placement'])
                        placements.append(placement)

                        if placement == 1:
                            stats['wins'] += 1
                        if placement <= 2:
                            stats['top_2'] += 1
                        if placement <= 3:
                            stats['top_3'] += 1

                        commander = row['commander']
                        stats['commanders_played'].add(commander)
                        commander_counts[commander] = commander_counts.get(
                            commander, 0) + 1

                        # Process color information
                        colors_str = row.get('commander_colors', '?')
                        if colors_str and colors_str != '?':
                            colors = colors_str.split(',')

                            # Track individual colors
                            for color in colors:
                                if color != '?':
                                    stats['colors_played'].add(color)

                            # Track color combinations
                            color_combo = ','.join(sorted(colors))
                            if color_combo not in stats['color_combinations']:
                                stats['color_combinations'][color_combo] = 0
                            stats['color_combinations'][color_combo] += 1
                            color_combo_counts[color_combo] = color_combo_counts.get(
                                color_combo, 0) + 1

                            # Count mono vs multicolor
                            if len(colors) == 1 and colors[0] != 'C':
                                stats['mono_color_games'] += 1
                            elif len(colors) > 1:
                                stats['multicolor_games'] += 1

            if stats['total_games'] > 0:
                stats['win_rate'] = stats['wins'] / stats['total_games'] * 100
                stats['avg_placement'] = sum(placements) / len(placements)

                # Find most played commander
                if commander_counts:
                    stats['favorite_commander'] = max(
                        commander_counts, key=commander_counts.get)

                # Find most played color combination
                if color_combo_counts:
                    stats['favorite_colors'] = max(
                        color_combo_counts, key=color_combo_counts.get)

            stats['commanders_played'] = list(stats['commanders_played'])
            stats['colors_played'] = list(stats['colors_played'])
            return stats

        except Exception as e:
            print(f"Error getting player stats: {e}")
            return {}


# Global manager instance
commander_manager = CommanderGameManager()


def create_game_info_embed(game: CommanderGame) -> discord.Embed:
    """Create an embed showing game information."""
    embed = discord.Embed(
        title=f"🎯 Commander Game: {game.game_id}",
        color=EMBED_COLORS.get('commander_game', 0x8B4513),
        description=f"Created by <@{game.creator_id}>"
    )

    # Helper function to format colors
    def format_colors(colors):
        if not colors or colors == ['?']:
            return "❓"
        elif colors == ['C']:
            return COLOR_EMOJIS.get('colorless', '⚪')
        else:
            color_map = {
                'W': COLOR_EMOJIS.get('white', '⚪'),
                'U': COLOR_EMOJIS.get('blue', '🔵'),
                'B': COLOR_EMOJIS.get('black', '⚫'),
                'R': COLOR_EMOJIS.get('red', '🔴'),
                'G': COLOR_EMOJIS.get('green', '🟢')
            }
            emojis = [color_map.get(color, '❓') for color in colors]
            return ''.join(emojis)

    # Players info
    players_text = ""
    for i, (user_id, player_data) in enumerate(game.players.items(), 1):
        commander = player_data['commander'] or "Not set"
        colors = player_data.get('commander_colors', [])
        color_display = format_colors(colors) if commander != "Not set" else ""
        
        # Add archetype info
        archetype = player_data.get('commander_archetype')
        archetype_display = ""
        if archetype and commander != "Not set":
            archetype_emoji = get_archetype_emoji(archetype)
            archetype_display = f" {archetype_emoji}{archetype}"

        placement = player_data['placement']
        placement_text = f"#{placement}" if placement else "Not set"

        players_text += f"**{i}.** <@{user_id}>\n"
        players_text += f"   └ Commander: {commander} {color_display}{archetype_display}\n"
        players_text += f"   └ Placement: {placement_text}\n\n"

    if players_text:
        embed.add_field(
            name=f"👥 Players ({len(game.players)}/8)",
            value=players_text,
            inline=False
        )

    # Game status
    status = "🟢 Active" if game.is_active else "🔴 Inactive"
    if game.is_finished:
        status = "✅ Finished"

    embed.add_field(
        name="📊 Status",
        value=status,
        inline=True
    )

    embed.add_field(
        name="🕐 Started",
        value=game.start_time.strftime("%Y-%m-%d %H:%M"),
        inline=True
    )

    # Can finish?
    if game.is_active and game.can_finish_game():
        embed.add_field(
            name="✅ Ready to Finish",
            value="All players have set commanders and placements!",
            inline=False
        )
    elif game.is_active:
        missing = []
        for pid, pdata in game.players.items():
            if not pdata['commander'] or pdata['placement'] is None:
                missing.append(pdata['username'])

        if missing:
            embed.add_field(
                name="⚠️ Missing Information",
                value=f"Players need to set commander/placement: {', '.join(missing)}",
                inline=False
            )

    return embed


def create_player_stats_embed(user_id: int, username: str, stats: Dict) -> discord.Embed:
    """Create an embed showing player statistics."""
    embed = discord.Embed(
        title=f"📊 Commander Stats for {username}",
        color=EMBED_COLORS.get('commander_stats', 0x8B4513),
        description="Your commander game statistics"
    )

    if stats.get('total_games', 0) == 0:
        embed.add_field(
            name="📝 No Games Played",
            value="You haven't played any commander games yet! Use `!commander create` to start a game.",
            inline=False
        )
        return embed

    # Basic stats
    embed.add_field(
        name="🎮 Games Played",
        value=str(stats['total_games']),
        inline=True
    )

    embed.add_field(
        name="🏆 Wins",
        value=f"{stats['wins']} ({stats['win_rate']:.1f}%)",
        inline=True
    )

    embed.add_field(
        name="📈 Average Placement",
        value=f"{stats['avg_placement']:.1f}",
        inline=True
    )

    embed.add_field(
        name="🥈 Top 2 Finishes",
        value=str(stats['top_2']),
        inline=True
    )

    embed.add_field(
        name="🥉 Top 3 Finishes",
        value=str(stats['top_3']),
        inline=True
    )

    embed.add_field(
        name="🎴 Commanders Played",
        value=str(len(stats['commanders_played'])),
        inline=True
    )

    if stats.get('favorite_commander'):
        embed.add_field(
            name="⭐ Most Played Commander",
            value=stats['favorite_commander'],
            inline=False
        )

    # Color statistics
    if stats.get('colors_played'):
        # Format colors with emojis
        color_map = {
            'W': COLOR_EMOJIS.get('white', '⚪'),
            'U': COLOR_EMOJIS.get('blue', '🔵'),
            'B': COLOR_EMOJIS.get('black', '⚫'),
            'R': COLOR_EMOJIS.get('red', '🔴'),
            'G': COLOR_EMOJIS.get('green', '🟢'),
            'C': COLOR_EMOJIS.get('colorless', '⚪')
        }

        colors_display = ''.join([color_map.get(color, '❓')
                                 for color in sorted(stats['colors_played'])])

        embed.add_field(
            name="🌈 Colors Played",
            value=f"{colors_display} ({len(stats['colors_played'])} colors)",
            inline=True
        )

        # Mono vs multicolor preference
        mono_games = stats.get('mono_color_games', 0)
        multi_games = stats.get('multicolor_games', 0)

        if mono_games > 0 or multi_games > 0:
            embed.add_field(
                name="🎨 Color Preference",
                value=f"Mono: {mono_games} | Multi: {multi_games}",
                inline=True
            )

    # Most played color combination
    if stats.get('favorite_colors'):
        fav_colors = stats['favorite_colors'].split(',')
        fav_display = ''.join([color_map.get(color, '❓')
                              for color in fav_colors])
        embed.add_field(
            name="🌟 Favorite Colors",
            value=f"{fav_display}",
            inline=True
        )

    return embed


def create_game_finished_embed(game: CommanderGame) -> discord.Embed:
    """Create an embed for a finished game."""
    embed = discord.Embed(
        title="🏁 Commander Game Finished!",
        color=EMBED_COLORS.get('success', 0x00ff00),
        description=f"Game **{game.game_id}** has been completed and results saved!"
    )

    # Helper function to format colors
    def format_colors(colors):
        if not colors or colors == ['?']:
            return ""
        elif colors == ['C']:
            return COLOR_EMOJIS.get('colorless', '⚪')
        else:
            color_map = {
                'W': COLOR_EMOJIS.get('white', '⚪'),
                'U': COLOR_EMOJIS.get('blue', '🔵'),
                'B': COLOR_EMOJIS.get('black', '⚫'),
                'R': COLOR_EMOJIS.get('red', '🔴'),
                'G': COLOR_EMOJIS.get('green', '🟢')
            }
            emojis = [color_map.get(color, '❓') for color in colors]
            return ''.join(emojis)

    # Sort players by placement
    sorted_players = sorted(game.players.items(),
                            key=lambda x: x[1]['placement'])

    results_text = ""
    place_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

    for user_id, player_data in sorted_players:
        placement = player_data['placement']
        emoji = place_emojis[placement -
                             1] if placement <= len(place_emojis) else f"{placement}️⃣"
        colors = player_data.get('commander_colors', [])
        color_display = format_colors(colors)

        results_text += f"{emoji} **{player_data['username']}** - {player_data['commander']} {color_display}\n"

    embed.add_field(
        name="🏆 Final Results",
        value=results_text,
        inline=False
    )

    embed.add_field(
        name="📊 Game Info",
        value=f"**Players:** {len(game.players)}\n**Duration:** {(datetime.now() - game.start_time).total_seconds() / 60:.0f} minutes",
        inline=False
    )

    embed.set_footer(
        text="Use !commander stats to view your updated statistics!")

    return embed


def create_placement_selection_embed(game: CommanderGame, user_id: int) -> discord.Embed:
    """Create an embed for placement selection with reactions."""
    embed = discord.Embed(
        title="🏆 Set Your Placement",
        color=EMBED_COLORS.get('commander_game', 0x8B4513),
        description=f"Game: **{game.game_id}**\n\nClick the emoji reaction below to set your final placement:"
    )

    username = game.players[user_id]['username']
    commander = game.players[user_id]['commander']
    colors = game.players[user_id].get('commander_colors', [])

    # Format colors
    def format_colors(colors):
        if not colors or colors == ['?']:
            return ""
        elif colors == ['C']:
            return COLOR_EMOJIS.get('colorless', '⚪')
        else:
            color_map = {
                'W': COLOR_EMOJIS.get('white', '⚪'),
                'U': COLOR_EMOJIS.get('blue', '🔵'),
                'B': COLOR_EMOJIS.get('black', '⚫'),
                'R': COLOR_EMOJIS.get('red', '🔴'),
                'G': COLOR_EMOJIS.get('green', '🟢')
            }
            emojis = [color_map.get(color, '❓') for color in colors]
            return ''.join(emojis)

    color_display = format_colors(colors)

    embed.add_field(
        name="👤 Your Commander",
        value=f"**{username}**\n{commander} {color_display}",
        inline=False
    )

    # Show available placements
    available_placements = commander_manager.get_available_placements(game)
    placement_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

    available_text = ""
    for placement in available_placements:
        emoji = placement_emojis[placement - 1]
        place_name = ["Winner", "Second", "Third", "Fourth",
                      "Fifth", "Sixth", "Seventh", "Eighth"][placement - 1]
        available_text += f"{emoji} **{place_name}** (#{placement})\n"

    embed.add_field(
        name="🎯 Available Placements",
        value=available_text if available_text else "No placements available",
        inline=False
    )

    # Show already taken placements
    taken_placements = {}
    for pid, pdata in game.players.items():
        if pdata['placement'] is not None and pid != user_id:
            taken_placements[pdata['placement']] = pdata['username']

    if taken_placements:
        taken_text = ""
        for placement in sorted(taken_placements.keys()):
            emoji = placement_emojis[placement - 1]
            taken_text += f"{emoji} {taken_placements[placement]}\n"

        embed.add_field(
            name="✅ Already Set",
            value=taken_text,
            inline=True
        )

    embed.set_footer(
        text="React with the number emoji to set your placement • This message will expire in 5 minutes")

    return embed


def get_placement_emojis(available_placements: List[int]) -> List[str]:
    """Get list of emoji reactions for available placements."""
    placement_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    return [placement_emojis[p - 1] for p in available_placements]


def create_join_games_embed(games: List[CommanderGame], channel_id: int) -> discord.Embed:
    """Create an embed showing available games to join."""
    embed = discord.Embed(
        title="🎮 Join Commander Game",
        description="Select a game to join by reacting with the corresponding emoji:",
        color=EMBED_COLORS['commander_game']
    )

    if not games:
        embed.description = "No available games to join in this channel.\nUse `!commander create` to start a new game!"
        embed.color = discord.Color.orange()
        return embed

    game_list = ""
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

    for i, game in enumerate(games[:8]):  # Limit to 8 games max
        emoji = emojis[i]
        players_info = f"{len(game.players)}/8 players"
        creator_name = game.players.get(
            game.creator_id, {}).get('username', 'Unknown')

        game_list += f"{emoji} **{game.game_id}**\n"
        game_list += f"   👑 Creator: {creator_name}\n"
        game_list += f"   👥 {players_info}\n\n"

    embed.add_field(
        name="Available Games",
        value=game_list,
        inline=False
    )

    embed.set_footer(
        text="React with the emoji to join that game • Times out in 30 seconds")

    return embed


def get_join_game_emojis(games: List[CommanderGame]) -> List[str]:
    """Get list of emoji reactions for available games to join."""
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    return emojis[:len(games)]


def get_placement_from_emoji(emoji: str) -> Optional[int]:
    """Convert emoji reaction to placement number."""
    emoji_to_placement = {
        "1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4,
        "5️⃣": 5, "6️⃣": 6, "7️⃣": 7, "8️⃣": 8
    }
    return emoji_to_placement.get(emoji)


def create_archetype_selection_embed(commander_name: str, archetype_data: Dict, current_archetype: str) -> discord.Embed:
    """Create an embed for archetype selection with reactions."""
    embed = discord.Embed(
        title="🎯 Select Commander Archetype",
        color=EMBED_COLORS.get('commander_game', 0x8B4513),
        description=f"Choose an archetype for **{commander_name}**:"
    )
    
    archetypes = archetype_data.get('archetypes', [])
    
    if not archetypes:
        embed.description = f"No archetype data available for **{commander_name}**.\nUsing default: **{current_archetype}**"
        return embed
    
    # Show current archetype
    current_emoji = get_archetype_emoji(current_archetype)
    embed.add_field(
        name="📌 Current Archetype",
        value=f"{current_emoji} **{current_archetype}**",
        inline=False
    )
    
    # List available archetypes
    archetype_list = ""
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    
    for i, archetype in enumerate(archetypes[:8]):  # Limit to 8 for Discord reactions
        emoji = emojis[i]
        archetype_emoji = get_archetype_emoji(archetype)
        
        # Mark current archetype
        current_marker = " **← Current**" if archetype == current_archetype else ""
        
        archetype_list += f"{emoji} {archetype_emoji} **{archetype}**{current_marker}\n"
    
    embed.add_field(
        name="🎮 Available Archetypes",
        value=archetype_list if archetype_list else "No archetypes available",
        inline=False
    )
    
    embed.set_footer(
        text="React with the number emoji to change archetype • Times out in 30 seconds"
    )
    
    return embed


def get_archetype_emojis(archetypes: List[str]) -> List[str]:
    """Get list of emoji reactions for archetype selection."""
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]
    return emojis[:len(archetypes)]


def get_archetype_from_emoji(emoji: str, archetypes: List[str]) -> Optional[str]:
    """Convert emoji reaction to archetype name."""
    emoji_to_number = {
        "1️⃣": 0, "2️⃣": 1, "3️⃣": 2, "4️⃣": 3,
        "5️⃣": 4, "6️⃣": 5, "7️⃣": 6, "8️⃣": 7
    }
    
    index = emoji_to_number.get(emoji)
    if index is not None and index < len(archetypes):
        return archetypes[index]
    return None
