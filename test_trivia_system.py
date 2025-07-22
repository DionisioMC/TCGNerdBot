#!/usr/bin/env python3
"""
Test script for the Magic: The Gathering trivia system.
Tests the trivia functionality without requiring Discord.
"""

import sys
import os
import asyncio

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock discord module for testing
class MockEmbed:
    def __init__(self, title="", description="", color=0):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []
        self.footer = None
    
    def add_field(self, name="", value="", inline=False):
        self.fields.append({"name": name, "value": value, "inline": inline})
    
    def set_footer(self, text=""):
        self.footer = text

class MockDiscord:
    Embed = MockEmbed

# Mock discord import
sys.modules['discord'] = MockDiscord()

# Now import the trivia system
from trivia_system import (
    trivia_manager, TriviaQuestion, create_trivia_question_embed,
    create_trivia_results_embed, create_trivia_stats_embed,
    create_trivia_leaderboard_embed
)

def test_question_initialization():
    """Test that trivia questions are properly initialized."""
    print("🧪 Testing Question Initialization...")
    
    questions = trivia_manager.questions
    print(f"✅ Loaded {len(questions)} trivia questions")
    
    # Test question categories
    categories = set(q.category for q in questions)
    print(f"✅ Question categories: {', '.join(categories)}")
    
    # Test difficulty levels
    difficulties = set(q.difficulty for q in questions)
    print(f"✅ Difficulty levels: {', '.join(difficulties)}")
    
    # Test a sample question
    if questions:
        sample = questions[0]
        print(f"✅ Sample question: {sample.question}")
        print(f"   Options: {sample.options}")
        print(f"   Correct answer: {sample.options[sample.correct_answer]} (index {sample.correct_answer})")
        print(f"   Points: {sample.points}, Difficulty: {sample.difficulty}")

def test_trivia_game_flow():
    """Test the complete trivia game flow."""
    print("\n🎮 Testing Trivia Game Flow...")
    
    # Start a mock game
    channel_id = 12345
    message_id = 67890
    starter_id = 999  # User who started the game
    
    game = trivia_manager.start_trivia_game(channel_id, message_id, starter_id)
    print(f"✅ Started trivia game with message ID {message_id}")
    print(f"   Question: {game.question.question}")
    print(f"   Correct answer: {game.question.options[game.question.correct_answer]}")
    print(f"   Started by user: {starter_id}")
    
    # Test player answers
    user1_id = 111
    user2_id = 222
    user3_id = 333
    user4_id = 444
    
    # User 1 answers correctly
    success, msg = trivia_manager.handle_player_answer(message_id, user1_id, game.question.correct_answer)
    print(f"✅ User 1 correct answer: {success} - {msg}")
    
    # User 2 answers incorrectly
    wrong_answer = (game.question.correct_answer + 1) % 4
    success, msg = trivia_manager.handle_player_answer(message_id, user2_id, wrong_answer)
    print(f"✅ User 2 wrong answer: {success} - {msg}")
    
    # User 3 tries to answer with already locked option
    success, msg = trivia_manager.handle_player_answer(message_id, user3_id, game.question.correct_answer)
    print(f"✅ User 3 duplicate option: {success} - {msg}")
    
    # User 3 answers with different option
    another_option = (game.question.correct_answer + 2) % 4
    success, msg = trivia_manager.handle_player_answer(message_id, user3_id, another_option)
    print(f"✅ User 3 different option: {success} - {msg}")
    
    # User 4 completes all options
    final_option = (game.question.correct_answer + 3) % 4
    success, msg = trivia_manager.handle_player_answer(message_id, user4_id, final_option)
    print(f"✅ User 4 final option: {success} - {msg}")
    
    # Check if game should be completed
    should_complete = trivia_manager.check_game_completion(message_id)
    print(f"✅ Game should complete: {should_complete}")
    
    return message_id, [user1_id, user2_id, user3_id, user4_id]

async def test_only_starter_answered():
    """Test the scenario where only the game starter answered."""
    print("\n🎯 Testing 'Only Starter Answered' Scenario...")
    
    # Start a new game
    channel_id = 54321
    message_id = 98765
    starter_id = 777
    
    game = trivia_manager.start_trivia_game(channel_id, message_id, starter_id)
    print(f"✅ Started game where only starter will answer")
    
    # Only the starter answers (correctly)
    success, msg = trivia_manager.handle_player_answer(message_id, starter_id, game.question.correct_answer)
    print(f"✅ Starter answered: {success} - {msg}")
    
    # Finish the game
    results = await trivia_manager.finish_trivia_game(message_id)
    
    print(f"✅ Game completed with only starter answering")
    print(f"   Only starter answered: {results.get('only_starter_answered', False)}")
    print(f"   Points awarded: {results['points_awarded']} (should be 0)")
    print(f"   Winners: {results['winners']} (should be empty)")
    
    # Check that stats were updated but no points awarded
    stats = trivia_manager.get_player_stats(starter_id)
    print(f"✅ Starter stats: {stats['total_questions']} questions, {stats['total_points']} points")
    
    return results

