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
    Create a Discord embed for the help command.
    
    Returns:
        Discord embed object.
    """
    embed = discord.Embed(
        title="🤖 TCG Nerd Bot Commands",
        color=EMBED_COLORS['help'],
        description="Your Magic: The Gathering collection assistant!"
    )

    embed.add_field(
        name="🔍 Card Lookup",
        value="`[card name]` - Show card image\n`[card name] price` - Show EUR price",
        inline=False
    )

    embed.add_field(
        name="📚 Wiki Lookup",
        value="`{keyword}` - Search MTG Wiki",
        inline=False
    )

    embed.add_field(
        name="📊 Collection Analysis",
        value="`!setstats <SET>` - Get set statistics\n`!compare <SET>` - Compare your collection to a set\n`!compareall` - Compare your top collection sets",
        inline=False
    )

    embed.add_field(
        name="🌟 Daily Features",
        value="`!dailycard` or `!randomcard` - Get a random MTG card\n🕙 **Auto daily cards at 10:00 AM**",
        inline=False
    )

    embed.add_field(
        name="📁 File Upload",
        value="**Upload a .txt file** - Check who owns cards from your want list\n**Format:** `1x Card Name` per line\n**Example:**\n```\n1x Lightning Bolt\n2x Counterspell\n1x Sol Ring\n```\n\n**`!upload` + CSV file** - Update your collection\n**Format:** Standard CSV collection export with card data\n**Owner:** Your Discord name will be automatically added",
        inline=False
    )

    embed.add_field(
        name="🎯 Examples",
        value="`!setstats MH3`\n`!compare OTJ`\n`!compareall`\n`!dailycard`\n`[Lightning Bolt]`\n`[Mana Crypt] price`\n📎 Upload `my_wants.txt`\n`!upload` + 📋 `my_collection.csv`",
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
