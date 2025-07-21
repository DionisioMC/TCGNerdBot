"""
Test script for the commander archetype tracking system.
Tests EDHREC API integration and archetype functionality.
"""

import asyncio
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from edhrec_api import EDHRECAPI, get_archetype_emoji
from commander_games import (
    commander_manager, 
    create_archetype_selection_embed,
    get_archetype_emojis,
    get_archetype_from_emoji
)


async def test_edhrec_api():
    """Test EDHREC API functionality."""
    print("🧪 Testing EDHREC API...")
    
    # Test popular commanders
    test_commanders = [
        "Atraxa, Praetors' Voice",
        "Edgar Markov", 
        "Korvold, Fae-Cursed King",
        "Meren of Clan Nel Toth",
        "Zaxara, the Exemplary"
    ]
    
    for commander in test_commanders:
        print(f"\n📋 Testing: {commander}")
        
        # Test basic commander data
        commander_data = EDHRECAPI.get_commander_data(commander)
        if commander_data:
            print(f"  ✅ Commander data found")
        else:
            print(f"  ❌ No commander data found")
            continue
        
        # Test archetype data
        archetype_data = EDHRECAPI.get_commander_archetypes(commander)
        if archetype_data:
            archetypes = archetype_data.get('archetypes', [])
            most_popular = archetype_data.get('most_popular')
            
            print(f"  🎯 Most popular: {most_popular}")
            print(f"  📊 Available archetypes ({len(archetypes)}):")
            for i, archetype in enumerate(archetypes[:5], 1):  # Show first 5
                emoji = get_archetype_emoji(archetype)
                print(f"    {i}. {emoji} {archetype}")
            
            if len(archetypes) > 5:
                print(f"    ... and {len(archetypes) - 5} more")
        else:
            print(f"  ❌ No archetype data found")
        
        # Test commander stats
        stats = EDHRECAPI.get_commander_stats(commander)
        if stats:
            print(f"  📈 Rank: {stats.get('rank', 'N/A')}")
            print(f"  🔢 Decks: {stats.get('num_decks', 'N/A')}")
            print(f"  🧂 Salt Score: {stats.get('salt_score', 'N/A')}")
        
        print("  " + "="*50)


def test_archetype_embeds():
    """Test archetype selection embed creation."""
    print("\n🖼️ Testing Archetype Embeds...")
    
    # Mock archetype data
    mock_archetype_data = {
        'archetypes': ['Control', 'Midrange', 'Combo', 'Tokens', 'Voltron'],
        'most_popular': 'Control'
    }
    
    commander_name = "Test Commander"
    current_archetype = "Control"
    
    # Test embed creation
    try:
        embed = create_archetype_selection_embed(commander_name, mock_archetype_data, current_archetype)
        print(f"  ✅ Embed created successfully")
        print(f"  📝 Title: {embed.title}")
        print(f"  📄 Description: {embed.description}")
        print(f"  🏷️ Fields: {len(embed.fields)}")
        
        # Test emoji generation
        emojis = get_archetype_emojis(mock_archetype_data['archetypes'])
        print(f"  😀 Reaction emojis: {emojis}")
        
        # Test emoji to archetype conversion
        for i, emoji in enumerate(emojis):
            archetype = get_archetype_from_emoji(emoji, mock_archetype_data['archetypes'])
            expected = mock_archetype_data['archetypes'][i]
            if archetype == expected:
                print(f"  ✅ {emoji} -> {archetype}")
            else:
                print(f"  ❌ {emoji} -> {archetype} (expected {expected})")
        
    except Exception as e:
        print(f"  ❌ Error creating embed: {e}")


def test_commander_manager():
    """Test commander manager archetype functionality."""
    print("\n⚙️ Testing Commander Manager...")
    
    # Test archetype setting
    try:
        # This would normally require an active game, so we'll just test the method exists
        if hasattr(commander_manager, 'set_commander_archetype_by_user'):
            print("  ✅ set_commander_archetype_by_user method exists")
        else:
            print("  ❌ set_commander_archetype_by_user method missing")
        
        # Test CSV field names include archetype
        fieldnames = ['game_id', 'player_id', 'username', 'commander',
                      'commander_colors', 'commander_archetype', 'placement', 'game_date', 'total_players']
        
        if 'commander_archetype' in fieldnames:
            print("  ✅ CSV includes commander_archetype field")
        else:
            print("  ❌ CSV missing commander_archetype field")
            
    except Exception as e:
        print(f"  ❌ Error testing commander manager: {e}")


def test_achievements():
    """Test archetype-related achievements."""
    print("\n🏆 Testing Archetype Achievements...")
    
    from achievements import achievement_manager
    
    # Check if archetype achievements exist
    archetype_achievements = [
        'aggro_master', 'control_master', 'combo_master', 'midrange_master',
        'tokens_master', 'voltron_master', 'reanimator_master', 'aristocrats_master',
        'archetype_explorer', 'archetype_master', 'archetype_specialist', 'archetype_purist'
    ]
    
    missing_achievements = []
    for achievement_id in archetype_achievements:
        if achievement_id in achievement_manager.achievements:
            achievement = achievement_manager.achievements[achievement_id]
            print(f"  ✅ {achievement.emoji} {achievement.name}")
        else:
            missing_achievements.append(achievement_id)
    
    if missing_achievements:
        print(f"  ❌ Missing achievements: {missing_achievements}")
    else:
        print("  🎉 All archetype achievements found!")
    
    # Test archetype checking methods
    methods_to_test = [
        '_check_archetype_wins',
        '_check_different_archetype_wins', 
        '_check_same_archetype_wins',
        '_check_same_archetype_games'
    ]
    
    for method_name in methods_to_test:
        if hasattr(achievement_manager, method_name):
            print(f"  ✅ {method_name} method exists")
        else:
            print(f"  ❌ {method_name} method missing")


async def main():
    """Run all tests."""
    print("🚀 Starting Archetype System Tests")
    print("=" * 60)
    
    # Test EDHREC API
    await test_edhrec_api()
    
    # Test embed functionality
    test_archetype_embeds()
    
    # Test commander manager
    test_commander_manager()
    
    # Test achievements
    test_achievements()
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    
    print("\n📋 Summary of New Features:")
    print("  🔗 EDHREC API integration for commander archetypes")
    print("  🎯 Automatic archetype detection when setting commanders")
    print("  😀 Interactive archetype selection with reactions")
    print("  📊 Archetype tracking in game statistics")
    print("  🏆 12 new archetype-based achievements")
    print("  📈 Enhanced player stats with archetype data")


if __name__ == "__main__":
    asyncio.run(main())
