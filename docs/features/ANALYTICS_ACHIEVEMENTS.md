# 📊 Commander Game Analytics & Achievements

This document covers the advanced analytics and achievement system features added to the TCG Nerd Bot.

## 🎯 **Analytics Features**

### Server Meta Analysis
- **Command:** `!commander meta [days]`
- **Description:** Provides comprehensive analysis of commander popularity, color trends, and win rates
- **Features:**
  - Most popular commanders
  - Color popularity statistics  
  - Meta tier list (win rates)
  - Server activity metrics
  - Average game size analysis
  - Most active players

### Personal Trends
- **Command:** `!commander trends [days]`
- **Description:** Analyzes your personal performance and preferences over time
- **Features:**
  - Performance improvement trends
  - Current win/loss streaks
  - Favorite color combinations
  - Recent game history
  - Weekly activity patterns
  - Commander success rates

### Matchup Analysis
- **Available in code:** Analyze head-to-head commander matchups
- **Features:**
  - Win rates between specific commanders
  - Game history for matchups
  - Sample size tracking

## 🏆 **Achievement System**

### Achievement Categories

#### 🎮 Milestone Achievements
- **First Blood** - Play your first commander game (5 pts)
- **Victory Royale** - Win your first commander game (15 pts)
- **Getting Started** - Play 5 games (25 pts)
- **Regular Player** - Play 10 games (50 pts)
- **Dedicated Gamer** - Play 25 games (100 pts)
- **Commander Veteran** - Play 50 games (200 pts)
- **Century Club** - Play 100 games (500 pts)

#### 🏆 Performance Achievements
- **Rising Star** - Win 5 games (75 pts)
- **Champion** - Win 10 games (150 pts)
- **Commander Master** - Win 25 games (400 pts)
- **Hot Streak** - Win 3 games in a row (100 pts)
- **Unstoppable** - Win 5 games in a row (250 pts)
- **Consistent Player** - Top 3 finish 5 times in a row (200 pts)
- **Dominant Force** - Maintain 50%+ win rate over 20+ games (400 pts)
- **Getting Better** - Improve average placement by 1.5+ over 10 games (150 pts)

#### 🌈 Color Achievements
- **Law and Order** - Win with mono-white (30 pts)
- **Master of Mind** - Win with mono-blue (30 pts)
- **Dark Arts** - Win with mono-black (30 pts)
- **Chaos Theory** - Win with mono-red (30 pts)
- **Nature's Fury** - Win with mono-green (30 pts)
- **Rainbow Warrior** - Win with all five mono-colors (300 pts)
- **WUBRG Master** - Win with five-color commander (150 pts)
- **Eldrazi Overlord** - Win with colorless commander (125 pts)

#### 🎭 Variety Achievements
- **Versatile Player** - Play 10 different commanders (100 pts)
- **Commander Collector** - Play 25 different commanders (250 pts)

#### 🤝 Social Achievements
- **Social Butterfly** - Play with 5 different players (100 pts)
- **Community Leader** - Play with 10 different players (200 pts)

#### ⭐ Special Achievements
- **Speed Demon** - Play 5 games in one day (150 pts)
- **Night Owl** - Play between midnight and 6 AM (75 pts)
- **Early Bird** - Play between 6 AM and 9 AM (75 pts)
- **Comeback King** - Win after being in last place (200 pts, hidden)

### Achievement Commands

#### View Achievements
```
!commander achievements
```
Shows your achievement overview with progress and categories.

#### Check for New Achievements
```
!commander achievements check
```
Manually checks for newly earned achievements and displays them.

#### Leaderboard
```
!commander leaderboard
```
Shows the top 10 players by achievement points.

### Achievement Rarity System

- **Common** (🔵) - Basic achievements, 5-50 points
- **Uncommon** (🟢) - Moderate difficulty, 75-150 points  
- **Rare** (🟦) - Challenging achievements, 125-250 points
- **Epic** (🟣) - Very difficult, 300-500 points
- **Legendary** (🟠) - Ultimate achievements, 500+ points

## 🔧 **Technical Implementation**

### Data Storage
- **Analytics:** Uses existing `commander_stats.csv` file
- **Achievements:** Creates new `player_achievements.json` file
- **Automatic processing:** Achievements checked after each game completion

### Performance Considerations
- Analytics queries can be limited by days parameter (1-365)
- Achievement checking is automatic but non-blocking
- Leaderboard shows top 10 players by default

### Integration Points
- **Game completion:** Automatic achievement checking
- **Statistics:** Enhanced with trend analysis
- **Embeddings:** Rich Discord embeds for all features

## 📈 **Usage Examples**

### Checking Server Meta
```
!commander meta           # Last 30 days
!commander meta 7         # Last 7 days
!commander meta 90        # Last 90 days
```

### Personal Analysis
```
!commander trends         # Your trends (30 days)
!commander trends 14      # Your trends (14 days)
!commander achievements   # Your achievement overview
```

### Competitive Features
```
!commander leaderboard    # Top achievement earners
!commander meta           # See what's winning
!commander stats          # Your personal stats
```

## 🎯 **Achievement Strategy Tips**

1. **Play Regularly** - Many achievements reward consistency
2. **Try Different Commanders** - Variety achievements offer good points
3. **Win with Different Colors** - Color achievements provide steady progress
4. **Play with Others** - Social achievements encourage community building
5. **Track Your Progress** - Use `!commander achievements check` regularly

## 🔮 **Future Enhancements**

Potential additions could include:
- Seasonal achievements
- Tournament-specific achievements
- Cross-server leaderboards
- Achievement notifications in Discord
- Weekly/monthly achievement spotlights
- Achievement-based rewards or titles

---

*This system significantly enhances player engagement through detailed statistics tracking and a comprehensive achievement system that rewards various playstyles and accomplishments.*
