# 🧠 Magic: The Gathering Trivia System

## Overview

The trivia system is an interactive question-and-answer game that tests players' knowledge of Magic: The Gathering. It features competitive gameplay with points, rankings, and comprehensive statistics tracking.

## ✨ Features

### 🎯 Interactive Gameplay
- **Multiple Choice Questions**: Each question has 4 options (A, B, C, D)
- **Reaction-Based Answers**: Players answer by reacting with 🇦, 🇧, 🇨, or 🇩 emojis
- **Exclusive Options**: Each option can only be selected by one player
- **Time Limit**: Games auto-complete after 2 minutes
- **Instant Completion**: Games end immediately when all 4 options are chosen

### 📚 Question Database
- **75+ Questions**: Comprehensive MTG knowledge base
- **Multiple Categories**: Rules, Commander, Cards, Lore, Formats, History
- **Difficulty Levels**: Easy (5-10 pts), Medium (10-15 pts), Hard (15-20 pts), Expert (20-25 pts)
- **Commander Focus**: Special emphasis on Commander format knowledge

### 🏆 Point System & Rankings
- **Points Per Question**: Based on difficulty level
- **Personal Statistics**: Track accuracy, categories, difficulty performance
- **Leaderboard**: Server-wide rankings by total points
- **Achievement Integration**: Works with existing achievement system

### 📊 Statistics Tracking
- **Personal Stats**: Questions answered, accuracy rate, points earned
- **Category Breakdown**: Performance in each knowledge category
- **Difficulty Analysis**: Success rate by question difficulty
- **Last Played**: Track engagement over time

## 🎮 How to Use

### Starting a Trivia Game
```
!trivia
```
- Creates a new trivia question in the channel
- Adds reaction emojis automatically (🇦🇧🇨🇩)
- Shows question, options, points value, and time remaining

### Answering Questions
- **React** with 🇦, 🇧, 🇨, or 🇩 to select your answer
- **One Answer Per Player**: You can only answer once per question
- **Option Locking**: Once chosen, others can't select that option
- **Real-time Updates**: Embed shows locked options and remaining time

### Viewing Statistics
```
!trivia stats
```
Shows your personal trivia performance:
- Total questions answered
- Correct answers and accuracy rate
- Points earned
- Performance by category and difficulty

### Leaderboard
```
!trivia leaderboard
```
Displays server rankings:
- Top 10 players by total points
- Points, accuracy, and questions answered for each player
- Competitive standings

## 📖 Question Categories

### 🏛️ **Rules** (Easy-Medium)
- Basic Magic rules and mechanics
- Deck construction requirements
- Turn structure and game flow
- Keywords and abilities

### ⚔️ **Commander** (Easy-Hard)
- Commander format rules
- Command zone mechanics
- Multiplayer interactions
- Format-specific knowledge

### 🃏 **Cards** (Medium-Expert)
- Famous and powerful cards
- Card interactions
- Banned/restricted lists
- Card knowledge

### 🌍 **Lore** (Medium-Hard)
- Planeswalker stories
- Plane descriptions
- Magic multiverse
- Story elements

### 🎯 **Formats** (Hard-Expert)
- Format legality
- Competitive formats
- Format-specific strategies
- Tournament knowledge

### 📜 **History** (Expert)
- Magic history
- First printings
- Historical significance
- Development stories

### 🎪 **Terminology** (Medium)
- Magic slang and abbreviations
- Community terms
- Technical terminology
- Gameplay expressions

## 🔧 Technical Implementation

### Game Flow
1. **Initialization**: Create game instance with question and timer
2. **Display**: Show question embed with reaction options
3. **Processing**: Handle player reactions and lock options
4. **Completion**: End game when all options taken or timeout
5. **Results**: Display correct answer, winners, and award points
6. **Statistics**: Update player stats and save to file

### Data Storage
- **Trivia Stats**: `trivia_stats.json` - Player statistics and progress
- **Active Games**: In-memory storage during gameplay
- **Question Database**: Hardcoded in `trivia_system.py` for reliability

### Integration Points
- **Command Handlers**: Integrated with existing bot command system
- **Reaction System**: Uses bot's reaction handling framework
- **Discord Embeds**: Consistent with bot's visual style
- **Point System**: Compatible with achievement points (separate tracking)

## 🎯 Difficulty & Points

| Difficulty | Point Range | Description | Examples |
|------------|-------------|-------------|----------|
| **Easy** | 5-10 pts | Basic rules and common knowledge | Deck size, basic colors |
| **Medium** | 10-15 pts | Intermediate concepts | Commander rules, mechanics |
| **Hard** | 15-20 pts | Advanced knowledge | Card interactions, format rules |
| **Expert** | 20-25 pts | Expert-level trivia | History, complex interactions |

## 📈 Statistics Categories

### Overall Performance
- **Total Questions**: Questions answered across all time
- **Correct Answers**: Number of correct responses
- **Accuracy Rate**: Percentage of correct answers
- **Total Points**: Cumulative points earned

### Category Performance
- **Performance by Category**: Accuracy in each knowledge area
- **Category Preferences**: Most answered categories
- **Improvement Tracking**: Progress over time

### Difficulty Analysis
- **Difficulty Breakdown**: Success rate by question difficulty
- **Challenge Progression**: Performance improvement patterns
- **Expertise Areas**: Strongest and weakest difficulty levels

## 🚀 Future Enhancements

### Potential Additions
- **Daily Trivia**: Scheduled daily questions
- **Themed Weeks**: Focus on specific topics (e.g., "Planeswalker Week")
- **Team Trivia**: Multiplayer team-based games
- **Question Submission**: Community-contributed questions
- **Seasonal Events**: Special trivia tournaments
- **Custom Categories**: Server-specific question sets

### Advanced Features
- **Hint System**: Reveal hints for difficult questions
- **Question Explanations**: Educational follow-ups to answers
- **Streak Tracking**: Consecutive correct answer tracking
- **Achievement Integration**: Trivia-specific achievements
- **Cross-Server Competitions**: Multi-server leaderboards

## 🔗 Integration with Existing Systems

### Achievement System
- Compatible with current achievement point tracking
- Separate trivia points for specialized ranking
- Potential for trivia-specific achievements

### Help System
- Integrated into page 4 of help documentation
- Examples and usage instructions included
- Navigation consistent with other features

### Discord Framework
- Uses existing embed color scheme
- Follows established command patterns
- Integrates with reaction handling system

## 📝 Usage Examples

### Basic Gameplay
```
User: !trivia
Bot: [Shows trivia question with A/B/C/D options]
User: [Reacts with 🇦]
Bot: [Updates embed showing User locked option A]
[Other users react with 🇧, 🇨, 🇩]
Bot: [Shows results, correct answer, winners, points awarded]
```

### Statistics Viewing
```
User: !trivia stats
Bot: [Shows detailed statistics embed]
     📊 Trivia Stats for User
     Questions Answered: 25
     Correct Answers: 18
     Accuracy: 72.0%
     Total Points: 280
```

### Leaderboard Competition
```
User: !trivia leaderboard
Bot: [Shows top 10 players]
     🥇 Player1: 1,250 points | 78.5% accuracy
     🥈 Player2: 980 points | 65.2% accuracy
     🥉 Player3: 875 points | 71.1% accuracy
```

---

*The trivia system adds an engaging educational element to your Magic: The Gathering Discord community, encouraging learning while providing competitive gameplay and community interaction!* 🎉
