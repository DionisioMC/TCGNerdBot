"""
Discord helper functions for the TCG Nerd Bot.
Contains functions for creating embeds and formatting Discord messages.
"""

import discord
from typing import Dict, Any, List
from config import RARITY_EMOJIS, COLOR_EMOJIS, EMBED_COLORS, MAX_MESSAGE_LENGTH


def create_daily_card_embed(card_data: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for the daily random card.
    
    Args:
        card_data: Card data from Scryfall API.
        
    Returns:
        Discord embed object.
    """
    embed = discord.Embed(
        title="🌟 Daily Random Card",
        color=EMBED_COLORS['daily_card'],
        description="Here's today's random Magic card!"
    )
    
    # Card basic info
    embed.add_field(
        name="📜 Card Name",
        value=f"**{card_data.get('name', 'Unknown')}**",
        inline=True
    )
    
    embed.add_field(
        name="💎 Mana Cost",
        value=card_data.get('mana_cost', 'N/A'),
        inline=True
    )
    
    embed.add_field(
        name="🎴 Type",
        value=card_data.get('type_line', 'Unknown'),
        inline=True
    )
    
    # Set info
    set_name = card_data.get('set_name', 'Unknown Set')
    set_code = card_data.get('set', 'N/A').upper()
    embed.add_field(
        name="📦 Set",
        value=f"{set_name} ({set_code})",
        inline=True
    )
    
    # Rarity with emoji
    rarity = card_data.get('rarity', 'common').lower()
    rarity_emoji = RARITY_EMOJIS.get(rarity, '❓')
    embed.add_field(
        name="💫 Rarity",
        value=f"{rarity_emoji} {rarity.capitalize()}",
        inline=True
    )
    
    # Oracle text (truncated if too long)
    oracle_text = card_data.get('oracle_text', '')
    if oracle_text:
        if len(oracle_text) > 300:
            oracle_text = oracle_text[:297] + "..."
        embed.add_field(
            name="📖 Oracle Text",
            value=oracle_text,
            inline=False
        )
    
    # Add card image
    image_uris = card_data.get('image_uris', {})
    if image_uris:
        embed.set_image(url=image_uris.get('normal', image_uris.get('large', '')))
    
    # Add Scryfall link
    scryfall_uri = card_data.get('scryfall_uri', '')
    if scryfall_uri:
        embed.add_field(
            name="🔗 More Info",
            value=f"[View on Scryfall]({scryfall_uri})",
            inline=False
        )
    
    embed.set_footer(text="Daily card updates at 10:00 AM • Powered by Scryfall")
    
    return embed


def create_set_stats_embed(stats: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for set statistics.
    
    Args:
        stats: Set statistics data.
        
    Returns:
        Discord embed object.
    """
    embed = discord.Embed(
        title=f"📊 Set Statistics: {stats['set_info']['name']}",
        color=EMBED_COLORS['set_stats']
    )
    
    embed.add_field(
        name="📅 Basic Info",
        value=f"**Code:** {stats['set_info']['code']}\n**Release:** {stats['set_info']['release_date']}\n**Total Cards:** {stats['set_info']['total_cards']}",
        inline=True
    )

    # Rarity breakdown
    rarity_text = ""
    for rarity, count in stats['rarity_breakdown'].items():
        if count > 0:
            percentage = (count / stats['set_info']['total_cards']) * 100
            rarity_text += f"**{rarity.capitalize()}:** {count} ({percentage:.1f}%)\n"

    embed.add_field(name="🎴 Rarity Breakdown", value=rarity_text, inline=True)

    # Color breakdown
    color_text = ""
    
    for color, count in stats['color_breakdown'].items():
        if count > 0:
            percentage = (count / stats['set_info']['total_cards']) * 100
            emoji = COLOR_EMOJIS.get(color, '🎨')
            color_text += f"{emoji} **{color.capitalize()}:** {count} ({percentage:.1f}%)\n"

    embed.add_field(name="🎨 Color Distribution", value=color_text, inline=False)
    
    return embed


def create_collection_overview_embed(username: str, comparisons: List[Dict[str, Any]]) -> discord.Embed:
    """
    Create a Discord embed for collection overview.
    
    Args:
        username: The username of the requester.
        comparisons: List of set comparison results.
        
    Returns:
        Discord embed object.
    """
    embed = discord.Embed(
        title=f"📊 Collection Overview for {username}",
        color=EMBED_COLORS['collection_overview'],
        description=f"Your top collection sets (showing up to {len(comparisons)} sets)"
    )

    # Show top 10 sets by completion
    top_sets = comparisons[:10]

    completion_text = ""
    for i, comp in enumerate(top_sets, 1):
        # Add completion emoji
        if comp['completion_percentage'] >= 50:
            emoji = "🎯"
        elif comp['completion_percentage'] >= 25:
            emoji = "📈"
        elif comp['completion_percentage'] >= 10:
            emoji = "📊"
        else:
            emoji = "📋"

        completion_text += f"{emoji} **{comp['set_name']} ({comp['set_code']})**\n"
        completion_text += f"└ {comp['your_total']}/{comp['set_total']} cards ({comp['completion_percentage']:.1f}%)\n\n"

    embed.add_field(
        name="🏆 Top Sets by Completion",
        value=completion_text[:1000] + ("..." if len(completion_text) > 1000 else ""),
        inline=False
    )

    # Calculate overall stats
    total_owned = sum(comp['your_total'] for comp in comparisons)
    total_possible = sum(comp['set_total'] for comp in comparisons)
    overall_completion = (total_owned / total_possible * 100) if total_possible > 0 else 0

    embed.add_field(
        name="📈 Overall Statistics",
        value=f"**Total Cards:** {total_owned:,}\n**Overall Completion:** {overall_completion:.1f}%\n**Sets with 50%+ completion:** {len([c for c in comparisons if c['completion_percentage'] >= 50])}",
        inline=True
    )

    embed.add_field(
        name="💡 Quick Actions",
        value="Use `!compare <SET>` for detailed set analysis",
        inline=True
    )
    
    return embed


def create_collection_comparison_embed(set_code: str, comparison: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for collection comparison.
    
    Args:
        set_code: The set code being compared.
        comparison: Comparison result data.
        
    Returns:
        Discord embed object.
    """
    embed = discord.Embed(
        title=f"🔍 Collection Comparison: {set_code}",
        color=EMBED_COLORS['comparison'],
        description=f"**Your** progress: **{comparison['your_total']} / {comparison['set_total']} cards ({comparison['completion_percentage']:.1f}% complete)**"
    )

    # Rarity completion
    rarity_text = ""
    for rarity, count in comparison['your_rarity_breakdown'].items():
        if count > 0:
            rarity_text += f"**{rarity.capitalize()}:** {count} cards\n"

    embed.add_field(
        name="🎴 Collection by Rarity",
        value=rarity_text or "No cards found", 
        inline=True
    )
    
    embed.add_field(
        name="💡 Tip", 
        value="Use `!compareall` to see your collection overview!", 
        inline=False
    )
    
    return embed


def create_help_embed() -> discord.Embed:
    """
    Create a Discord embed for the help command - Page 1 (Basic Commands).
    
    Returns:
        Discord embed object.
    """
    return create_help_embed_page(1)


def create_help_embed_page(page: int) -> discord.Embed:
    """
    Create a paginated Discord embed for the help command.
    
    Args:
        page: Page number (1-4)
        
    Returns:
        Discord embed object.
    """
    if page == 1:
        return _create_help_page_1()
    elif page == 2:
        return _create_help_page_2()
    elif page == 3:
        return _create_help_page_3()
    elif page == 4:
        return _create_help_page_4()
    else:
        return _create_help_page_1()  # Default to page 1


def _create_help_page_1() -> discord.Embed:
    """Create help page 1: Basic Commands & Quick Start."""
    embed = discord.Embed(
        title="🤖 TCG Nerd Bot Commands - Page 1/4",
        color=EMBED_COLORS['help'],
        description="Your Magic: The Gathering collection assistant! 🎯\n\n⚡ **Quick Aliases:** `!h` = help • `!c` = commander • `!comp` = compare"
    )

    embed.add_field(
        name="🔍 Card & Wiki Lookup",
        value=(
            "`[card name]` - Show card image\n"
            "`[card name] price` - Show EUR price\n"
            "`{keyword}` - Search MTG Wiki"
        ),
        inline=False
    )

    embed.add_field(
        name="📊 Collection Analysis",
        value=(
            "`!setstats <SET>` - Get set statistics\n"
            "`!compare <SET>` or `!comp <SET>` - Compare collection to set\n"
            "`!compareall` - Compare your top collection sets"
        ),
        inline=False
    )

    embed.add_field(
        name="🌟 Daily Features",
        value=(
            "`!dailycard` or `!randomcard` - Get a random MTG card\n"
            "🕙 **Auto daily cards at 10:00 AM**"
        ),
        inline=False
    )

    embed.add_field(
        name="📁 File Upload",
        value=(
            "**Upload .txt file** - Check who owns cards from your want list\n"
            "**Format:** `1x Card Name` per line\n"
            "**Upload CSV + `!upload`** - Update your collection"
        ),
        inline=False
    )

    embed.add_field(
        name="📖 Navigation",
        value="🔹 Page 2: Commander Games • 🔹 Page 3: Archetype System • 🔹 Page 4: Examples\n\n**Use ⬅️ ➡️ reactions to navigate pages**",
        inline=False
    )
    
    return embed


def _create_help_page_2() -> discord.Embed:
    """Create help page 2: Commander Game Management."""
    embed = discord.Embed(
        title="🎯 Commander Game Commands - Page 2/4",
        color=EMBED_COLORS['help'],
        description="Track your Magic: The Gathering Commander games with **simplified commands**!"
    )
    
    embed.add_field(
        name="⚡ Quick Aliases",
        value=(
            "`!c` = `!commander` (main command)\n"
            "`!c c` = `!commander create`\n"
            "`!c j` = `!commander join`\n"
            "`!c l` = `!commander leave`\n"
            "`!c s` = `!commander start`\n"
            "`!c e` = `!commander end`\n"
            "`!c st` = `!commander stats`"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎮 Game Management",
        value=(
            "`!commander create` - Create a new game\n"
            "`!commander join` - Join a game (interactive selection) 🆕\n"
            "`!commander leave` - Leave your current game (auto-finds) 🆕\n"
            "`!commander list` - List active games in this channel\n"
            "`!commander info <game_id>` - Show game details"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Game Setup",
        value=(
            "`!commander setcommander <name>` - Set commander with archetype 🆕\n"
            "`!commander archetype` - Change your commander's archetype 🆕\n"
            "`!commander setplace` - Set placement with emoji reactions 🆕\n"
            "`!commander finish <game_id>` - Finish the game (creator only)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Statistics & Analytics",
        value=(
            "`!commander stats` - View your game statistics & archetype data 🆕\n"
            "`!commander meta [days]` - Server meta analysis 🆕\n"
            "`!commander trends [days]` - Your performance trends 🆕"
        ),
        inline=False
    )

    embed.add_field(
        name="📖 Navigation",
        value="🔹 Page 1: Basic Commands • 🔹 Page 3: Archetype System • 🔹 Page 4: Examples\n\n**Use ⬅️ ➡️ reactions to navigate pages**",
        inline=False
    )
    
    return embed


def _create_help_page_3() -> discord.Embed:
    """Create help page 3: Archetype System & Achievements."""
    embed = discord.Embed(
        title="🏆 Archetype System & Achievements - Page 3/4",
        color=EMBED_COLORS['help'],
        description="New archetype tracking system with interactive selection and achievements! 🎯"
    )

    embed.add_field(
        name="� Archetype System",
        value=(
            "🎯 **Automatic Commander Archetype Detection**\n"
            "• Set commander → Select archetype with emoji reactions\n"
            "• ⚡ Aggro, 🛡️ Control, 🔄 Combo, ⚖️ Midrange, 👥 Tokens, 🤖 Voltron, and more!\n"
            "• Uses EDHREC API for intelligent suggestions\n"
            "• Fallback system when API is rate-limited"
        ),
        inline=False
    )

    embed.add_field(
        name="🏆 Achievement System",
        value=(
            "`!commander achievements` - View your achievements 🆕\n"
            "`!commander achievements check` - Check for new achievements 🆕\n"
            "`!commander leaderboard` - Achievement leaderboard 🆕"
        ),
        inline=False
    )

    embed.add_field(
        name="🎖️ Archetype Achievements",
        value=(
            "**12 New Archetype-Based Achievements:**\n"
            "• Master specific strategies (5+ wins with archetype)\n"
            "• Explore different playstyles (try multiple archetypes)\n"
            "• Track progression and earn leaderboard points\n"
            "• Special achievements for versatility and dominance"
        ),
        inline=False
    )

    embed.add_field(
        name="📊 Enhanced Statistics",
        value=(
            "• Win rates by archetype\n"
            "• Meta analysis with archetype trends\n"
            "• Personal performance tracking\n"
            "• Server-wide archetype popularity"
        ),
        inline=False
    )

    embed.add_field(
        name="📖 Navigation",
        value="🔹 Page 1: Basic Commands • 🔹 Page 2: Commander Games • 🔹 Page 4: Examples\n\n**Use ⬅️ ➡️ reactions to navigate pages**",
        inline=False
    )
    
    return embed


def _create_help_page_4() -> discord.Embed:
    """Create help page 4: Examples & Quick Reference."""
    embed = discord.Embed(
        title="🎯 Examples & Quick Reference - Page 4/4",
        color=EMBED_COLORS['help'],
        description="Practical examples to get you started quickly! 🚀"
    )

    embed.add_field(
        name="🔍 Card & Collection Examples",
        value=(
            "**Collection:** `!setstats MH3` • `!comp OTJ` • `!compareall`\n"
            "**Cards:** `[Lightning Bolt]` • `[Mana Crypt] price` • `!dailycard`\n"
            "**Wiki:** `{planeswalker}` • `{cascade}` • `{commander damage}`"
        ),
        inline=False
    )

    embed.add_field(
        name="🎯 Commander Game Examples",
        value=(
            "**Quick Commands:**\n"
            "`!c c` → Create game • `!c j` → Join game • `!c st` → View stats\n\n"
            "**Full Commands:**\n"
            "`!commander create` → Start new game\n"
            "`!commander setcommander Atraxa` → Set commander with archetype selection 🆕\n"
            "`!commander join` → Interactive game selection with reactions 🆕"
        ),
        inline=False
    )

    embed.add_field(
        name="🏆 Archetype & Achievement Examples",
        value=(
            "**Archetype Selection:** Choose ⚡ Aggro, 🛡️ Control, 🔄 Combo with reactions 🆕\n"
            "**Achievements:** `!commander achievements` • `!commander leaderboard` 🆕\n"
            "**Analytics:** `!commander meta 7` → Last 7 days meta analysis 🆕"
        ),
        inline=False
    )

    embed.add_field(
        name="� File Upload Examples",
        value=(
            "**Want List (📎 .txt file):**\n"
            "```\n1x Lightning Bolt\n2x Counterspell\n1x Sol Ring\n```\n"
            "**Collection Update:** Upload CSV + `!upload` command"
        ),
        inline=False
    )

    embed.add_field(
        name="📖 Navigation",
        value="🔹 Page 1: Basic Commands • 🔹 Page 2: Commander Games • 🔹 Page 3: Archetype System\n\n**Use ⬅️ ➡️ reactions to navigate pages**",
        inline=False
    )
    
    return embed


def split_message_into_chunks(message: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
    """
    Split a long message into chunks for Discord's character limit.
    
    Args:
        message: The message to split.
        max_length: Maximum length per chunk.
        
    Returns:
        List of message chunks.
    """
    if len(message) <= max_length:
        return [message]
    
    chunks = []
    for i in range(0, len(message), max_length):
        chunks.append(message[i:i+max_length])
    
    return chunks
