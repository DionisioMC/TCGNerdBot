"""
Magic: The Gathering Trivia System for TCG Nerd Bot.
Handles trivia questions, player answers, and scoring.
"""

import asyncio
import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
import discord
from config import EMBED_COLORS

class TriviaQuestion:
    """Represents a single trivia question."""
    
    def __init__(self, question: str, options: List[str], correct_answer: int, 
                 points: int = 10, difficulty: str = "medium", category: str = "general"):
        self.question = question
        self.options = options  # List of 4 options
        self.correct_answer = correct_answer  # Index of correct option (0-3)
        self.points = points
        self.difficulty = difficulty
        self.category = category

class TriviaGame:
    """Represents an active trivia game session."""
    
    def __init__(self, channel_id: int, message_id: int, question: TriviaQuestion, started_by: int):
        self.channel_id = channel_id
        self.message_id = message_id
        self.question = question
        self.started_by = started_by  # User ID of who started the game
        self.player_answers: Dict[int, int] = {}  # user_id -> answer_index
        self.locked_options: Set[int] = set()  # Set of locked option indices
        self.start_time = datetime.now()
        self.is_finished = False
        self.time_limit = 120  # 2 minutes

class TriviaManager:
    """Manages trivia games and player statistics."""
    
    def __init__(self, trivia_data_file: str = "trivia_stats.json"):
        self.trivia_data_file = trivia_data_file
        self.active_games: Dict[int, TriviaGame] = {}  # message_id -> TriviaGame
        self.player_stats = self._load_player_stats()
        self.questions = self._initialize_questions()
        
    def _load_player_stats(self) -> Dict[int, Dict]:
        """Load player trivia statistics from file."""
        if os.path.exists(self.trivia_data_file):
            try:
                with open(self.trivia_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_player_stats(self):
        """Save player trivia statistics to file."""
        try:
            with open(self.trivia_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.player_stats, f, indent=2)
        except IOError as e:
            print(f"Error saving trivia stats: {e}")
    
    def _initialize_questions(self) -> List[TriviaQuestion]:
        """Initialize trivia questions database."""
        questions = []
        
        # Basic MTG Questions
        questions.extend([
            TriviaQuestion(
                "How many cards are in a standard Magic: The Gathering deck?",
                ["40", "60", "75", "100"],
                1, 5, "easy", "rules"
            ),
            TriviaQuestion(
                "What is the minimum number of cards in a Commander deck?",
                ["60", "75", "99", "100"],
                3, 5, "easy", "commander"
            ),
            TriviaQuestion(
                "Which color is associated with drawing cards and counterspells?",
                ["White", "Blue", "Black", "Red"],
                1, 5, "easy", "colors"
            ),
            TriviaQuestion(
                "What does 'WUBRG' stand for in Magic terms?",
                ["White, Blue, Black, Red, Green", "Win, Untap, Block, Resolve, Go", "Wizard, Unicorn, Beast, Rogue, Goblin", "Water, Underground, Bridge, River, Ground"],
                0, 10, "medium", "colors"
            ),
        ])
        
        # Commander Specific Questions
        questions.extend([
            TriviaQuestion(
                "In Commander, what is the 'Command Zone'?",
                ["The graveyard", "A special zone where your commander starts", "The library", "The battlefield"],
                1, 10, "medium", "commander"
            ),
            TriviaQuestion(
                "What happens when a commander dies in Commander format?",
                ["It goes to the graveyard permanently", "It can be put back in the command zone", "It gets shuffled into the library", "The game ends"],
                1, 10, "medium", "commander"
            ),
            TriviaQuestion(
                "How much additional mana does it cost to cast your commander each time after the first?",
                ["0", "1", "2", "X, where X is the number of times cast"],
                2, 10, "medium", "commander"
            ),
            TriviaQuestion(
                "What is the starting life total in Commander?",
                ["20", "25", "30", "40"],
                3, 10, "medium", "commander"
            ),
        ])
        
        # Card Knowledge Questions
        questions.extend([
            TriviaQuestion(
                "Which planeswalker is known as the 'Mind Sculptor'?",
                ["Liliana Vess", "Jace Beleren", "Chandra Nalaar", "Gideon Jura"],
                1, 15, "hard", "planeswalkers"
            ),
            TriviaQuestion(
                "What creature type is associated with the phrase 'Dies to Doom Blade'?",
                ["Artifact creatures", "Non-black creatures", "Flying creatures", "Legendary creatures"],
                1, 15, "hard", "cards"
            ),
            TriviaQuestion(
                "Which card is banned in almost every format due to its power level?",
                ["Lightning Bolt", "Counterspell", "Black Lotus", "Giant Growth"],
                2, 20, "hard", "cards"
            ),
            TriviaQuestion(
                "What does the term 'ETB' stand for in Magic?",
                ["End the Battle", "Enters the Battlefield", "Exile to Bottom", "Extra Turn Begins"],
                1, 10, "medium", "terminology"
            ),
        ])
        
        # Lore and Flavor Questions
        questions.extend([
            TriviaQuestion(
                "What is the name of the multiverse in Magic: The Gathering?",
                ["The Blind Eternities", "The Æther", "The Void", "The Nexus"],
                0, 15, "hard", "lore"
            ),
            TriviaQuestion(
                "Which plane is known for its five Shards?",
                ["Ravnica", "Alara", "Zendikar", "Innistrad"],
                1, 15, "hard", "lore"
            ),
            TriviaQuestion(
                "What are the five colors of magic called collectively?",
                ["The Pentagon", "The Color Wheel", "The Pentarchy", "The Mana Circle"],
                1, 10, "medium", "lore"
            ),
            TriviaQuestion(
                "Which guild from Ravnica is associated with White and Blue?",
                ["Azorius Senate", "Orzhov Syndicate", "Selesnya Conclave", "Simic Combine"],
                0, 15, "hard", "lore"
            ),
        ])
        
        # Format and Rules Questions
        questions.extend([
            TriviaQuestion(
                "In which format are fetchlands like Flooded Strand legal?",
                ["Standard only", "Modern and Legacy", "Legacy and Vintage only", "All formats"],
                1, 15, "hard", "formats"
            ),
            TriviaQuestion(
                "What is the 'stack' in Magic: The Gathering?",
                ["A pile of discarded cards", "The order in which spells resolve", "A type of deck construction", "The command zone"],
                1, 10, "medium", "rules"
            ),
            TriviaQuestion(
                "Which of these is NOT a basic land type?",
                ["Island", "Swamp", "Wastes", "Desert"],
                3, 10, "medium", "cards"
            ),
            TriviaQuestion(
                "What does 'RTFC' mean in Magic slang?",
                ["Return to First Cast", "Read the Full Card", "Resolve the Final Cost", "Really Tough Flying Creature"],
                1, 10, "medium", "terminology"
            ),
        ])
        
        # Advanced Questions
        questions.extend([
            TriviaQuestion(
                "Which of these creatures has the highest converted mana cost ever printed?",
                ["Emrakul, the Aeons Torn", "Draco", "Autochthon Wurm", "B.F.M. (Big Furry Monster)"],
                1, 25, "expert", "cards"
            ),
            TriviaQuestion(
                "What was the first planeswalker card ever printed?",
                ["Jace Beleren", "Ajani Goldmane", "Liliana Vess", "All were printed simultaneously"],
                3, 20, "expert", "history"
            ),
            TriviaQuestion(
                "Which mechanic allows you to play cards from your graveyard?",
                ["Flashback", "Unearth", "Retrace", "All of the above"],
                3, 15, "hard", "mechanics"
            ),
            TriviaQuestion(
                "In Commander, which of these is NOT a legal target for 'target opponent'?",
                ["The player to your left", "Yourself", "Any other player in the game", "The last player to cast a spell"],
                1, 15, "hard", "commander"
            ),
        ])
        
        return questions
    
    def get_random_question(self) -> TriviaQuestion:
        """Get a random trivia question."""
        return random.choice(self.questions)
    
    def start_trivia_game(self, channel_id: int, message_id: int, started_by: int) -> TriviaGame:
        """Start a new trivia game."""
        question = self.get_random_question()
        game = TriviaGame(channel_id, message_id, question, started_by)
        self.active_games[message_id] = game
        
        # Schedule automatic completion after time limit
        asyncio.create_task(self._auto_finish_game(message_id))
        
        return game
    
    async def _auto_finish_game(self, message_id: int):
        """Automatically finish a game after the time limit."""
        await asyncio.sleep(120)  # 2 minutes
        if message_id in self.active_games and not self.active_games[message_id].is_finished:
            await self._finish_game_internal(message_id, timeout=True)
    
    def handle_player_answer(self, message_id: int, user_id: int, answer_option: int) -> Tuple[bool, str]:
        """Handle a player's answer attempt."""
        if message_id not in self.active_games:
            return False, "No active trivia game found."
        
        game = self.active_games[message_id]
        
        if game.is_finished:
            return False, "This trivia game has already ended."
        
        # Check if player already answered
        if user_id in game.player_answers:
            return False, "You have already answered this question!"
        
        # Check if the option is already locked
        if answer_option in game.locked_options:
            return False, "This answer option is already taken by another player!"
        
        # Lock the option and record the answer
        game.locked_options.add(answer_option)
        game.player_answers[user_id] = answer_option
        
        return True, f"Answer recorded! You selected option {answer_option + 1}."
    
    async def _finish_game_internal(self, message_id: int, timeout: bool = False) -> Dict:
        """Internal method to finish a game and calculate results."""
        if message_id not in self.active_games:
            return {"error": "Game not found"}
        
        game = self.active_games[message_id]
        game.is_finished = True
        
        # Check if only the game starter answered (no points awarded in this case)
        only_starter_answered = (
            len(game.player_answers) == 1 and 
            game.started_by in game.player_answers
        )
        
        # Calculate results
        results = {
            "question": game.question.question,
            "options": game.question.options,
            "correct_answer": game.question.correct_answer,
            "correct_option": game.question.options[game.question.correct_answer],
            "points_awarded": 0 if only_starter_answered else game.question.points,
            "timeout": timeout,
            "winners": [],
            "all_answers": {},
            "only_starter_answered": only_starter_answered
        }
        
        # Find winners and update stats
        for user_id, answer_index in game.player_answers.items():
            results["all_answers"][user_id] = {
                "answer_index": answer_index,
                "answer_text": game.question.options[answer_index],
                "correct": answer_index == game.question.correct_answer
            }
            
            # Update player stats
            user_id_str = str(user_id)
            if user_id_str not in self.player_stats:
                self.player_stats[user_id_str] = {
                    "total_questions": 0,
                    "correct_answers": 0,
                    "total_points": 0,
                    "categories": {},
                    "difficulty_stats": {},
                    "last_played": None
                }
            
            stats = self.player_stats[user_id_str]
            stats["total_questions"] += 1
            stats["last_played"] = datetime.now().isoformat()
            
            # Update category stats
            category = game.question.category
            if category not in stats["categories"]:
                stats["categories"][category] = {"total": 0, "correct": 0}
            stats["categories"][category]["total"] += 1
            
            # Update difficulty stats
            difficulty = game.question.difficulty
            if difficulty not in stats["difficulty_stats"]:
                stats["difficulty_stats"][difficulty] = {"total": 0, "correct": 0}
            stats["difficulty_stats"][difficulty]["total"] += 1
            
            # Award points if correct AND not only the starter answered
            if answer_index == game.question.correct_answer:
                stats["correct_answers"] += 1
                stats["categories"][category]["correct"] += 1
                stats["difficulty_stats"][difficulty]["correct"] += 1
                
                # Only award points if multiple people participated
                if not only_starter_answered:
                    stats["total_points"] += game.question.points
                    results["winners"].append(user_id)
        
        # Save updated stats
        self._save_player_stats()
        
        # Remove from active games
        del self.active_games[message_id]
        
        return results
    
    def check_game_completion(self, message_id: int) -> bool:
        """Check if a trivia game should be completed (all 4 options locked)."""
        if message_id not in self.active_games:
            return False
        
        game = self.active_games[message_id]
        return len(game.locked_options) == 4
    
    async def finish_trivia_game(self, message_id: int) -> Dict:
        """Finish a trivia game and return results."""
        return await self._finish_game_internal(message_id, timeout=False)
    
    def get_player_stats(self, user_id: int) -> Dict:
        """Get trivia statistics for a player."""
        user_id_str = str(user_id)
        if user_id_str not in self.player_stats:
            return {
                "total_questions": 0,
                "correct_answers": 0,
                "total_points": 0,
                "accuracy": 0.0,
                "categories": {},
                "difficulty_stats": {},
                "last_played": None
            }
        
        stats = self.player_stats[user_id_str].copy()
        if stats["total_questions"] > 0:
            stats["accuracy"] = (stats["correct_answers"] / stats["total_questions"]) * 100
        else:
            stats["accuracy"] = 0.0
        
        return stats
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, Dict]]:
        """Get trivia leaderboard by points."""
        leaderboard = []
        for user_id, stats in self.player_stats.items():
            leaderboard.append((user_id, stats))
        
        # Sort by points, then by accuracy
        leaderboard.sort(key=lambda x: (x[1]["total_points"], x[1].get("accuracy", 0)), reverse=True)
        return leaderboard[:limit]

