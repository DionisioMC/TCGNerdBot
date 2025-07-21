"""
Example reaction handler for archetype selection.
This shows how the main bot file would handle archetype reactions.
"""

import discord
from commander_games import (
    commander_manager, 
    get_archetype_from_emoji,
    create_archetype_selection_embed
)
from edhrec_api import EDHRECAPI


async def handle_archetype_reaction(reaction, user):
    """
    Handle archetype selection reactions.
    This function should be called from the main bot's on_reaction_add event.
    """
    # Skip bot reactions
    if user.bot:
        return
    
    # Check if this is an archetype selection message
    embed = reaction.message.embeds[0] if reaction.message.embeds else None
    if not embed or "Select Commander Archetype" not in embed.title:
        return
    
    # Find the user's active game
    game = commander_manager.get_user_unfinished_game(user.id)
    if not game:
        return
    
    # Get commander and current archetype
    commander_name = game.players[user.id].get('commander')
    if not commander_name:
        return
    
    # Get archetype data
    archetype_data = EDHRECAPI.get_commander_archetypes(commander_name)
    if not archetype_data or not archetype_data.get('archetypes'):
        return
    
    # Convert emoji to archetype
    selected_archetype = get_archetype_from_emoji(str(reaction.emoji), archetype_data['archetypes'])
    if not selected_archetype:
        return
    
    # Set the new archetype
    success, msg, updated_game = commander_manager.set_commander_archetype_by_user(user.id, selected_archetype)
    
    if success:
        # Update the embed to show the new selection
        current_archetype = updated_game.players[user.id].get('commander_archetype', 'Unknown')
        new_embed = create_archetype_selection_embed(commander_name, archetype_data, current_archetype)
        
        await reaction.message.edit(embed=new_embed)
        
        # Send confirmation message
        await reaction.message.channel.send(f"✅ {msg}")
        
        # Remove user's reaction to allow for future selections
        await reaction.remove(user)


# Example integration in main bot file:
"""
@bot.event
async def on_reaction_add(reaction, user):
    # Handle placement reactions (existing)
    await handle_placement_reaction(reaction, user)
    
    # Handle join game reactions (existing)  
    await handle_join_game_reaction(reaction, user)
    
    # Handle archetype reactions (new)
    await handle_archetype_reaction(reaction, user)
"""
