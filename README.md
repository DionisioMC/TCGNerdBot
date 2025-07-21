# TCGNerdBot

Do you like TCGs? Do you have a Discord server with your friends where you talk about these kinds of things? Then I have the perfect Bot to add to your server! **TCGNerdBot** - your comprehensive Magic: The Gathering collection assistant and Commander game tracker!

This bot helps you and your friends manage your card collections, find card information, analyze set completion, track Commander games, earn achievements, and make informed decisions about your Magic: The Gathering purchases. Whether you're looking for specific cards, checking prices, organizing Commander games, or competing for achievements, TCGNerdBot has you covered!

## 🌟 Current Features

### 🔍 Card Lookup & Information

- **🖼️ Card Images**: Get an image of any Magic: The Gathering card by writing its name inside `[card name]`
- **💰 Price Checking**: Get the current EUR price of a card by adding "price" to your message. Example: `[Sol Ring] price`
- **⚖️ Commander Legality**: Check if a card is legal in Commander format by adding "legal" to your message. Example: `[Mana Crypt] legal`
- **📚 Wiki Integration**: Search the MTG Wiki by writing a keyword inside `{keyword}`

### 🎮 Commander Game Tracking

- **🎯 Game Management**: Create, join, and manage Commander games with unique game IDs
- **👥 Player Tracking**: Support for 2-8 players per game with automatic validation
- **🃏 Commander Selection**: Set your commander with automatic color identity detection via Scryfall API
- **🎨 Archetype System**: Integrated EDHREC API for automatic archetype detection and selection
- **🏆 Placement Tracking**: Interactive emoji-based placement setting system
- **📊 Statistics**: Comprehensive personal statistics including win rates, color preferences, and commander data
- **💾 Data Persistence**: Games saved to JSON for crash recovery, results stored in CSV for analysis

**Commander Commands:**
- `!commander create` - Create a new game
- `!commander join` - Join available games (interactive selection)
- `!commander setcommander <name>` - Set your commander (auto-detects colors & archetype)
- `!commander setplace` - Set your placement using emoji reactions
- `!commander finish <game_id>` - Complete the game and save results
- `!commander stats` - View your personal statistics
- `!commander analytics` - Advanced game analysis and trends
- `!c` - Short alias for all commander commands

### 🏆 Achievement System (102 Achievements)

- **🎖️ Milestone Achievements**: Game count milestones, win achievements, and progress tracking
- **🌈 Color Achievements**: Win with specific color combinations (mono, guild, shard, wedge, WUBRG)
- **🎯 Performance Achievements**: Win streaks, placement-based achievements, consistency tracking
- **🎪 Strategy Achievements**: Archetype mastery (Aggro, Control, Combo, Midrange, Tokens, etc.)
- **🎲 Special Achievements**: Time-based, social, and hidden achievements
- **🔍 Achievement Details**: `!c achievements info <name>` - View detailed achievement information
- **📈 Progress Tracking**: Personal achievement progress with earned dates and server statistics
- **🏅 Leaderboards**: Server-wide achievement leaderboards by points

**Achievement Commands:**
- `!commander achievements` - View your achievements overview
- `!commander achievements check` - Check for new achievements
- `!commander achievements info <name>` - View detailed achievement information
- `!commander leaderboard` - Achievement leaderboard

### 📊 Collection Management & Analysis

- **📤 File Upload Analysis**: Upload a .txt file with your want list (format: `1x Card Name` per line) to see who in your group owns those cards
- **📈 Set Statistics**: Use `!setstats <SET_CODE>` to get comprehensive statistics about any Magic set, including rarity breakdown and color distribution
- **🔍 Personal Collection Comparison**: Use `!compare <SET_CODE>` to see how your collection compares to a specific set
- **📋 Complete Collection Overview**: Use `!compareall` to get a comprehensive overview of your collection across all sets you own cards from

### 🕒 Daily Features

- **🃏 Daily Random Card**: Automatic daily card posting at 10:00 AM with card details and image
- **🎲 Manual Random Card**: Use `!dailycard` or `!randomcard` to get a random card anytime

### 💬 Interactive Help System

- **📖 Paginated Help**: Use `!help`, `!commands`, or `!h` for a comprehensive, navigable help system
- **🔗 Page Navigation**: React with ⬅️ and ➡️ to navigate between help pages
- **📑 Organized Content**: Features organized by category with examples and usage instructions

### 🔧 Advanced Features

- **📊 Commander Analytics**: Advanced statistics, trends analysis, and matchup data
- **🎨 Rich Discord Embeds**: Beautiful, color-coded embeds for all responses
- **⚡ Command Aliases**: Short aliases for frequently used commands (`!c` for `!commander`, `!comp` for `!compare`)
- **🛡️ Error Handling**: User-friendly error messages with helpful suggestions
- **🔄 Real-time Updates**: Live game status updates and interactive elements
- **💾 Data Backup**: Automatic backup systems and crash recovery

## 🚀 Getting Started

### Prerequisites
- Discord bot token and server permissions
- Python 3.7+ with required dependencies