# Global trivia manager instance
trivia_manager = TriviaManager()

def create_trivia_question_embed(game: TriviaGame) -> discord.Embed:
    """Create an embed for a trivia question."""
    embed = discord.Embed(
        title="🧠 Magic: The Gathering Trivia",
        description=game.question.question,
        color=EMBED_COLORS.get('trivia', 0x9b59b6)
    )
    
    # Add options
    option_emojis = ["🇦", "🇧", "🇨", "🇩"]
    options_text = ""
    for i, option in enumerate(game.question.options):
        status = ""
        if i in game.locked_options:
            # Find who locked this option
            locker = None
            for user_id, answer_idx in game.player_answers.items():
                if answer_idx == i:
                    locker = f"<@{user_id}>"
                    break
            status = f" 🔒 _{locker}_"
        
        options_text += f"{option_emojis[i]} {option}{status}\n"
    
    embed.add_field(name="Answer Options:", value=options_text, inline=False)
    
    # Add game info
    embed.add_field(name="Points:", value=f"{game.question.points}", inline=True)
    embed.add_field(name="Difficulty:", value=f"{game.question.difficulty.title()}", inline=True)
    embed.add_field(name="Category:", value=f"{game.question.category.title()}", inline=True)
    
    # Add participation info
    locked_count = len(game.locked_options)
    embed.add_field(
        name="Participation:", 
        value=f"{locked_count}/4 options locked", 
        inline=True
    )
    
    # Time remaining
    elapsed = (datetime.now() - game.start_time).total_seconds()
    remaining = max(0, 120 - elapsed)
    embed.add_field(
        name="Time Remaining:", 
        value=f"{int(remaining)}s", 
        inline=True
    )
    
    embed.set_footer(text="React with 🇦, 🇧, 🇨, or 🇩 to answer! Each option can only be selected by one player.")
    
    return embed

