# Commander Archetype Tracking System

## 🎯 Overview

The Commander Archetype Tracking System adds detailed strategy classification to your Commander games, allowing players to:

- **Automatically detect** the most popular archetype for their commander using EDHREC data
- **Manually select** from available archetypes using interactive Discord reactions
- **Track statistics** by archetype for enhanced analytics
- **Earn achievements** based on archetype mastery and variety

## 🚀 Features Added

### 1. EDHREC API Integration
- Fetches commander data and available archetypes
- Identifies the most popular archetype automatically
- Provides fallback archetypes based on commander colors

### 2. Interactive Archetype Selection
- React with emojis to choose your preferred archetype
- Real-time embed updates showing current selection
- Support for up to 8 different archetypes per commander

### 3. Enhanced Game Tracking
- Archetype data saved in game statistics CSV
- Archetype information displayed in game info embeds
- Historical archetype tracking for trend analysis

### 4. New Achievements (12 total)
- **Archetype Masters** (5): Master specific archetypes (Aggro, Control, Combo, Midrange, Tokens, etc.)
- **Variety Achievements** (2): Play with multiple different archetypes
- **Specialization** (2): Focus on mastering single archetypes
- **Strategy Specific** (3): Win with specialized strategies (Voltron, Reanimator, Aristocrats)

## 📋 How to Use

### Setting a Commander with Archetype
```
!commander setcommander Atraxa, Praetors' Voice
```
1. Bot automatically detects "Control" as the most popular archetype
2. Archetype selection embed appears with available options
3. React with number emojis (1️⃣, 2️⃣, etc.) to change archetype
4. Confirmation message shows your selection

### Changing Archetype Later
```
!commander archetype
```
- Shows current archetype and available alternatives
- Use reactions to select a different archetype
- Works only when you're in an active game

### Viewing Enhanced Statistics
```
!commander stats
```
- Now includes archetype win rates and preferences
- Shows your most successful archetypes
- Tracks archetype diversity

## 🏆 New Achievements

### Archetype Masters (125-150 points each)
- **⚡ Aggro Master**: Win 5 games with Aggro archetype
- **🛡️ Control Master**: Win 5 games with Control archetype  
- **🔄 Combo Master**: Win 5 games with Combo archetype
- **⚖️ Midrange Master**: Win 5 games with Midrange archetype

### Strategy Specialists (75-100 points each)
- **👥 Token Army**: Win 3 games with Tokens archetype
- **🤖 Voltron Pilot**: Win 3 games with Voltron archetype
- **☠️ Death and Taxes**: Win 3 games with Reanimator archetype
- **🎩 Noble Sacrifice**: Win 3 games with Aristocrats archetype

### Variety & Mastery (200-400 points)
- **🗺️ Archetype Explorer**: Win with 5 different archetypes
- **🎓 Master Strategist**: Win with 10 different archetypes
- **🏅 Specialist**: Win 10 games with the same archetype
- **💎 Purist**: Play 25 games with the same archetype

## 🔧 Technical Implementation

### Database Changes
- Added `commander_archetype` field to CSV statistics
- Enhanced JSON game storage for archetype data
- Backward compatibility with existing data

### API Integration
- EDHREC API integration with fallback handling
- Rate limiting and error handling
- Commander name sanitization for API calls

### Discord Integration
- Reaction-based archetype selection
- Rich embed displays with archetype emojis
- Seamless integration with existing commands

## 🎮 Example Workflow

1. **Create Game**: `!commander create`
2. **Set Commander**: `!commander setcommander Meren of Clan Nel Toth`
   - Bot suggests "Reanimator" archetype
   - React to change to "Aristocrats" or "Midrange"
3. **Play Game**: Continue as normal
4. **Track Progress**: View archetype stats and earn achievements
5. **Analytics**: Server analytics now include archetype meta analysis

## 🛠️ Configuration

### Archetype Categories Supported
- **Core Strategies**: Aggro, Control, Combo, Midrange
- **Synergy Based**: Tokens, Tribal, Artifacts, Enchantments
- **Specialized**: Voltron, Reanimator, Aristocrats, Stax
- **Social**: Group Hug, Politics
- **Advanced**: Storm, Lands Matter

### Emoji Mappings
- ⚡ Aggro
- 🛡️ Control  
- 🔄 Combo
- ⚖️ Midrange
- 👥 Tokens
- 🤖 Voltron
- ☠️ Reanimator
- 🎩 Aristocrats
- 🏺 Tribal
- ⚙️ Artifacts
- 🔒 Stax
- 🤗 Group Hug

## 📈 Future Enhancements

### Planned Features
1. **Meta Analysis**: Server-wide archetype win rates and popularity
2. **Matchup Tracking**: Archetype vs archetype statistics  
3. **Seasonal Reports**: Archetype meta shifts over time
4. **Recommendations**: Suggested archetypes based on play style
5. **Tournament Brackets**: Archetype-based tournament categories

### Advanced Analytics
- Archetype performance by table size
- Color combination + archetype success rates
- Player archetype preferences and evolution
- Meta game influence tracking

## 🚨 Notes & Limitations

- EDHREC API has rate limits; fallback archetypes provided
- Archetype detection works best with popular commanders
- Manual archetype selection always available as backup
- Existing games won't have archetype data (starts with new games)

## 🎉 Benefits for Players

1. **Better Self-Understanding**: Track which strategies work best for you
2. **Meta Awareness**: See what archetypes are succeeding on your server
3. **Achievement Goals**: Clear progression paths for strategy mastery
4. **Deck Building**: Data-driven insights for deck selection
5. **Competition**: Compare archetype mastery with other players

This system transforms basic game tracking into rich strategic analytics, helping players improve their gameplay while earning meaningful achievements!