### Setup Instructions

1. **Add the bot to your Discord server** (requires message reading and sending permissions)
2. **Create a `.env` file** in the bot directory with your Discord bot token:

   ```env
   DISCORD_TOKEN=your_bot_token_here
   DISCORD_SERVER=your_server_id_here  # Optional but recommended
   ```

3. **Install required dependencies**:
   ```bash
   pip install discord.py requests python-dotenv beautifulsoup4
   ```

4. **Prepare your collection** (optional): Place your collection CSV file in the `Collections/` directory as `final_collection.csv`

5. **Run the bot**:
   ```bash
   python bot.py
   ```

## 📁 Project Structure

```
TCGNerdBot/
├── tests/              # Test files and validation scripts
├── demos/              # Demo scripts and examples
├── docs/               # Documentation and feature guides
│   ├── features/       # Individual feature documentation
│   └── logs/          # Change logs and development history
├── backup/            # Backup files
├── Collections/       # Collection CSV files
├── bot.py             # Main bot file
├── achievements.py    # Achievement system
├── commander_games.py # Commander game tracking
├── command_handlers.py # Command processing
├── daily_card.py      # Daily card functionality
├── discord_helpers.py # Discord utility functions
├── edhrec_api.py      # EDHREC API integration
├── scryfall_api.py    # Scryfall API integration
└── config.py          # Configuration settings
```

## 📋 Collection File Format

Your collection CSV should include these columns:

- `Name`: Card name
- `Set code`: Magic set code (e.g., "MH3")
- `Set name`: Full set name
- `Rarity`: Card rarity (common, uncommon, rare, mythic)
- `Owner`: Owner's name
- `Quantity`: Number of copies owned

## 🎯 Usage Examples

### Card Information
```
[Sol Ring] price          # Get current price
[Mana Crypt] legal        # Check Commander legality
{flying}                  # Search MTG Wiki for "flying"
```

### Commander Games
```
!c create                 # Create new game
!c join                   # Join available games
!c setcommander Atraxa    # Set your commander
!c setplace               # Set placement with reactions
!c stats                  # View your statistics
```

### Achievements
```
!c achievements           # View your achievements
!c achievements check     # Check for new achievements
!c achievements info first_win  # View achievement details
!c leaderboard           # View server leaderboard
```

### Collection Analysis
```
!setstats MH3            # Modern Horizons 3 statistics
!compare OTJ             # Compare your collection to Outlaws of Thunder Junction
!compareall              # Overview of all your collections
```

## 🔄 Data Sources

- **Scryfall API**: Card data, images, prices, and legality information
- **EDHREC API**: Commander archetype data and popularity statistics
- **MTG Wiki**: Keyword definitions and Magic: The Gathering lore

## 🎉 What's New

### Recent Features (2025)
- ✅ **Achievement Detail Command**: View comprehensive information about specific achievements
- ✅ **Advanced Analytics**: Deep statistical analysis and trend tracking
- ✅ **Archetype Integration**: EDHREC-powered archetype detection and tracking
- ✅ **Interactive Help System**: Paginated, navigable help with emoji reactions
- ✅ **Enhanced Game Management**: Streamlined Commander game creation and management
- ✅ **Organized Project Structure**: Clean folder organization for better maintainability

### Comprehensive Achievement System
The bot now features 102 unique achievements across multiple categories:
- **Performance**: Win streaks, placement records, consistency achievements
- **Strategy**: Master different archetypes and playstyles
- **Collection**: Color combination mastery and commander variety
- **Social**: Community engagement and multiplayer achievements
- **Special**: Hidden achievements and unique accomplishments

## 📈 Future Enhancements

- Enhanced format legality checking for all formats
- Advanced collection analytics and insights
- Trade suggestion system based on collection data
- Price trend tracking and alerts
- Deck building assistance with collection integration
- Tournament bracket management
- Advanced statistics export and visualization

---

**TCGNerdBot** - Making Magic: The Gathering more social, competitive, and fun for Discord communities! 🎮✨

1. Add the bot to your Discord server (requires message reading and sending permissions)
2. Create a `.env` file in the bot directory with your Discord bot token:

   ```env
   DISCORD_TOKEN=your_bot_token_here
   DISCORD_SERVER=your_server_id_here
   ```

   Note: `DISCORD_TOKEN` is required, `DISCORD_SERVER` is optional

3. Install required dependencies (discord.py, requests, python-dotenv, beautifulsoup4)
4. Place your collection CSV file in the `Collections/` directory as `final_collection.csv`
5. Run the bot: `python3 bot.py`

## Collection File Format

Your collection CSV should include these columns:

- `Name`: Card name
- `Set code`: Magic set code (e.g., "MH3")
- `Set name`: Full set name
- `Rarity`: Card rarity (common, uncommon, rare, mythic)
- `Owner`: Owner's name
- `Quantity`: Number of copies owned

## Future Features

- Enhanced format legality checking for all formats
- Advanced collection analytics and insights
- Trade suggestion system
- Price trend tracking
- Deck building assistance
