"""
Test script for setcommander without game_id functionality
"""
import asyncio
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(__file__))

from commander_games import CommanderGameManager
from scryfall_api import ScryfallAPI

async def test_setcommander_no_id():
    print("🎯 Testing setcommander without game_id...")
    
    # Initialize game manager
    manager = CommanderGameManager()
    
    # Test user IDs
    user1_id = 123456789
    user2_id = 987654321
    
    print("\n1. Creating a game...")
    success, msg, game = manager.create_game(user1_id, 123456, "TestUser1")  # Using int for channel_id
    print(f"   Result: {msg}")
    assert success, "Game creation failed"
    assert game is not None, "Game object should not be None"
    game_id = game.game_id
    
    print("\n2. Adding another player...")
    success, msg = manager.join_game(game_id, user2_id, "TestUser2")
    print(f"   Result: {msg}")
    assert success, "Failed to join game"
    
    print("\n3. Testing new setcommander (without game_id) for user1...")
    success, msg, game = await manager.set_commander_by_user(user1_id, "Atraxa, Praetors' Voice")
    print(f"   Result: {msg}")
    assert success, "Failed to set commander without game_id"
    
    print("\n4. Testing new setcommander (without game_id) for user2...")
    success, msg, game = await manager.set_commander_by_user(user2_id, "Edgar Markov")
    print(f"   Result: {msg}")
    assert success, "Failed to set commander without game_id for second user"
    
    print("\n5. Testing with user not in any game...")
    user3_id = 555555555
    success, msg, game = await manager.set_commander_by_user(user3_id, "Krenko, Mob Boss")
    print(f"   Result: {msg}")
    assert not success, "Should fail for user not in any game"
    
    print("\n6. Verifying old setcommander (with game_id) still works...")
    success, msg = await manager.set_commander(game_id, user1_id, "Kaalia of the Vast")
    print(f"   Result: {msg}")
    assert success, "Old format should still work"
    
    print("\n7. Getting game info to verify changes...")
    game = manager.get_game_info(game_id)
    if game:
        print(f"   Game has {len(game.players)} players")
        for player_id, player_data in game.players.items():
            commander = player_data.get('commander', 'Not set')
            colors = player_data.get('commander_colors', [])
            print(f"   Player {player_id}: {commander} (colors: {colors})")
    
    print("\n✅ All setcommander without game_id tests passed!")

if __name__ == "__main__":
    asyncio.run(test_setcommander_no_id())
