# Commander Game Tracking Feature

## Overview
The Commander Game Tracking feature allows Discord users to track their Magic: The Gathering Commander games, including players, commanders used, final placements, and comprehensive statistics.

## Commands

### Game Management
- `!commander create` - Create a new commander game
- `!commander join` - Join a game (shows available games with reactions)
- `!commander leave` - Leave your current game
- `!commander list` - List active games in the current channel
- `!commander info <game_id>` - Show detailed game information

### Game Setup
- `!commander setcommander <commander_name>` - Set your commander for your active game
- `!commander setplace` - Set your final placement using emoji reactions (no game_id needed)
- `!commander finish <game_id>` - Finish the game and save results (creator only)

### Statistics
- `!commander stats` - View your personal commander game statistics
- `!commander help` - Show detailed help for commander commands

## How to Use

### Starting a Game
1. **Create a game**: Use `!commander create` to start a new game
2. **Share the game ID**: Other players can join using `!commander join`
3. **Players join**: Use `!commander join` to see and select from available games

### During the Game
- Players can set their commander at any time during the game using `!commander setcommander <commander_name>`
- The bot will automatically find your active game - no need to remember game IDs!

### After the Game
1. **Set placements**: Players use `!commander setplace` to get an interactive placement selection
   - React with emoji numbers (1️⃣, 2️⃣, 3️⃣, etc.) to set your placement
   - No need to remember game IDs - automatically finds your active game
   - Shows available placements and which ones are already taken
2. **Finish the game**: The game creator uses `!commander finish <game_id>` to complete the game
3. **Results saved**: Game data is automatically saved for statistics

### Statistics Tracking
The bot tracks comprehensive statistics including:
- Total games played
- Number of wins
- Win rate percentage
- Average placement
- Top 2 and Top 3 finishes
- Number of different commanders played
- Most frequently played commander
- **Color identity statistics:**
  - Individual colors played (White, Blue, Black, Red, Green, Colorless)
  - Color combinations used
  - Most frequently played color combination
  - Mono-color vs multi-color deck preference
  - Visual color representation with emojis

## Features

### Game Validation
- Ensures all players have set their commander before finishing
- Validates that all placements are set and unique
- Prevents duplicate placements
- Supports 2-8 players per game

### Data Persistence
- Games are saved to JSON file for crash recovery
- Final results are saved to CSV for statistics and analysis
- Automatic cleanup of finished games

### Discord Integration
- Rich embeds showing game status and player information
- Real-time updates when players join or set information
- User-friendly error messages and validation

## File Structure
- `commander_games.py` - Main game logic and management
- `commander_games_data.json` - Active games storage
- `commander_stats.csv` - Historical game results for statistics

## Data Storage

### Active Games (JSON)
Stores currently active games with all player information, commanders, and placements.

### Statistics (CSV)
Stores completed game results with columns:
- game_id
- player_id (Discord user ID)
- username
- commander
- commander_colors (comma-separated color identity)
- placement
- game_date
- total_players

This data can be used for advanced statistics, leaderboards, and analysis of playing patterns.

## Example Workflow

```
User1: !commander create
Bot: Commander game game_123456 created! You've been automatically added as a player.

User2: !commander join
Bot: [Shows interactive game selection with emoji reactions]
   🎮 Join Commander Game
   Available Games:
   1️⃣ game_123456 | 👑 Creator: User1 | 👥 1/8 players
   [User clicks 1️⃣ reaction]
Bot: ✅ Successfully joined game game_123456!

User1: !commander setcommander Atraxa, Praetors' Voice
Bot: ✅ Commander set to **Atraxa, Praetors' Voice** ⚪🔵⚫🟢!

User2: !commander setcommander Edgar Markov
Bot: ✅ Commander set to **Edgar Markov** ⚪⚫🔴!

# After the game...
User1: !commander setplace
Bot: [Shows interactive placement selection with emoji reactions]
   🏆 Set Your Placement
   Available: 1️⃣ Winner | 2️⃣ Second | 3️⃣ Third | 4️⃣ Fourth
   [User clicks 1️⃣ reaction]
Bot: ✅ Placement Set! User1 - Placement set to #1!

User2: !commander setplace
Bot: [Shows updated placement selection]
   Available: 2️⃣ Second | 3️⃣ Third | 4️⃣ Fourth
   Already Set: 1️⃣ User1
   [User clicks 2️⃣ reaction]
Bot: ✅ Placement Set! User2 - Placement set to #2!

User1: !commander finish game_123456
Bot: 🏁 Commander Game Finished! [Shows detailed results embed]

User1: !commander stats
Bot: [Shows comprehensive statistics embed with color data]
   📊 Commander Stats for User1
   🎮 Games Played: 5
   🏆 Wins: 2 (40.0%)
   🌈 Colors Played: ⚪🔵⚫🔴🟢 (5 colors)
   🌟 Favorite Colors: ⚫🟢
   🎨 Color Preference: Mono: 1 | Multi: 4
```
