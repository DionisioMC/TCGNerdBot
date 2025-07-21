# TCG Nerd Bot - Project Structure

This document describes the organized project structure after cleanup and reorganization.

## 📁 Project Structure

```
TCGNerdBot/
├── 📄 bot.py                    # Main bot entry point
├── 📄 config.py                 # Configuration settings
├── 📄 command_handlers.py       # Discord command handlers
├── 📄 commander_games.py        # Commander game management
├── 📄 commander_analytics.py    # Game analytics and achievements
├── 📄 achievements.py           # Achievement system
├── 📄 daily_card.py            # Daily card feature
├── 📄 discord_helpers.py       # Discord utility functions
├── 📄 edhrec_api.py            # EDHREC API integration
├── 📄 request_db.py            # Database requests
├── 📄 scryfall_api.py          # Scryfall API integration
├── 📄 commander_games_data.json # Game data storage
├── 📄 README.md                # Main project documentation
├── 📄 LICENSE                  # Project license
├── 📄 .env                     # Environment variables (not in git)
├── 📄 .gitignore              # Git ignore rules
├── 📄 __init__.py             # Python package marker
│
├── 📁 Collections/             # Card collection data
├── 📁 __pycache__/            # Python cache (auto-generated)
│
├── 📁 tests/                   # All test files
│   ├── test_*.py               # Various test scripts
│   └── simple_test.py          # Simple functionality tests
│
├── 📁 docs/                    # Documentation
│   ├── 📁 features/            # Feature documentation
│   │   ├── ANALYTICS_ACHIEVEMENTS.md
│   │   ├── ARCHETYPE_REACTION_FIX.md
│   │   ├── ARCHETYPE_SYSTEM_GUIDE.md
│   │   ├── COMMAND_ALIASES.md
│   │   ├── COMMANDER_GAME_FEATURE.md
│   │   ├── CSV_COLLECTION_FEATURE.md
│   │   ├── EDHREC_API_IMPROVEMENTS.md
│   │   ├── EDHREC_API_STATUS.md
│   │   ├── FILE_UPLOAD_FIX.md
│   │   ├── PAGINATED_HELP_SYSTEM.md
│   │   └── COMPLEX_ACHIEVEMENTS_GUIDE.md
│   │
│   ├── 📁 logs/                # Development logs and summaries
│   │   ├── ANALYTICS_ACHIEVEMENTS_SUMMARY.md
│   │   ├── API_TEST_CONCLUSION.txt
│   │   ├── COMMANDER_REMOVAL_LOG.md
│   │   ├── COMPLEX_ACHIEVEMENTS_COMPLETE.md
│   │   ├── EDHREC_TEST_RESULTS.txt
│   │   ├── ELVES_TRIBAL_UPDATE.txt
│   │   ├── HELP_UPDATE_SUMMARY.txt
│   │   ├── IMPLEMENTATION_COMPLETE.txt
│   │   └── IMPLEMENTATION_SUMMARY.md
│   │
│   └── README_RESTRUCTURE.md   # Documentation restructure notes
│
└── 📁 backup/                  # Legacy and backup files
    ├── add_owner_column.py     # Legacy utility script
    ├── archetype_reaction_handler.py # Old archetype handler
    ├── bot_original_backup.py  # Original bot backup
    ├── colection_merge.py      # Legacy collection merge
    ├── debug_file.py           # Debug utilities
    └── edhrec_api_new.py       # Old EDHREC API version
```

## 🚀 Core Components

### Main Application Files
- **bot.py**: Discord bot main entry point and event handlers
- **command_handlers.py**: All Discord command processing logic
- **commander_games.py**: Commander game state management and logic
- **commander_analytics.py**: Game analytics, statistics, and achievements
- **achievements.py**: Achievement system implementation

### API Integrations
- **edhrec_api.py**: EDHREC data fetching with Tags-based archetype extraction
- **scryfall_api.py**: Scryfall API for card data and images
- **discord_helpers.py**: Discord-specific utility functions

### Configuration & Data
- **config.py**: Bot configuration and settings
- **commander_games_data.json**: Persistent game data storage
- **Collections/**: User card collection data

## 🧪 Testing

All test files are organized in the `tests/` folder:
- Integration tests for major features
- Unit tests for specific components
- API testing scripts
- Functionality validation tests

## 📚 Documentation

Documentation is organized in the `docs/` folder:

### Features (`docs/features/`)
- Feature implementation guides
- API improvement documentation
- System architecture descriptions
- User guides and command references

### Logs (`docs/logs/`)
- Development progress logs
- Implementation summaries
- Test results and conclusions
- Change logs and updates

## 🗄️ Backup Files

Legacy code and backup files are stored in `backup/`:
- Original bot implementations
- Deprecated utility scripts
- Old API versions
- Debug files

## 🔧 Development Workflow

1. **Main Development**: Work in root directory with core files
2. **Testing**: Use files in `tests/` directory for validation
3. **Documentation**: Update relevant files in `docs/` as features are added
4. **Backup**: Move deprecated files to `backup/` to maintain clean structure

## 📖 Key Features

- 🎯 Commander game tracking with analytics
- 🏆 Achievement system with complex unlocks
- 🔍 EDHREC integration with Tags-based archetypes
- 📊 Collection management and comparison
- 🎴 Daily random card feature
- 📝 Paginated help system
- ⚡ Command aliases for improved UX

This organized structure improves maintainability, makes testing easier, and provides clear separation between active code, documentation, and legacy files.
