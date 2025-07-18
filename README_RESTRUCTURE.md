# TCG Nerd Bot - Code Restructure Documentation

## Overview

The TCG Nerd Bot codebase has been restructured for better maintainability, readability, and modularity. The original monolithic `bot.py` file has been split into several focused modules.

## New File Structure

```
TCGNerdBot/
├── bot.py                    # Main bot entry point (clean and minimal)
├── bot_original_backup.py    # Backup of original bot.py
├── config.py                 # Configuration constants and settings
├── scryfall_api.py          # Scryfall API interactions
├── discord_helpers.py       # Discord embed creation and formatting
├── daily_card.py            # Daily card scheduling and posting
├── command_handlers.py      # Command processing logic
├── __init__.py              # Package initialization
├── request_db.py            # Database/collection functions (existing)
└── Collections/
    └── final_collection.csv  # Card collection data
```

## Module Breakdown

### 🎯 `bot.py` - Main Entry Point
- **Purpose**: Clean main bot file with minimal code
- **Responsibilities**: 
  - Discord client setup
  - Event handling (`on_ready`, `on_message`)
  - Command routing to appropriate handlers
- **Lines of Code**: ~100 (down from ~600+)

### ⚙️ `config.py` - Configuration Management
- **Purpose**: Centralized configuration and constants
- **Contains**:
  - Environment variable loading
  - API settings and timeouts
  - Discord embed colors
  - Channel preferences
  - File paths
  - Emoji mappings

### 🔌 `scryfall_api.py` - API Interactions
- **Purpose**: Handle all Scryfall API communication
- **Key Features**:
  - `ScryfallAPI` class with static methods
  - Error handling for API requests
  - Helper functions for data extraction
- **Functions**:
  - `get_random_card()`
  - `get_card_by_name()`
  - `get_card_price_eur()`
  - `get_commander_legality()`
  - `get_card_image_url()`

### 🎨 `discord_helpers.py` - Embed Creation
- **Purpose**: Create beautiful Discord embeds
- **Key Features**:
  - Consistent styling across all embeds
  - Reusable embed creation functions
  - Message chunking for Discord limits
- **Functions**:
  - `create_daily_card_embed()`
  - `create_set_stats_embed()`
  - `create_commander_recommendations_embed()`
  - `create_collection_overview_embed()`
  - `create_collection_comparison_embed()`
  - `create_help_embed()`
  - `split_message_into_chunks()`

### 📅 `daily_card.py` - Daily Card Feature
- **Purpose**: Handle daily card scheduling and posting
- **Key Features**:
  - Background task scheduling
  - Smart channel selection
  - Configuration-driven timing
- **Functions**:
  - `post_daily_card()`
  - `daily_card_task()`

### 🎮 `command_handlers.py` - Command Processing
- **Purpose**: Process and handle all bot commands
- **Key Features**:
  - `CommandHandlers` class with organized methods
  - Consistent error handling
  - Separation of command logic from Discord events
- **Command Methods**:
  - `handle_card_lookup()`
  - `handle_wiki_lookup()`
  - `handle_file_upload()`
  - `handle_setstats_command()`
  - `handle_commander_command()`
  - `handle_compareall_command()`
  - `handle_compare_command()`
  - `handle_dailycard_command()`
  - `handle_help_command()`
  - `handle_mention()`

## Benefits of Restructuring

### ✅ **Improved Maintainability**
- Each module has a single responsibility
- Easy to locate and fix bugs
- Modular testing possible

### ✅ **Better Readability**
- Shorter, focused files
- Clear separation of concerns
- Self-documenting code structure

### ✅ **Enhanced Scalability**
- Easy to add new commands
- Simple to extend API functionality
- Configurable settings in one place

### ✅ **Error Isolation**
- Issues in one module don't affect others
- Easier debugging and testing
- Better error handling per module

### ✅ **Code Reusability**
- Embed functions can be reused
- API methods are modular
- Helper functions are accessible

## Configuration Highlights

### Environment Variables
```python
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER = os.getenv('DISCORD_SERVER')
```

### Customizable Settings
```python
DAILY_CARD_TIME_HOUR = 10  # 10 AM
PREFERRED_CHANNEL_NAMES = ['general', 'chat', 'main', 'cards', 'daily']
MAX_MESSAGE_LENGTH = 1900
```

### Color Schemes
```python
EMBED_COLORS = {
    'daily_card': 0xffd700,
    'set_stats': 0x00ff00,
    'commander': 0x9932cc,
    # ... more colors
}
```

## Usage

The bot works exactly the same as before from a user perspective. All commands and functionality remain unchanged:

- `[card name]` - Card lookup
- `{keyword}` - Wiki search
- `!setstats <SET>` - Set statistics
- `!commander` - Commander recommendations
- `!compareall` - Collection overview
- `!compare <SET>` - Set comparison
- `!dailycard` - Manual random card
- `!help` - Help command
- File uploads for card checking

## Migration Notes

1. **Backup Created**: `bot_original_backup.py` contains the original code
2. **No Breaking Changes**: All functionality preserved
3. **Easy Rollback**: Can revert by copying backup over `bot.py`
4. **Environment Variables**: Same `.env` file structure required

## Future Enhancements

With this modular structure, future improvements can be easily added:

- **New APIs**: Add modules for other card databases
- **Database Integration**: Replace CSV with proper database
- **Web Dashboard**: Add web interface modules
- **Analytics**: Add statistics and tracking modules
- **Testing**: Add unit tests per module
- **Caching**: Add caching layer for API responses

## Development Workflow

1. **Adding Commands**: Add handler method to `CommandHandlers` class
2. **New Embeds**: Create function in `discord_helpers.py`
3. **API Features**: Extend `ScryfallAPI` class
4. **Configuration**: Add settings to `config.py`
5. **Daily Features**: Modify `daily_card.py`

This restructure provides a solid foundation for continued development while maintaining all existing functionality.
