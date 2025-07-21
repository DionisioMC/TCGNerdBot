"""
Test script for enhanced commander game functionality:
- Leave without game_id
- Join with reaction-based game selection
"""
import asyncio
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(__file__))

from commander_games import CommanderGameManager, create_join_games_embed, get_join_game_emojis

async def test_enhanced_functionality():
    print("🎯 Testing enhanced commander game functionality...")
    
    # Initialize game manager
    manager = CommanderGameManager()
    
    # Test user IDs
    user1_id = 123456789
    user2_id = 987654321
    user3_id = 555555555
    channel_id = 123456
    
    print("\n1. Creating multiple games...")
    success1, msg1, game1 = manager.create_game(user1_id, channel_id, "User1")
    print(f"   Game 1: {msg1}")
    assert success1, "Game 1 creation failed"
    
    success2, msg2, game2 = manager.create_game(user2_id, channel_id, "User2") 
    print(f"   Game 2: {msg2}")
    assert success2, "Game 2 creation failed"
    
    print("\n2. Testing get_joinable_games_for_user...")
    joinable_games = manager.get_joinable_games_for_user(channel_id, user3_id)
    print(f"   Found {len(joinable_games)} joinable games for user3")
    assert len(joinable_games) == 2, "Should find 2 joinable games"
    
    print("\n3. Testing join games embed creation...")
    embed_dict = create_join_games_embed(joinable_games, channel_id)
    print(f"   Embed title: {embed_dict.title}")
    print(f"   Embed has fields: {len(embed_dict.fields)}")
    
    print("\n4. Testing join game emojis...")
    emojis = get_join_game_emojis(joinable_games)
    print(f"   Emojis: {emojis}")
    assert len(emojis) == 2, "Should have 2 emojis for 2 games"
    
    print("\n5. User3 joins game1...")
    success, msg = manager.join_game(game1.game_id, user3_id, "User3")
    print(f"   Result: {msg}")
    assert success, "Failed to join game1"
    
    print("\n6. Testing leave_game_by_user (user3 leaves)...")
    success, msg, game = manager.leave_game_by_user(user3_id)
    print(f"   Result: {msg}")
    assert success, "Failed to leave game using new method"
    
    print("\n7. Testing leave_game_by_user when not in any game...")
    success, msg, game = manager.leave_game_by_user(user3_id)
    print(f"   Result: {msg}")
    assert not success, "Should fail when not in any game"
    
    print("\n8. User3 joins game1 again...")
    success, msg = manager.join_game(game1.game_id, user3_id, "User3")
    print(f"   Result: {msg}")
    assert success, "Failed to join game1 again"
    
    print("\n9. Testing setcommander_by_user for user3...")
    success, msg, game = await manager.set_commander_by_user(user3_id, "Krenko, Mob Boss")
    print(f"   Result: {msg}")
    assert success, "Failed to set commander without game_id"
    
    print("\n10. Checking joinable games after user3 joined...")
    joinable_games_after = manager.get_joinable_games_for_user(channel_id, user3_id)
    print(f"   Found {len(joinable_games_after)} joinable games for user3 (should be 1)")
    assert len(joinable_games_after) == 1, "Should find 1 joinable game (user3 is now in game1)"
    
    print("\n11. Testing with channel that has no games...")
    empty_channel_games = manager.get_joinable_games_for_user(999999, user3_id)
    print(f"   Games in empty channel: {len(empty_channel_games)}")
    assert len(empty_channel_games) == 0, "Empty channel should have no games"
    
    print("\n✅ All enhanced functionality tests passed!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_functionality())
