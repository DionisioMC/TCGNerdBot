# TCGNerdBot Command Aliases

## Main Command Aliases
- `!c` → `!commander` (Main commander game command)
- `!comp` → `!compare` (Compare collections)
- `!h` → `!help` (Show help)

## Commander Subcommand Aliases
- `!c c` → `!commander create` (Create new game)
- `!c j` → `!commander join` (Join game)
- `!c l` → `!commander leave` (Leave game)
- `!c s` → `!commander start` (Start game)
- `!c r` → `!commander remove` (Remove player)
- `!c e` → `!commander end` (End game)
- `!c st` → `!commander stats` (View stats)
- `!c g` → `!commander games` (List games)

## Examples
```
# Old way:
!commander create
!commander join A1
!commander setcommander "Atraxa, Praetors' Voice"
!commander stats

# New way with aliases:
!c c
!c j
!c setcommander "Atraxa, Praetors' Voice"
!c st
```

## Game ID Format
Game IDs are now simplified:
- Old: `game_1704067200_123456789`
- New: `A1`, `B2`, `C3`, etc.

## Features Enhanced with Aliases
1. **EDHREC Archetype Integration** - Interactive archetype selection with emoji reactions
2. **Achievement System** - 12 new archetype-based achievements
3. **Simplified Commands** - Quick aliases for all major functions
4. **Auto-Detection** - Many commands now auto-find your active game
5. **Interactive UI** - Emoji-based selections for better UX