def create_trivia_results_embed(results: Dict, guild) -> discord.Embed:
    """Create an embed showing trivia results."""
    if results.get("timeout"):
        title = "⏰ Trivia Time's Up!"
        color = EMBED_COLORS.get('trivia_timeout', 0xe67e22)
    else:
        title = "🎯 Trivia Results!"
        color = EMBED_COLORS.get('trivia_correct', 0x27ae60)
    
    embed = discord.Embed(
        title=title,
        description=results["question"],
        color=color
    )
    
    # Show correct answer
    option_emojis = ["🇦", "🇧", "🇨", "🇩"]
    correct_emoji = option_emojis[results["correct_answer"]]
    embed.add_field(
        name="✅ Correct Answer:", 
        value=f"{correct_emoji} {results['correct_option']}", 
        inline=False
    )
    
    # Show winners
    if results.get("only_starter_answered"):
        embed.add_field(
            name="⚠️ No Competition:", 
            value="Only the person who started the trivia answered!\nNo points awarded - need multiple participants to earn points.", 
            inline=False
        )
    elif results["winners"]:
        winner_mentions = []
        for winner_id in results["winners"]:
            try:
                member = guild.get_member(winner_id)
                if member:
                    winner_mentions.append(member.display_name)
                else:
                    winner_mentions.append(f"<@{winner_id}>")
            except:
                winner_mentions.append(f"<@{winner_id}>")
        
        points_text = f"+{results['points_awarded']} points each!" if results['points_awarded'] > 0 else "No points awarded"
        embed.add_field(
            name=f"🏆 Winner{'s' if len(results['winners']) > 1 else ''}:", 
            value=f"{', '.join(winner_mentions)}\n{points_text}", 
            inline=False
        )
    else:
        embed.add_field(
            name="😢 No Winners:", 
            value="No one got the correct answer this time!", 
            inline=False
        )
    
    # Show all answers
    if results["all_answers"]:
        answers_text = ""
        for user_id, answer_data in results["all_answers"].items():
            try:
                member = guild.get_member(user_id)
                name = member.display_name if member else f"<@{user_id}>"
            except:
                name = f"<@{user_id}>"
            
            emoji = option_emojis[answer_data["answer_index"]]
            status = "✅" if answer_data["correct"] else "❌"
            answers_text += f"{status} {name}: {emoji} {answer_data['answer_text']}\n"
        
        embed.add_field(name="📋 All Answers:", value=answers_text, inline=False)
    
    return embed

