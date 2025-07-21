# Achievement Detail Command

## Overview
Added a new command to view detailed information about specific achievements in the TCG Nerd Bot.

## Command Usage
```
!commander achievements info <achievement_name_or_id>
!c achievements info <achievement_name_or_id>
!c achievements detail <achievement_name_or_id>
!c achievements details <achievement_name_or_id>
```

## Features

### 🔍 Smart Achievement Search
- **ID Match**: Search by exact achievement ID (e.g., `first_win`)
- **Name Match**: Search by exact achievement name (e.g., `Victory Royale`)
- **Partial Match**: Search with partial names (e.g., `legendary` finds `Legendary Streak`)
- **Case Insensitive**: All searches work regardless of capitalization

### 📊 Detailed Information Display
- **Basic Info**: ID, category, rarity, points, hidden status
- **Your Progress**: Whether you've earned it and when
- **Server Statistics**: How many players have earned it and completion rate
- **Visual Indicators**: 
  - ✅ for earned achievements
  - 🔒 for locked achievements
  - Color-coded rarity (common=gray, uncommon=green, rare=blue, epic=purple, legendary=orange)

### 📈 Rarity Analysis
The command shows both the designed rarity and actual completion rate:
- **Very Common**: 75%+ completion rate
- **Common**: 50-75% completion rate  
- **Uncommon**: 25-50% completion rate
- **Rare**: 10-25% completion rate
- **Very Rare**: <10% completion rate

## Examples

### Basic Usage
```
!c achievements info first_win
!c achievements detail Victory Royale
!c achievements info legendary
```

### Error Handling
```
!c achievements info nonexistent
# Response: ❌ Achievement 'nonexistent' not found. Try a different name or ID.
# 💡 Tip: Use `!c achievements` to see all available achievements.
```

## Implementation Details

### New Functions Added
1. `AchievementManager.find_achievement()` - Smart search for achievements
2. `AchievementManager.get_all_achievements_by_category()` - Category grouping
3. `create_achievement_detail_embed()` - Detailed embed creation

### Command Handler Updates
- Added new subcommand handling for "info", "detail", "details"
- Integrated with existing achievement system
- Proper error messages and user guidance

### Help System Updates
- Updated help page 3 to include the new command
- Clear usage examples and descriptions

## Benefits
- **Better Discovery**: Players can easily learn about specific achievements
- **Progress Tracking**: See exactly when you earned achievements
- **Community Insight**: Understand how rare achievements really are
- **Goal Setting**: Know what to work towards with detailed descriptions

This command enhances the achievement system by making it more discoverable and informative for players!
