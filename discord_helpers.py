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
        embed.set_image(url=image_uris.get(
            'normal', image_uris.get('large', '')))

    # Add Scryfall link
    scryfall_uri = card_data.get('scryfall_uri', '')
    if scryfall_uri:
        embed.add_field(
            name="🔗 More Info",
            value=f"[View on Scryfall]({scryfall_uri})",
            inline=False
        )

    embed.set_footer(
        text="Daily card updates at 10:00 AM • Powered by Scryfall")

    return embed


def create_set_stats_embed(stats: Dict[str, Any]) -> discord.Embed:
    """
    Create a Discord embed for set statistics.

    Args:
        stats: Set statistics data (supports both full API format and simplified format).

    Returns:
        Discord embed object.
    """
    # Handle both full API format and simplified test format
    if 'set_info' in stats:
        # Full API format
        set_name = stats['set_info']['name']
        set_code = stats['set_info']['code']
        release_date = stats['set_info'].get('release_date', 'Unknown')
        total_cards = stats['set_info']['total_cards']
        rarity_breakdown = stats.get('rarity_breakdown', {})
        color_breakdown = stats.get('color_breakdown', {})
    else:
        # Simplified format for testing
        set_name = stats.get('set_name', 'Unknown Set')
        set_code = stats.get('set_code', 'UNK')
        release_date = stats.get('release_date', 'Unknown')
        total_cards = stats.get('total_cards', 0)

        # Build rarity breakdown from individual counts
        rarity_breakdown = {}
        for rarity in ['mythic', 'rare', 'uncommon', 'common']:
            count_key = f'{rarity}_count'
            if count_key in stats:
                rarity_breakdown[rarity] = stats[count_key]

        color_breakdown = stats.get('color_breakdown', {})

    embed = discord.Embed(
        title=f"📊 Set Statistics: {set_name}",
        color=EMBED_COLORS['set_stats']
    )

    embed.add_field(
        name="📅 Basic Info",
        value=f"**Code:** {set_code}\n**Release:** {release_date}\n**Total Cards:** {total_cards}",
        inline=True
    )

    # Rarity breakdown
    if rarity_breakdown:
        rarity_text = ""
        for rarity, count in rarity_breakdown.items():
            if count > 0:
                percentage = (count / total_cards *
                              100) if total_cards > 0 else 0
                rarity_text += f"**{rarity.capitalize()}:** {count} ({percentage:.1f}%)\n"

        if rarity_text:
            embed.add_field(name="🎴 Rarity Breakdown",
                            value=rarity_text, inline=True)

    # Color breakdown
    if color_breakdown:
        color_text = ""
        for color, count in color_breakdown.items():
            if count > 0:
                percentage = (count / total_cards *
                              100) if total_cards > 0 else 0
                emoji = COLOR_EMOJIS.get(color, '🎨')
                color_text += f"{emoji} **{color.capitalize()}:** {count} ({percentage:.1f}%)\n"

        if color_text:
            embed.add_field(name="🎨 Color Distribution",
                            value=color_text, inline=False)

    return embed