def create_trivia_stats_embed(user_id: int, guild) -> discord.Embed:
    """Create an embed showing player trivia statistics."""
    stats = trivia_manager.get_player_stats(user_id)
    
    try:
        member = guild.get_member(user_id)
        username = member.display_name if member else f"User {user_id}"
    except:
        username = f"User {user_id}"
    
    embed = discord.Embed(
        title=f"🧠 Trivia Stats for {username}",
        color=EMBED_COLORS.get('analytics', 0x3498db)
    )
    
    # Overall stats
    embed.add_field(
        name="📊 Overall Performance:",
        value=f"**Questions Answered:** {stats['total_questions']}\n"
              f"**Correct Answers:** {stats['correct_answers']}\n"
              f"**Accuracy:** {stats['accuracy']:.1f}%\n"
              f"**Total Points:** {stats['total_points']}",
        inline=True
    )
    
    # Category breakdown
    if stats['categories']:
        category_text = ""
        for category, cat_stats in stats['categories'].items():
            accuracy = (cat_stats['correct'] / cat_stats['total'] * 100) if cat_stats['total'] > 0 else 0
            category_text += f"**{category.title()}:** {cat_stats['correct']}/{cat_stats['total']} ({accuracy:.1f}%)\n"
        
        embed.add_field(
            name="📂 Category Performance:",
            value=category_text,
            inline=True
        )
    
    # Difficulty breakdown
    if stats['difficulty_stats']:
        difficulty_text = ""
        for difficulty, diff_stats in stats['difficulty_stats'].items():
            accuracy = (diff_stats['correct'] / diff_stats['total'] * 100) if diff_stats['total'] > 0 else 0
            difficulty_text += f"**{difficulty.title()}:** {diff_stats['correct']}/{diff_stats['total']} ({accuracy:.1f}%)\n"
        
        embed.add_field(
            name="🎯 Difficulty Breakdown:",
            value=difficulty_text,
            inline=True
        )
    
    # Last played
    if stats['last_played']:
        try:
            last_played = datetime.fromisoformat(stats['last_played'])
            embed.set_footer(text=f"Last played: {last_played.strftime('%Y-%m-%d %H:%M')}")
        except:
            pass
    
    return embed

