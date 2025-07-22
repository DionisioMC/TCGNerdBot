"""
TCG Nerd Bot - A Discord bot for Magic: The Gathering card collection management.

This is the main bot file that handles Discord events and delegates command processing
to specialized modules for better code organization and maintainability.
"""

import asyncio
from typing import Optional

import discord
from dotenv import load_dotenv

from command_handlers import CommandHandlers, parse_bracketed_content, parse_braced_content
from daily_card import daily_card_task
from config import DISCORD_TOKEN, DISCORD_SERVER

# Load environment variables
load_dotenv()
TOKEN: Optional[str] = DISCORD_TOKEN
GUILD = DISCORD_SERVER

# Configure Discord client
intent = discord.Intents.default()
intent.message_content = True
# intent.members = True  # Disabled - requires privileged intent

client = discord.Client(intents=intent)

# Initialize command handlers (will be set in on_ready)
command_handlers: Optional[CommandHandlers] = None


@client.event
async def on_ready():
    """Event handler for when the bot is ready."""
    global command_handlers

    guild = discord.utils.get(client.guilds, id=int(GUILD))

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    # Initialize command handlers
    command_handlers = CommandHandlers(client, int(GUILD))

    # Start the daily card task
    asyncio.create_task(daily_card_task(client, int(GUILD)))
    print("Daily card task started - will post random cards at 10:00 AM daily")


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    """Event handler for processing reaction additions."""
    # Ignore reactions from the bot itself
    if user == client.user:
        return

    # Ensure command handlers are initialized
    if not command_handlers:
        return

    try:
        # Handle placement reactions
        await command_handlers.handle_placement_reaction(reaction, user)

        # Handle join game reactions
        await command_handlers.handle_join_game_reaction(reaction, user)

        # Handle help navigation reactions
        await command_handlers.handle_help_navigation_reaction(reaction, user)

        # Handle archetype selection reactions
        await command_handlers.handle_archetype_reaction(reaction, user)
    except Exception as e:
        print(f"Error processing reaction: {e}")


@client.event
async def on_message(message: discord.Message):
    """Event handler for processing messages."""
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Ensure command handlers are initialized
    if not command_handlers:
        return

    try:
        # Card lookup with [card name]
        if '[' in message.content and ']' in message.content:
            card_name = parse_bracketed_content(message.content)
            await command_handlers.handle_card_lookup(message, card_name)

        # Wiki lookup with {keyword}
        elif '{' in message.content and '}' in message.content:
            keyword = parse_braced_content(message.content)
            await command_handlers.handle_wiki_lookup(message, keyword)

        # Handle file uploads - Card list checking
        elif message.attachments:
            await command_handlers.handle_file_upload(message)

        # Set statistics command: !setstats <SET_CODE>
        elif message.content.startswith('!setstats'):
            try:
                set_code = message.content.split()[1].upper()
                await command_handlers.handle_setstats_command(message, set_code)
            except IndexError:
                await message.channel.send("❌ Please provide a set code! Usage: `!setstats <SET_CODE>`\nExample: `!setstats MH3`")

        # Compare all sets command: !compareall
        elif message.content.startswith('!compareall'):
            await command_handlers.handle_compareall_command(message)

        # Collection comparison command: !compare <SET_CODE> (with alias !comp)
        elif message.content.startswith('!compare') or message.content.startswith('!comp'):
            try:
                if message.content.startswith('!comp'):
                    set_code = message.content.split()[1].upper()
                else:
                    set_code = message.content.split()[1].upper()
                await command_handlers.handle_compare_command(message, set_code)
            except IndexError:
                await message.channel.send("❌ Please provide a set code! Usage: `!compare <SET_CODE>` or `!comp <SET_CODE>`\nExample: `!comp OTJ`")

        # Test daily card command (manual trigger)
        elif message.content.startswith('!dailycard') or message.content.startswith('!randomcard'):
            await command_handlers.handle_dailycard_command(message)

        # Upload collection command: !upload
        elif message.content.startswith('!upload'):
            await command_handlers.handle_upload_command(message)

        # Help command (with aliases)
        elif (message.content.startswith('!help') or
              message.content.startswith('!commands') or
              message.content.startswith('!h')):
            await command_handlers.handle_help_command(message)

        # Commander game tracking commands (with aliases)
        elif (message.content.startswith('!commander') or
              message.content.startswith('!c ')):
            try:
                # Handle alias
                if message.content.startswith('!c '):
                    # Replace !c with !commander for processing
                    command_content = message.content.replace(
                        '!c ', '!commander ', 1)
                    # Remove '!commander' from args
                    args = command_content.split()[1:]
                else:
                    # Remove '!commander' from args
                    args = message.content.split()[1:]
                await command_handlers.handle_commander_command(message, args)
            except IndexError:
                await command_handlers.handle_commander_command(message, [])

        # Short alias for commander (just "!c")
        elif message.content == '!c':
            await command_handlers.handle_commander_command(message, [])

        # Original collection request when bot is mentioned
        elif client.user and client.user.mentioned_in(message):
            await command_handlers.handle_mention(message)

    except Exception as e:
        print(f"Error processing message: {e}")
        await message.channel.send("❌ An unexpected error occurred while processing your request.")


def main():
    """Main function to run the bot."""
    if TOKEN:
        client.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN environment variable not set!")


if __name__ == "__main__":
    main()
