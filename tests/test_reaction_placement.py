"""
Test script for the new reaction-based placement system.
"""

import asyncio
import sys
import os

# Mock the discord and config imports for testing
class MockUser:
    def __init__(self, user_id, display_name):
        self.id = user_id
        self.display_name = display_name

class MockReaction:
    def __init__(self, emoji, message_id):
        self.emoji = emoji
        self.message = type('MockMessage', (), {'id': message_id})()

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

class MockDiscord:
    Embed = MockEmbed
    User = MockUser
    Reaction = MockReaction

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
        mock_commanders = {
            'atraxa, praetors\' voice': {'color_identity': ['W', 'U', 'B', 'G']},
            'edgar markov': {'color_identity': ['W', 'B', 'R']},
        }
        return mock_commanders.get(card_name.lower())

sys.modules['scryfall_api'] = type('MockScryfallAPI', (), {'ScryfallAPI': MockScryfallAPI})()

# Now import the actual modules
from commander_games import (
    CommanderGameManager, create_placement_selection_embed, 
    get_placement_emojis, get_placement_from_emoji
)

async def test_reaction_placement():
    """Test the new reaction-based placement system."""
    print("🎯 Testing Reaction-Based Placement System")
    print("=" * 50)
    
    # Create a manager and game
    manager = CommanderGameManager()
    success, msg, game = manager.create_game(12345, 67890, "Alice")
    print(f"✅ Created game: {success}")
    
    # Add players
    manager.join_game(game.game_id, 54321, "Bob")
    manager.join_game(game.game_id, 98765, "Charlie")
    
    # Set commanders
    await manager.set_commander(game.game_id, 12345, "Atraxa, Praetors' Voice")
    await manager.set_commander(game.game_id, 54321, "Edgar Markov")
    await manager.set_commander(game.game_id, 98765, "Edgar Markov")
    
    print(f"Game has {len(game.players)} players")
    
    # Test placement selection embed
    print("\n📋 Testing Placement Selection Embed:")
    embed = create_placement_selection_embed(game, 12345)
    print(f"   Title: {embed.title}")
    print(f"   Description: {embed.description}")
    print(f"   Fields: {len(embed.fields)}")
    
    # Test available placements
    available = manager.get_available_placements(game)
    print(f"\n🎯 Available placements: {available}")
    
    # Test emoji generation
    emojis = get_placement_emojis(available)
    print(f"   Emojis for reactions: {emojis}")
    
    # Test emoji to placement conversion
    for emoji in emojis:
        placement = get_placement_from_emoji(emoji)
        print(f"   {emoji} → Placement {placement}")
    
    # Test setting placement by reaction
    print("\n⚡ Testing Reaction Placement Setting:")
    success, msg, updated_game = manager.set_placement_by_reaction(12345, 1)
    print(f"   Alice sets placement 1: {success} - {msg}")
    
    success, msg, updated_game = manager.set_placement_by_reaction(54321, 2)
    print(f"   Bob sets placement 2: {success} - {msg}")
    
    # Test conflict
    success, msg, updated_game = manager.set_placement_by_reaction(98765, 1)
    print(f"   Charlie tries placement 1: {success} - {msg}")
    
    # Test available placements after some are taken
    available_after = manager.get_available_placements(game)
    print(f"\n🎯 Available placements after setting some: {available_after}")
    
    # Test user finding their game
    user_game = manager.get_user_unfinished_game(12345)
    print(f"\n🔍 Alice's unfinished game found: {user_game is not None}")
    
    print("\n✅ Reaction placement test completed!")

if __name__ == "__main__":
    asyncio.run(test_reaction_placement())