def create_collection_overview_embed(username: str, comparisons: List[Dict[str, Any]]) -> discord.Embed:
    """
    Create a Discord embed for collection overview.

    Args:
        username: The username of the requester.
        comparisons: List of set comparison results (supports both full and simplified formats).

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
        # Handle both formats
        if 'completion_percentage' in comp:
            # Full format
            completion_pct = comp['completion_percentage']
            your_total = comp['your_total']
            set_total = comp['set_total']
            set_name = comp.get('set_name', 'Unknown Set')
            set_code = comp.get('set_code', 'UNK')
        else:
            # Simplified format
            completion_pct = comp.get('completion', 0)
            your_total = comp.get('owned', 0)
            set_total = comp.get('total', 0)
            set_name = comp.get(
                'set_name', f"Set {comp.get('set_code', 'UNK')}")
            set_code = comp.get('set_code', 'UNK')

        # Add completion emoji
        if completion_pct >= 50:
            emoji = "🎯"
        elif completion_pct >= 25:
            emoji = "📈"
        elif completion_pct >= 10:
            emoji = "📊"
        else:
            emoji = "📋"

        completion_text += f"{emoji} **{set_name} ({set_code})**\n"
        completion_text += f"└ {your_total}/{set_total} cards ({completion_pct:.1f}%)\n\n"

    embed.add_field(
        name="🏆 Top Sets by Completion",
        value=completion_text[:1000] +
        ("..." if len(completion_text) > 1000 else ""),
        inline=False
    )

    # Calculate overall stats
    total_owned = 0
    total_possible = 0

    for comp in comparisons:
        if 'your_total' in comp:
            total_owned += comp['your_total']
            total_possible += comp['set_total']
        else:
            total_owned += comp.get('owned', 0)
            total_possible += comp.get('total', 0)

    overall_completion = (total_owned / total_possible *
                          100) if total_possible > 0 else 0

    # Count sets with 50%+ completion
    high_completion_sets = 0
    for comp in comparisons:
        completion = comp.get('completion_percentage',
                              comp.get('completion', 0))
        if completion >= 50:
            high_completion_sets += 1

    embed.add_field(
        name="📈 Overall Statistics",
        value=f"**Total Cards:** {total_owned:,}\n**Overall Completion:** {overall_completion:.1f}%\n**Sets with 50%+ completion:** {high_completion_sets}",
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
        comparison: Comparison result data (supports both full and simplified formats).

    Returns:
        Discord embed object.
    """
    # Handle both formats
    if 'your_total' in comparison:
        # Full format
        your_total = comparison['your_total']
        set_total = comparison['set_total']
        completion_pct = comparison['completion_percentage']
        rarity_breakdown = comparison.get('your_rarity_breakdown', {})
    else:
        # Simplified format
        your_total = comparison.get('owned_cards', 0)
        set_total = comparison.get('total_cards', 0)
        completion_pct = comparison.get('completion_percentage', 0)
        rarity_breakdown = comparison.get('rarity_breakdown', {})

    embed = discord.Embed(
        title=f"🔍 Collection Comparison: {set_code}",
        color=EMBED_COLORS['comparison'],
        description=f"**Your** progress: **{your_total} / {set_total} cards ({completion_pct:.1f}% complete)**"
    )

    # Rarity completion
    if rarity_breakdown:
        rarity_text = ""
        for rarity, count in rarity_breakdown.items():
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
            "`!commander join` - Join a game (interactive selection) \n"
            "`!commander leave` - Leave your current game (auto-finds) \n"
            "`!commander list` - List active games in this channel\n"
            "`!commander info <game_id>` - Show game details"
        ),
        inline=False
    )

    embed.add_field(
        name="⚙️ Game Setup",
        value=(
            "`!commander setcommander <name>` - Set commander with archetype \n"
            "`!commander archetype` - Change your commander's archetype \n"
            "`!commander setplace` - Set placement with emoji reactions \n"
            "`!commander finish <game_id>` - Finish the game (creator only)"
        ),
        inline=False
    )

    embed.add_field(
        name="📊 Statistics & Analytics",
        value=(
            "`!commander stats` - View your game statistics & archetype data \n"
            "`!commander meta [days]` - Server meta analysis \n"
            "`!commander trends [days]` - Your performance trends "
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
            "`!commander achievements` - View your achievements \n"
            "`!commander achievements check` - Check for new achievements \n"
            "`!commander achievements info <name>` - View achievement details \n"
            "`!commander leaderboard` - Achievement leaderboard "
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
            "`!commander setcommander Atraxa` → Set commander with archetype selection \n"
            "`!commander join` → Interactive game selection with reactions "
        ),
        inline=False
    )

    embed.add_field(
        name="🏆 Archetype & Achievement Examples",
        value=(
            "**Archetype Selection:** Choose ⚡ Aggro, 🛡️ Control, 🔄 Combo with reactions \n"
            "**Achievements:** `!commander achievements` • `!commander leaderboard` \n"
            "**Analytics:** `!commander meta 7` → Last 7 days meta analysis "
        ),
        inline=False
    )

    embed.add_field(
        name="🧠 Trivia & Fun",
        value=(
            "**Trivia Commands:**\n"
            "`!trivia` → Start MTG trivia game (react with 🇦🇧🇨🇩)\n"
            "`!trivia stats` → Your trivia statistics and accuracy\n"
            "`!trivia leaderboard` → Top trivia players by points"
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