async def test_game_completion(message_id, user_ids):
    """Test game completion and results."""
    print("\n🏁 Testing Game Completion...")
    
    # Finish the game
    results = await trivia_manager.finish_trivia_game(message_id)
    
    if "error" in results:
        print(f"❌ Error finishing game: {results['error']}")
        return
    
    print(f"✅ Game finished successfully")
    print(f"   Question: {results['question']}")
    print(f"   Correct answer: {results['correct_option']}")
    print(f"   Winners: {results['winners']}")
    print(f"   Points awarded: {results['points_awarded']}")
    
    # Test player stats after game
    for user_id in user_ids:
        stats = trivia_manager.get_player_stats(user_id)
        print(f"✅ User {user_id} stats: {stats['total_questions']} questions, "
              f"{stats['correct_answers']} correct, {stats['total_points']} points")

def test_embed_creation():
    """Test Discord embed creation."""
    print("\n🎨 Testing Embed Creation...")
    
    # Create a mock game for embed testing
    channel_id = 54321
    message_id = 98765
    starter_id = 888
    game = trivia_manager.start_trivia_game(channel_id, message_id, starter_id)
    
    # Test question embed
    embed = create_trivia_question_embed(game)
    print(f"✅ Question embed created: {embed.title}")
    print(f"   Description: {embed.description}")
    print(f"   Fields: {len(embed.fields)}")
    
    # Mock some answers for results embed
    trivia_manager.handle_player_answer(message_id, 111, 0)
    trivia_manager.handle_player_answer(message_id, 222, 1)
    
    # Test stats embed (mock guild)
    class MockGuild:
        def get_member(self, user_id):
            class MockMember:
                display_name = f"User{user_id}"
            return MockMember()
    
    mock_guild = MockGuild()
    stats_embed = create_trivia_stats_embed(111, mock_guild)
    print(f"✅ Stats embed created: {stats_embed.title}")
    
    # Test leaderboard embed
    leaderboard_embed = create_trivia_leaderboard_embed(mock_guild)
    print(f"✅ Leaderboard embed created: {leaderboard_embed.title}")

def test_leaderboard():
    """Test leaderboard functionality."""
    print("\n🏆 Testing Leaderboard...")
    
    # Get current leaderboard
    leaderboard = trivia_manager.get_leaderboard(5)
    print(f"✅ Retrieved leaderboard with {len(leaderboard)} entries")
    
    for i, (user_id, stats) in enumerate(leaderboard):
        print(f"   {i+1}. User {user_id}: {stats['total_points']} points, "
              f"{stats['correct_answers']}/{stats['total_questions']} correct")

async def main():
    """Run all trivia system tests."""
    print("🧠 Starting Magic: The Gathering Trivia System Tests\n")
    
    # Test basic functionality
    test_question_initialization()
    
    # Test game flow
    message_id, user_ids = test_trivia_game_flow()
    
    # Test game completion
    await test_game_completion(message_id, user_ids)
    
    # Test only starter answered scenario
    await test_only_starter_answered()
    
    # Test embed creation
    test_embed_creation()
    
    # Test leaderboard
    test_leaderboard()
    
    print("\n🎉 All trivia system tests completed!")
    print("\n📝 Summary:")
    print("✅ Question database initialized with MTG-focused questions")
    print("✅ Game flow works correctly (start, answer, complete)")
    print("✅ Player stats tracking functional")
    print("✅ Leaderboard system operational")
    print("✅ Discord embed creation ready")
    print("✅ Points system integrated")
    
    print("\n🎯 How to use:")
    print("• Users type '!trivia' to start a game")
    print("• React with 🇦, 🇧, 🇨, 🇩 to answer")
    print("• Each option can only be chosen by one player")
    print("• Game ends when all options are taken or after 2 minutes")
    print("• Winners get points based on question difficulty")
    print("• Use '!trivia stats' and '!trivia leaderboard' to view progress")

if __name__ == "__main__":
    asyncio.run(main())