def create_trivia_leaderboard_embed(guild) -> discord.Embed:
    """Create an embed showing the trivia leaderboard."""
    leaderboard = trivia_manager.get_leaderboard(10)
    
    embed = discord.Embed(
        title="🏆 Trivia Leaderboard",
        description="Top players by total trivia points",
        color=EMBED_COLORS.get('achievements', 0xf39c12)
    )
    
    if not leaderboard:
        embed.add_field(
            name="🤔 No Data Yet",
            value="No trivia games have been played yet! Use `!trivia` to start one.",
            inline=False
        )
        return embed
    
    rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    leaderboard_text = ""
    
    for i, (user_id_str, stats) in enumerate(leaderboard):
        try:
            user_id = int(user_id_str)
            member = guild.get_member(user_id)
            username = member.display_name if member else f"Unknown User"
        except:
            username = "Unknown User"
        
        rank_emoji = rank_emojis[i] if i < len(rank_emojis) else f"{i+1}."
        accuracy = (stats['correct_answers'] / stats['total_questions'] * 100) if stats['total_questions'] > 0 else 0
        
        leaderboard_text += f"{rank_emoji} **{username}**\n"
        leaderboard_text += f"     Points: {stats['total_points']} | Accuracy: {accuracy:.1f}% | Questions: {stats['total_questions']}\n\n"
    
    embed.add_field(
        name="👑 Top Players:",
        value=leaderboard_text,
        inline=False
    )
    
    return embed
