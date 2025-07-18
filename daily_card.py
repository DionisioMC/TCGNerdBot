"""
Daily card functionality for the TCG Nerd Bot.
Handles the scheduling and posting of daily random cards.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional
import discord

from scryfall_api import ScryfallAPI
from discord_helpers import create_daily_card_embed
from config import DAILY_CARD_TIME_HOUR, DAILY_CARD_TIME_MINUTE, PREFERRED_CHANNEL_NAMES


async def post_daily_card(client: discord.Client, guild_id: int) -> None:
    """
    Post the daily random card to the guild's general channel.
    
    Args:
        client: Discord client instance.
        guild_id: ID of the guild to post to.
    """
    try:
        guild = discord.utils.get(client.guilds, id=guild_id)
        if not guild:
            print("Guild not found for daily card posting")
            return
        
        # Try to find a general channel (common channel names)
        channel = None
        for ch in guild.text_channels:
            if ch.name.lower() in PREFERRED_CHANNEL_NAMES:
                channel = ch
                break
        
        # If no specific channel found, use the first available text channel
        if not channel:
            channel = guild.text_channels[0] if guild.text_channels else None
            
        if not channel:
            print("No suitable channel found for daily card posting")
            return
            
        card_data = await ScryfallAPI.get_random_card()
        if card_data:
            embed = create_daily_card_embed(card_data)
            await channel.send(embed=embed)
            print(f"Daily card posted successfully: {card_data.get('name', 'Unknown')}")
        else:
            await channel.send("❌ Failed to fetch today's random card. Try again later!")
            
    except Exception as e:
        print(f"Error posting daily card: {e}")


async def daily_card_task(client: discord.Client, guild_id: int) -> None:
    """
    Background task that runs daily at 10 AM.
    
    Args:
        client: Discord client instance.
        guild_id: ID of the guild to post to.
    """
    await client.wait_until_ready()
    
    while not client.is_closed():
        now = datetime.now()
        # Calculate next 10 AM
        next_run = now.replace(hour=DAILY_CARD_TIME_HOUR, minute=DAILY_CARD_TIME_MINUTE, second=0, microsecond=0)
        
        # If it's already past 10 AM today, schedule for tomorrow
        if now.hour >= DAILY_CARD_TIME_HOUR:
            next_run += timedelta(days=1)
        
        # Calculate seconds until next run
        seconds_until_run = (next_run - now).total_seconds()
        
        print(f"Daily card task scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Wait until it's time
        await asyncio.sleep(seconds_until_run)
        
        # Post the daily card
        await post_daily_card(client, guild_id)
        
        # Wait 24 hours before next iteration (in case of small timing discrepancies)
        await asyncio.sleep(24 * 60 * 60)
