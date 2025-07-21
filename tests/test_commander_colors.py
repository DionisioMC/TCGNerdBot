"""
Test script for commander games color functionality.
This script tests the color tracking features without requiring Discord.
"""

import asyncio
import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the discord and config imports for testing
class MockEmbed:
    def __init__(self, title="", color=0, description=""):
        self.title = title
        self.color = color
        self.description = description
        self.fields = []
    
    def add_field(self, name="", value="", inline=False):
        self.fields.append({"name": name, "value": value, "inline": inline})
    
    def set_footer(self, text=""):
        self.footer = text

# Mock discord module
class MockDiscord:
    Embed = MockEmbed

sys.modules['discord'] = MockDiscord()

# Mock config
class MockConfig:
    EMBED_COLORS = {
        'commander_game': 0x8B4513,
        'commander_stats': 0x8B4513,
        'success': 0x00ff00
    }
    
    COLOR_EMOJIS = {
        'white': '⚪',
        'blue': '🔵', 
        'black': '⚫',
        'red': '🔴', 
        'green': '🟢',
        'colorless': '⚪'
    }

sys.modules['config'] = MockConfig()

# Mock scryfall_api
class MockScryfallAPI:
    @classmethod
    async def get_card_by_name(cls, card_name: str):
        # Return mock data for common commanders
        mock_commanders = {
            'atraxa, praetors\' voice': {
                'color_identity': ['W', 'U', 'B', 'G']
            },
            'edgar markov': {
                'color_identity': ['W', 'B', 'R']
            },
            'meren of clan nel toth': {
                'color_identity': ['B', 'G']
            },
            'rhys the redeemed': {
                'color_identity': ['W', 'G']
            },
            'kozilek, the great distortion': {
                'color_identity': []  # Colorless
            }
        }
        
        return mock_commanders.get(card_name.lower())

sys.modules['scryfall_api'] = type('MockScryfallAPI', (), {'ScryfallAPI': MockScryfallAPI})()

# Now import the actual module
from commander_games import CommanderGameManager, create_player_stats_embed

async def test_color_functionality():
    """Test the color tracking functionality."""
    print("🧪 Testing Commander Games Color Functionality")
    print("=" * 50)
    
    # Create a manager
    manager = CommanderGameManager()
    
    # Create a test game
    success, msg, game = manager.create_game(12345, 67890, "TestUser1")
    print(f"✅ Created game: {success}")
    print(f"   Message: {msg}")
    
    if not success:
        return
    
    game_id = game.game_id
    
    # Add another player
    success, msg = manager.join_game(game_id, 54321, "TestUser2")
    print(f"✅ Player 2 joined: {success}")
    
    # Test setting commanders with colors
    print("\n🎴 Testing Commander Color Tracking:")
    
    commanders_to_test = [
        ("Atraxa, Praetors' Voice", 12345, "TestUser1"),
        ("Edgar Markov", 54321, "TestUser2")
    ]
    
    for commander, user_id, username in commanders_to_test:
        success, msg = await manager.set_commander(game_id, user_id, commander)
        print(f"   {username} set commander to {commander}: {success}")
        print(f"   Response: {msg}")
        
        if success:
            player_data = game.players[user_id]
            colors = player_data.get('commander_colors', [])
            print(f"   Colors stored: {colors}")
    
    # Set placements
    manager.set_placement(game_id, 12345, 1)
    manager.set_placement(game_id, 54321, 2)
    
    # Finish the game
    success, msg, finished_game = manager.finish_game(game_id, 12345)
    print(f"\n🏁 Game finished: {success}")
    
    # Test statistics
    print("\n📊 Testing Statistics:")
    stats = manager.get_player_stats(12345)
    print(f"   Player stats keys: {list(stats.keys())}")
    if 'colors_played' in stats:
        print(f"   Colors played: {stats['colors_played']}")
        print(f"   Favorite colors: {stats.get('favorite_colors')}")
        print(f"   Mono games: {stats.get('mono_color_games', 0)}")
        print(f"   Multi games: {stats.get('multicolor_games', 0)}")
    
    # Test embed creation
    print("\n🎨 Testing Embed Creation:")
    embed = create_player_stats_embed(12345, "TestUser1", stats)
    print(f"   Embed title: {embed.title}")
    print(f"   Number of fields: {len(embed.fields)}")
    for field in embed.fields:
        if "Colors" in field['name']:
            print(f"   Color field: {field['name']} = {field['value']}")
    
    print("\n✅ Test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_color_functionality())
