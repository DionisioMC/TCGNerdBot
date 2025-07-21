"""
Command handlers for the TCG Nerd Bot.
Contains functions to handle various bot commands and responses.
"""

import random
from typing import List
import discord
import requests
from bs4 import BeautifulSoup

from scryfall_api import ScryfallAPI, get_card_price_eur, get_card_image_url
from discord_helpers import (
    create_set_stats_embed,
    create_collection_overview_embed, create_collection_comparison_embed,
    create_help_embed, create_help_embed_page, split_message_into_chunks
)
from request_db import (
    get_cards_from_csv, get_cards_from_txt, request_owners,
    get_set_stats, quick_rarity_comparison_by_owner,
    compare_top_sets_by_owner, update_collection_with_owner_data
)
from daily_card import post_daily_card
from config import COLLECTION_PATH, EXAMPLE_REQUEST_PATH, EMBED_COLORS
from commander_games import (
    commander_manager, create_game_info_embed, create_player_stats_embed, 
    create_game_finished_embed, create_placement_selection_embed, 
    get_placement_emojis, get_placement_from_emoji, create_join_games_embed,
    get_join_game_emojis
)
from commander_analytics import (
    analytics, create_meta_analysis_embed, create_player_trends_embed
)
from achievements import (
    achievement_manager, create_achievement_embed, create_achievements_overview_embed
)


class CommandHandlers:
    """Class containing all command handler methods for the bot."""
    
    def __init__(self, client: discord.Client, guild_id: int):
        self.client = client
        self.guild_id = guild_id
        self.collection_path = COLLECTION_PATH
        self.archetype_messages = {}  # Track archetype selection messages
    
    async def handle_card_lookup(self, message: discord.Message, card_name: str) -> None:
        """Handle card lookup with [card name] syntax."""
        try:
            card_data = await ScryfallAPI.get_card_by_name(card_name)

            if not card_data:
                responses = [
                    "The card doesn't exist, try again, bitch", 
                    "You fucked up",
                    "Billions of years of evolution for you to not being able to type a card name correctly? We are doomed...", 
                    "Good job buddy, thats not it"
                ]
                response = random.choice(responses)
                await message.channel.send(response)
                return

            if 'price' in message.content:
                eur_price = get_card_price_eur(card_data)
                if eur_price:
                    await message.channel.send(f"{eur_price} euros")
                else:
                    await message.channel.send("❌ EUR price not available for this card")
                    
            else:
                image_url = get_card_image_url(card_data)
                if image_url:
                    await message.channel.send(image_url)
                else:
                    await message.channel.send("❌ No image available for this card")

        except requests.RequestException as e:
            await message.channel.send(f"❌ Network error: {str(e)}")
        except (KeyError, ValueError) as e:
            await message.channel.send(f"❌ Error parsing card data: {str(e)}")
        except Exception as e:
            await message.channel.send(f"❌ Unexpected error: {str(e)}")

    async def handle_wiki_lookup(self, message: discord.Message, keyword: str) -> None:
        """Handle wiki lookup with {keyword} syntax."""
        try:
            URL = f'https://mtg.fandom.com/wiki/{keyword}'
            page = requests.get(URL)
            wiki = BeautifulSoup(page.content, 'html.parser')
            result = wiki.find('table').prettify()
            await message.channel.send(result)
        except Exception as e:
            await message.channel.send(f"❌ Error fetching wiki data: {str(e)}")

    async def handle_file_upload(self, message: discord.Message) -> None:
        """Handle file upload for card list checking only (TXT files)."""
        for attachment in message.attachments:
            # Only handle TXT files for card list checking
            if attachment.filename.endswith('.txt'):
                await self.handle_txt_cardlist_upload(message, attachment)
                break

    async def handle_csv_collection_upload(self, message: discord.Message, attachment) -> None:
        """Handle CSV collection upload with owner tracking."""
        await message.channel.send(f"� Processing your collection: **{attachment.filename}**...")
        
        try:
            # Download the CSV file
            file_content = await attachment.read()
            
            # Save temporarily to process with existing function
            temp_filename = f"temp_collection_{message.author.id}_{attachment.filename}"
            with open(temp_filename, 'wb') as temp_file:
                temp_file.write(file_content)
            
            # Get the owner name from Discord user
            owner_name = message.author.display_name
            
            # Update the collection with the new data
            success, result_message, cards_added = update_collection_with_owner_data(
                temp_filename, owner_name, self.collection_path
            )
            
            if success:
                embed = discord.Embed(
                    title="✅ Collection Updated Successfully!",
                    color=EMBED_COLORS['success'],
                    description=result_message
                )
                embed.add_field(
                    name="📊 Summary",
                    value=f"**Owner:** {owner_name}\n**Cards Added:** {cards_added}\n**File:** {attachment.filename}",
                    inline=False
                )
                embed.set_footer(text="Your previous collection entries have been replaced with the new data.")
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"❌ {result_message}")
            
            # Clean up temp file
            import os
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        except Exception as e:
            await message.channel.send(f"❌ Error processing CSV collection: {str(e)}\n\n**Expected CSV format:**\nYour CSV should contain card collection data with standard columns like 'Name', 'Set code', 'Rarity', etc.")

    async def handle_txt_cardlist_upload(self, message: discord.Message, attachment) -> None:
        """Handle TXT card list upload for ownership checking."""
        await message.channel.send(f"🔍 Processing your card list: **{attachment.filename}**...")

        try:
            # Download the file content
            file_content = await attachment.read()
            file_text = file_content.decode('utf-8')

            # Save temporarily to process with existing function
            temp_filename = f"temp_{message.author.id}_{attachment.filename}"
            with open(temp_filename, 'w', encoding='utf-8') as temp_file:
                temp_file.write(file_text)

            # Process the card list
            try:
                cards = get_cards_from_txt(temp_filename)
                if not cards:
                    await message.channel.send("❌ No valid card entries found in the file. Please check the format (e.g., '1x Card Name').")
                    return
            except Exception as e:
                await message.channel.send(f"❌ Error parsing card list: {str(e)}\nPlease ensure each line follows the format: '1x Card Name'")
                return

            collection = get_cards_from_csv(self.collection_path)
            result = request_owners(cards, collection)

            if result.strip():
                # Split result into manageable chunks for Discord
                chunks = split_message_into_chunks(result)

                embed = discord.Embed(
                    title=f"🎯 Card Ownership Results for {attachment.filename}",
                    color=EMBED_COLORS['card_ownership'],
                    description="Here's who owns the cards you're looking for:"
                )
                await message.channel.send(embed=embed)

                for i, chunk in enumerate(chunks, 1):
                    await message.channel.send(f"**Results (Part {i}/{len(chunks)}):**\n```\n{chunk}\n```")
            else:
                await message.channel.send("❌ No cards from your list were found in any collection.")

            # Clean up temp file
            import os
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        except UnicodeDecodeError:
            await message.channel.send("❌ Error reading file: The file must be in UTF-8 text format.")
        except Exception as e:
            await message.channel.send(f"❌ Error processing file: {str(e)}\n\n**File format help:**\nEach line should be: `1x Card Name`\nExample:\n```\n1x Lightning Bolt\n2x Counterspell\n1x Sol Ring\n```")

    async def handle_setstats_command(self, message: discord.Message, set_code: str) -> None:
        """Handle !setstats command."""
        try:
            await message.channel.send(f"📊 Analyzing set statistics for **{set_code}**...")

            stats = get_set_stats(set_code)
            if stats:
                embed = create_set_stats_embed(stats)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"❌ Set **{set_code}** not found or API error.")
                
        except Exception as e:
            await message.channel.send(f"❌ Error analyzing set: {str(e)}")

    async def handle_compareall_command(self, message: discord.Message) -> None:
        """Handle !compareall command."""
        try:
            username = str(message.author.display_name)
            await message.channel.send("📊 Analyzing **your** top collection sets...")

            collection = get_cards_from_csv(self.collection_path)
            comparisons = compare_top_sets_by_owner(collection, username, top_count=15)

            if comparisons:
                embed = create_collection_overview_embed(username, comparisons)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("❌ No collection data found for **you**.")
                
        except Exception as e:
            await message.channel.send(f"❌ Error analyzing your collection: {str(e)}")

    async def handle_compare_command(self, message: discord.Message, set_code: str) -> None:
        """Handle !compare command."""
        try:
            username = str(message.author.display_name)
            await message.channel.send(f"🔍 Comparing **your** collection to **{set_code}**...")

            collection = get_cards_from_csv(self.collection_path)
            comparison = quick_rarity_comparison_by_owner(collection, set_code, username)

            if comparison:
                embed = create_collection_comparison_embed(set_code, comparison)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"❌ **You** don't have any cards from set **{set_code}** or set not found.")
                
        except Exception as e:
            await message.channel.send(f"❌ Error comparing collection: {str(e)}")

    async def handle_dailycard_command(self, message: discord.Message) -> None:
        """Handle !dailycard or !randomcard command."""
        try:
            await message.channel.send("🎲 Fetching a random card for you...")
            await post_daily_card(self.client, self.guild_id)
        except Exception as e:
            await message.channel.send(f"❌ Error fetching random card: {str(e)}")

    async def handle_upload_command(self, message: discord.Message) -> None:
        """Handle !upload command for CSV collection updates."""
        if not message.attachments:
            await message.channel.send("❌ Please attach a CSV file with your `!upload` command.\n\n**Usage:** `!upload` + attach your collection CSV file\n**Format:** Standard collection export (Binder Name, Name, Set code, Rarity, etc.)")
            return
        
        # Look for CSV file in attachments
        csv_attachment = None
        for attachment in message.attachments:
            if attachment.filename.endswith('.csv'):
                csv_attachment = attachment
                break
        
        if not csv_attachment:
            await message.channel.send("❌ Please attach a CSV file with your `!upload` command.\n\n**Supported format:** `.csv` files only\n**Example:** Export your collection from ManaBox, Deckbox, etc. as CSV")
            return
        
        await self.handle_csv_collection_upload(message, csv_attachment)

    async def handle_help_command(self, message: discord.Message) -> None:
        """Handle !help command with pagination."""
        try:
            embed = create_help_embed_page(1)  # Start with page 1
            help_message = await message.channel.send(embed=embed)
            
            # Add navigation reactions
            await help_message.add_reaction("⬅️")
            await help_message.add_reaction("➡️")
            
            # Store the message for reaction handling
            if not hasattr(self, 'pending_help_navigations'):
                self.pending_help_navigations = {}
            
            self.pending_help_navigations[help_message.id] = {
                'current_page': 1,
                'total_pages': 4,
                'user_id': message.author.id,
                'channel_id': message.channel.id
            }
            
            # Clean up after 5 minutes
            import asyncio
            asyncio.create_task(self._cleanup_help_navigation(help_message.id, 300))  # 5 minutes
            
        except Exception as e:
            await message.channel.send(f"❌ Error displaying help: {str(e)}")
    
    async def _cleanup_help_navigation(self, message_id: int, delay: int) -> None:
        """Clean up help navigation data after a delay."""
        import asyncio
        await asyncio.sleep(delay)
        
        if hasattr(self, 'pending_help_navigations') and message_id in self.pending_help_navigations:
            del self.pending_help_navigations[message_id]

    async def handle_mention(self, message: discord.Message) -> None:
        """Handle when bot is mentioned."""
        try:
            cards = get_cards_from_txt(EXAMPLE_REQUEST_PATH)
            collection = get_cards_from_csv(self.collection_path)
            username = str(message.author.display_name)
            result = request_owners(cards, collection, specific_owner=username)
            await message.channel.send(result)
        except Exception as e:
            await message.channel.send(f"❌ Error processing mention: {str(e)}")

    async def handle_commander_command(self, message: discord.Message, args: List[str]) -> None:
        """Handle !commander commands for game tracking."""
        if not args:
            await self.send_commander_help(message)
            return

        # Handle subcommand aliases
        subcommand_aliases = {
            'c': 'create',
            'j': 'join',
            'l': 'leave',
            's': 'start',
            'r': 'remove',
            'e': 'end',
            'st': 'stats',
            'g': 'games'
        }
        
        subcommand = args[0].lower()
        if subcommand in subcommand_aliases:
            subcommand = subcommand_aliases[subcommand]
            
        username = str(message.author.display_name)
        user_id = message.author.id
        channel_id = message.channel.id

        try:
            if subcommand == "create":
                success, msg, game = commander_manager.create_game(user_id, channel_id, username)
                if success:
                    embed = create_game_info_embed(game)
                    await message.channel.send(msg, embed=embed)
                else:
                    await message.channel.send(f"❌ {msg}")

            elif subcommand == "join":
                if len(args) > 1:
                    # Old format: !commander join <game_id>
                    game_id = args[1]
                    success, msg = commander_manager.join_game(game_id, user_id, username)
                    await message.channel.send(f"{'✅' if success else '❌'} {msg}")
                    
                    if success:
                        game = commander_manager.get_game_info(game_id)
                        if game:
                            embed = create_game_info_embed(game)
                            await message.channel.send(embed=embed)
                else:
                    # New format: !commander join (shows available games with reactions)
                    available_games = commander_manager.get_joinable_games_for_user(message.channel.id, user_id)
                    
                    if not available_games:
                        await message.channel.send("❌ No available games to join in this channel.\nUse `!commander create` to start a new game!")
                        return
                    
                    # Create and send selection embed
                    embed = create_join_games_embed(available_games, message.channel.id)
                    join_message = await message.channel.send(embed=embed)
                    
                    # Add reaction emojis
                    emojis = get_join_game_emojis(available_games)
                    for emoji in emojis:
                        await join_message.add_reaction(emoji)
                    
                    # Store the message for reaction handling
                    if not hasattr(commander_manager, 'pending_join_selections'):
                        commander_manager.pending_join_selections = {}
                    
                    commander_manager.pending_join_selections[join_message.id] = {
                        'user_id': user_id,
                        'username': username,
                        'games': available_games,
                        'emojis': emojis
                    }

            elif subcommand == "leave":
                if len(args) > 1:
                    # Old format: !commander leave <game_id>
                    game_id = args[1]
                    success, msg = commander_manager.leave_game(game_id, user_id)
                else:
                    # New format: !commander leave (auto-finds your game)
                    success, msg, game = commander_manager.leave_game_by_user(user_id)
                
                await message.channel.send(f"{'✅' if success else '❌'} {msg}")

            elif subcommand == "setcommander":
                if len(args) < 2:
                    await message.channel.send("❌ Please provide commander name! Usage: `!commander setcommander <commander_name>` or `!commander setcommander <game_id> <commander_name>`")
                    return
                
                # Check if first argument is a game_id (starts with 'game_')
                if args[1].startswith('game_') and len(args) >= 3:
                    # Old format: !commander setcommander <game_id> <commander_name>
                    game_id = args[1]
                    commander_name = " ".join(args[2:])
                    success, msg, archetype_data = await commander_manager.set_commander(game_id, user_id, commander_name)
                    
                    if success and archetype_data and archetype_data.get('archetypes'):
                        # Show archetype selection
                        game = commander_manager.get_game_info(game_id)
                        current_archetype = game.players[user_id].get('commander_archetype', 'Unknown')
                        
                        await message.channel.send(f"✅ {msg}")
                        
                        # Create archetype selection embed
                        from commander_games import create_archetype_selection_embed, get_archetype_emojis
                        embed = create_archetype_selection_embed(commander_name, archetype_data, current_archetype)
                        
                        archetype_msg = await message.channel.send(embed=embed)
                        
                        # Add reactions for archetype selection
                        emojis = get_archetype_emojis(archetype_data['archetypes'])
                        for emoji in emojis:
                            await archetype_msg.add_reaction(emoji)
                        
                        # Store archetype selection data for reaction handling
                        self.archetype_messages[archetype_msg.id] = {
                            'user_id': user_id,
                            'game_id': game_id,
                            'commander_name': commander_name,
                            'archetypes': archetype_data['archetypes'],
                            'emojis': emojis
                        }
                        return
                    else:
                        await message.channel.send(f"{'✅' if success else '❌'} {msg}")
                else:
                    # New format: !commander setcommander <commander_name>
                    commander_name = " ".join(args[1:])
                    success, msg, game, archetype_data = await commander_manager.set_commander_by_user(user_id, commander_name)
                    
                    if success and archetype_data and archetype_data.get('archetypes'):
                        # Show archetype selection
                        current_archetype = game.players[user_id].get('commander_archetype', 'Unknown')
                        
                        await message.channel.send(f"✅ {msg}")
                        
                        # Create archetype selection embed
                        from commander_games import create_archetype_selection_embed, get_archetype_emojis
                        embed = create_archetype_selection_embed(commander_name, archetype_data, current_archetype)
                        
                        archetype_msg = await message.channel.send(embed=embed)
                        
                        # Add reactions for archetype selection
                        emojis = get_archetype_emojis(archetype_data['archetypes'])
                        for emoji in emojis:
                            await archetype_msg.add_reaction(emoji)
                        
                        # Store archetype selection data for reaction handling
                        self.archetype_messages[archetype_msg.id] = {
                            'user_id': user_id,
                            'game_id': game.game_id,
                            'commander_name': commander_name,
                            'archetypes': archetype_data['archetypes'],
                            'emojis': emojis
                        }
                        return
                    else:
                        await message.channel.send(f"{'✅' if success else '❌'} {msg}")
                
                if success:
                    # Try to get game for info display
                    game = None
                    if 'game_id' in locals():
                        game = commander_manager.get_game_info(game_id)
                    else:
                        game = commander_manager.get_user_unfinished_game(user_id)
                    
                    if game:
                        embed = create_game_info_embed(game)
                        await message.channel.send(embed=embed)

            elif subcommand == "setplace":
                # New reaction-based placement setting
                game = commander_manager.get_user_unfinished_game(user_id)
                
                if not game:
                    await message.channel.send("❌ You're not in any active commander games!")
                    return
                
                if not game.players[user_id].get('commander'):
                    await message.channel.send("❌ You need to set your commander first using `!commander setcommander <commander_name>`!")
                    return
                
                available_placements = commander_manager.get_available_placements(game)
                
                if not available_placements:
                    await message.channel.send("❌ No placement positions are available!")
                    return
                
                # Create and send the placement selection embed
                embed = create_placement_selection_embed(game, user_id)
                placement_message = await message.channel.send(embed=embed)
                
                # Add reaction emojis for available placements
                reaction_emojis = get_placement_emojis(available_placements)
                for emoji in reaction_emojis:
                    await placement_message.add_reaction(emoji)
                
                # Store the message ID for reaction handling
                if not hasattr(self, 'placement_messages'):
                    self.placement_messages = {}
                self.placement_messages[placement_message.id] = {
                    'user_id': user_id,
                    'game_id': game.game_id,
                    'available_placements': available_placements
                }

            elif subcommand == "setplace_old":
                # Keep the old text-based method as backup
                if len(args) < 3:
                    await message.channel.send("❌ Please provide game ID and placement! Usage: `!commander setplace_old <game_id> <placement>`")
                    return
                
                game_id = args[1]
                try:
                    placement = int(args[2])
                except ValueError:
                    await message.channel.send("❌ Placement must be a number!")
                    return
                
                success, msg = commander_manager.set_placement(game_id, user_id, placement)
                await message.channel.send(f"{'✅' if success else '❌'} {msg}")
                
                if success:
                    game = commander_manager.get_game_info(game_id)
                    if game:
                        embed = create_game_info_embed(game)
                        await message.channel.send(embed=embed)

            elif subcommand == "finish":
                if len(args) < 2:
                    await message.channel.send("❌ Please provide a game ID! Usage: `!commander finish <game_id>`")
                    return
                
                game_id = args[1]
                success, msg, game = commander_manager.finish_game(game_id, user_id)
                
                if success:
                    embed = create_game_finished_embed(game)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(f"❌ {msg}")

            elif subcommand == "info":
                if len(args) < 2:
                    await message.channel.send("❌ Please provide a game ID! Usage: `!commander info <game_id>`")
                    return
                
                game_id = args[1]
                game = commander_manager.get_game_info(game_id)
                
                if game:
                    embed = create_game_info_embed(game)
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("❌ Game not found!")

            elif subcommand == "archetype":
                # Change commander archetype with reaction selection
                game = commander_manager.get_user_unfinished_game(user_id)
                
                if not game:
                    await message.channel.send("❌ You're not in any active commander games!")
                    return
                
                if not game.players[user_id].get('commander'):
                    await message.channel.send("❌ You need to set your commander first using `!commander setcommander <commander_name>`!")
                    return
                
                commander_name = game.players[user_id]['commander']
                current_archetype = game.players[user_id].get('commander_archetype', 'Unknown')
                
                # Fetch archetype data from EDHREC
                from edhrec_api import edhrec_api
                archetype_data = edhrec_api.get_commander_archetypes(commander_name)
                
                if not archetype_data or not archetype_data.get('archetypes'):
                    await message.channel.send(f"❌ No archetype data available for **{commander_name}**!")
                    return
                
                # Create archetype selection embed
                from commander_games import create_archetype_selection_embed, get_archetype_emojis
                embed = create_archetype_selection_embed(commander_name, archetype_data, current_archetype)
                
                archetype_msg = await message.channel.send(embed=embed)
                
                # Add reactions for archetype selection
                emojis = get_archetype_emojis(archetype_data['archetypes'])
                for emoji in emojis:
                    await archetype_msg.add_reaction(emoji)
                
                # Store archetype selection data for reaction handling
                self.archetype_messages[archetype_msg.id] = {
                    'user_id': user_id,
                    'game_id': game.game_id,
                    'commander_name': commander_name,
                    'archetypes': archetype_data['archetypes'],
                    'emojis': emojis
                }

            elif subcommand == "list":
                # List active games in this channel
                active_games = commander_manager.get_channel_active_games(channel_id)
                
                if not active_games:
                    await message.channel.send("📭 No active commander games in this channel.")
                    return
                
                embed = discord.Embed(
                    title="🎯 Active Commander Games",
                    color=EMBED_COLORS.get('commander_game', 0x8B4513),
                    description=f"Active games in this channel:"
                )
                
                for game in active_games:
                    player_count = len(game.players)
                    creator_name = next((p['username'] for p in game.players.values() if game.creator_id in game.players), "Unknown")
                    
                    embed.add_field(
                        name=f"Game: {game.game_id}",
                        value=f"**Creator:** {creator_name}\n**Players:** {player_count}/8\n**Started:** {game.start_time.strftime('%H:%M')}",
                        inline=True
                    )
                
                await message.channel.send(embed=embed)

            elif subcommand == "stats":
                # Show player stats
                stats = commander_manager.get_player_stats(user_id)
                embed = create_player_stats_embed(user_id, username, stats)
                await message.channel.send(embed=embed)

            elif subcommand == "meta":
                # Show server meta analysis
                days = 30
                if len(args) > 1:
                    try:
                        days = int(args[1])
                        days = max(1, min(days, 365))  # Limit between 1 and 365 days
                    except ValueError:
                        pass
                
                await message.channel.send(f"📊 Analyzing server meta for the last {days} days...")
                
                meta_stats = analytics.get_server_meta_analysis(channel_id, days)
                embed = create_meta_analysis_embed(meta_stats, days)
                await message.channel.send(embed=embed)

            elif subcommand == "trends":
                # Show player trends analysis
                days = 30
                if len(args) > 1:
                    try:
                        days = int(args[1])
                        days = max(1, min(days, 365))
                    except ValueError:
                        pass
                
                await message.channel.send(f"📈 Analyzing your trends for the last {days} days...")
                
                trends = analytics.get_player_trends(user_id, days)
                embed = create_player_trends_embed(user_id, username, trends)
                await message.channel.send(embed=embed)

            elif subcommand == "achievements":
                # Show or manage achievements
                if len(args) > 1 and args[1].lower() == "check":
                    # Check for new achievements
                    new_achievements = achievement_manager.check_achievements(user_id)
                    
                    if new_achievements:
                        await message.channel.send(f"🎉 **{username}**, you've earned {len(new_achievements)} new achievement{'s' if len(new_achievements) > 1 else ''}!")
                        
                        for achievement in new_achievements:
                            embed = create_achievement_embed(achievement, is_new=True)
                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("✅ No new achievements at this time. Keep playing to unlock more!")
                else:
                    # Show achievements overview
                    player_data = achievement_manager.get_player_achievements(user_id)
                    total_achievements = len(achievement_manager.achievements)
                    
                    embed = create_achievements_overview_embed(user_id, username, player_data, total_achievements)
                    await message.channel.send(embed=embed)

            elif subcommand == "leaderboard":
                # Show achievement leaderboard
                leaderboard = achievement_manager.get_achievement_leaderboard(10)
                
                if not leaderboard:
                    await message.channel.send("📊 No achievement data available yet.")
                    return
                
                embed = discord.Embed(
                    title="🏆 Achievement Leaderboard",
                    color=EMBED_COLORS.get('achievements', 0xf39c12),
                    description="Top players by achievement points"
                )
                
                leaderboard_text = ""
                rank_emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                
                for i, (player_id, data) in enumerate(leaderboard):
                    emoji = rank_emojis[i] if i < len(rank_emojis) else f"{i+1}."
                    
                    # Try to get username from recent games
                    player_name = f"Player {player_id}"
                    try:
                        # This is a simplified way - in production you'd want to cache usernames
                        player_name = f"<@{player_id}>"
                    except:
                        pass
                    
                    leaderboard_text += (
                        f"{emoji} **{player_name}**\n"
                        f"   🏆 {data['total_points']} points • "
                        f"🎯 {data['total_achievements']} achievements\n\n"
                    )
                
                embed.add_field(
                    name="🏅 Rankings",
                    value=leaderboard_text,
                    inline=False
                )
                
                embed.set_footer(text="🎮 Play more games to climb the leaderboard!")
                await message.channel.send(embed=embed)

            else:
                await self.send_commander_help(message)

        except Exception as e:
            await message.channel.send(f"❌ Error processing commander command: {str(e)}")

    async def handle_placement_reaction(self, reaction: discord.Reaction, user: discord.User) -> None:
        """Handle reactions on placement selection messages."""
        # Check if this is a placement message
        if not hasattr(self, 'placement_messages'):
            return
        
        message_id = reaction.message.id
        if message_id not in self.placement_messages:
            return
        
        placement_data = self.placement_messages[message_id]
        
        # Check if the reaction is from the correct user
        if user.id != placement_data['user_id']:
            # Remove reaction from wrong user
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Convert emoji to placement number
        placement = get_placement_from_emoji(str(reaction.emoji))
        if placement is None or placement not in placement_data['available_placements']:
            # Invalid placement, remove reaction
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Set the placement
        success, msg, game = commander_manager.set_placement_by_reaction(user.id, placement)
        
        if success:
            # Update the original message to show the placement was set
            embed = discord.Embed(
                title="✅ Placement Set!",
                color=EMBED_COLORS.get('success', 0x00ff00),
                description=f"**{user.display_name}** - Placement set to **#{placement}**!"
            )
            
            try:
                await reaction.message.edit(embed=embed)
                await reaction.message.clear_reactions()
            except:
                pass
            
            # Send updated game info if needed
            if game and game.can_finish_game():
                finish_embed = discord.Embed(
                    title="🎯 Game Ready to Finish!",
                    color=EMBED_COLORS.get('commander_game', 0x8B4513),
                    description=f"All players in game **{game.game_id}** have set their commanders and placements!\n\nGame creator can use `!commander finish {game.game_id}` to complete the game."
                )
                await reaction.message.channel.send(embed=finish_embed)
        else:
            # Error setting placement
            error_embed = discord.Embed(
                title="❌ Error",
                color=0xff0000,
                description=msg
            )
            try:
                await reaction.message.edit(embed=error_embed)
            except:
                pass
        
        # Clean up the message data
        if message_id in self.placement_messages:
            del self.placement_messages[message_id]

    async def handle_join_game_reaction(self, reaction: discord.Reaction, user: discord.User) -> None:
        """Handle join game selection reactions."""
        # Check if this is a pending join selection
        if not hasattr(commander_manager, 'pending_join_selections'):
            return
        
        message_id = reaction.message.id
        if message_id not in commander_manager.pending_join_selections:
            return
        
        join_data = commander_manager.pending_join_selections[message_id]
        
        # Make sure it's the right user
        if user.id != join_data['user_id']:
            # Remove reaction from wrong user
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Find which game was selected
        emoji_str = str(reaction.emoji)
        if emoji_str not in join_data['emojis']:
            # Invalid emoji, remove reaction
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        game_index = join_data['emojis'].index(emoji_str)
        if game_index >= len(join_data['games']):
            return
        
        selected_game = join_data['games'][game_index]
        
        # Join the game
        success, msg = commander_manager.join_game(selected_game.game_id, user.id, join_data['username'])
        
        # Send response
        if success:
            success_embed = discord.Embed(
                title="✅ Joined Game!",
                description=msg,
                color=EMBED_COLORS['commander_game']
            )
            await reaction.message.channel.send(embed=success_embed)
            
            # Show game info
            game = commander_manager.get_game_info(selected_game.game_id)
            if game:
                embed = create_game_info_embed(game)
                await reaction.message.channel.send(embed=embed)
        else:
            error_embed = discord.Embed(
                title="❌ Error",
                color=0xff0000,
                description=msg
            )
            await reaction.message.channel.send(embed=error_embed)
        
        # Clean up the selection message and pending data
        try:
            await reaction.message.delete()
        except:
            pass
        
        if message_id in commander_manager.pending_join_selections:
            del commander_manager.pending_join_selections[message_id]

    async def handle_help_navigation_reaction(self, reaction: discord.Reaction, user: discord.User) -> None:
        """Handle help page navigation reactions."""
        # Check if this is a pending help navigation
        if not hasattr(self, 'pending_help_navigations'):
            return
        
        message_id = reaction.message.id
        if message_id not in self.pending_help_navigations:
            return
        
        help_data = self.pending_help_navigations[message_id]
        
        # Make sure it's the right user
        if user.id != help_data['user_id']:
            # Remove reaction from wrong user
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Handle navigation
        emoji_str = str(reaction.emoji)
        current_page = help_data['current_page']
        total_pages = help_data['total_pages']
        new_page = current_page
        
        if emoji_str == "⬅️" and current_page > 1:
            new_page = current_page - 1
        elif emoji_str == "➡️" and current_page < total_pages:
            new_page = current_page + 1
        else:
            # Invalid navigation, remove reaction
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Update the page if changed
        if new_page != current_page:
            help_data['current_page'] = new_page
            new_embed = create_help_embed_page(new_page)
            
            try:
                await reaction.message.edit(embed=new_embed)
            except Exception as e:
                print(f"Error updating help page: {e}")
        
        # Remove the user's reaction to allow re-clicking
        try:
            await reaction.remove(user)
        except:
            pass

    async def send_commander_help(self, message: discord.Message) -> None:
        """Send commander commands help."""
        embed = discord.Embed(
            title="🎯 Commander Game Commands",
            color=EMBED_COLORS.get('help', 0x00ffff),
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
                "`!c st` = `!commander stats`\n"
                "`!comp` = `!compare` • `!h` = `!help`"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎮 Game Management",
            value=(
                "`!commander create` - Create a new game\n"
                "`!commander join` - Join a game (interactive game selection) 🆕\n"
                "`!commander leave` - Leave your current game (auto-finds your game) 🆕\n"
                "`!commander list` - List active games in this channel\n"
                "`!commander info <game_id>` - Show game details"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Game Setup",
            value=(
                "`!commander setcommander <commander_name>` - Set your commander (auto-finds your game) 🆕\n"
                "`!commander archetype` - Change your commander's archetype 🆕\n"
                "`!commander setplace` - Set your final placement with emoji reactions 🆕\n"
                "`!commander finish <game_id>` - Finish the game (creator only)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📊 Statistics & Analytics",
            value=(
                "`!commander stats` - View your commander game statistics\n"
                "`!commander meta [days]` - Server meta analysis (default: 30 days) 🆕\n"
                "`!commander trends [days]` - Your performance trends (default: 30 days) 🆕\n"
                "`!commander help` - Show this help message"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🏆 Achievements",
            value=(
                "`!commander achievements` - View your achievements 🆕\n"
                "`!commander achievements check` - Check for new achievements 🆕\n"
                "`!commander leaderboard` - Achievement leaderboard 🆕"
            ),
            inline=False
        )
        
        embed.add_field(
            name="✨ New Features",
            value=(
                "🎯 **No more game IDs needed** - Commands automatically find your active game\n"
                "🎮 **Interactive game selection** - React with emojis to join games\n"
                "🎨 **Color tracking** - Automatically fetches commander colors from Scryfall\n"
                "📊 **Rich statistics** - Track colors, win rates, and favorite commanders\n"
                "📈 **Advanced analytics** - Server meta analysis and performance trends\n"
                "🏆 **Achievement system** - Unlock achievements and compete on leaderboards"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📝 Quick Start",
            value=(
                "1. Create: `!commander create`\n"
                "2. Join: `!commander join` → select with reactions\n"
                "3. Set commander: `!commander setcommander <name>`\n"
                "4. After game: `!commander setplace` → select placement\n"
                "5. Finish: `!commander finish <game_id>` (creator only)"
            ),
            inline=False
        )
        
        embed.set_footer(text="🚀 Enhanced UX • 📊 Analytics • 🏆 Achievements • 2-8 players supported")
        
        await message.channel.send(embed=embed)

    async def handle_archetype_reaction(self, reaction: discord.Reaction, user: discord.User) -> None:
        """Handle archetype selection reactions."""
        # Check if this is an archetype selection message
        if not hasattr(self, 'archetype_messages'):
            return
        
        message_id = reaction.message.id
        if message_id not in self.archetype_messages:
            return
        
        archetype_data = self.archetype_messages[message_id]
        
        # Check if the reaction is from the correct user
        if user.id != archetype_data['user_id']:
            # Remove reaction from wrong user
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Find which archetype this emoji represents
        emoji_str = str(reaction.emoji)
        emojis = archetype_data['emojis']
        archetypes = archetype_data['archetypes']
        
        # Find the index of the emoji in the list
        selected_archetype = None
        try:
            emoji_index = emojis.index(emoji_str)
            if emoji_index < len(archetypes):
                selected_archetype = archetypes[emoji_index]
        except (ValueError, IndexError):
            # Invalid emoji, remove reaction
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        if not selected_archetype:
            try:
                await reaction.remove(user)
            except:
                pass
            return
        
        # Update the archetype using commander_manager
        from commander_games import commander_manager
        success, msg = commander_manager.set_archetype(
            archetype_data['game_id'],
            user.id,
            selected_archetype
        )
        
        if success:
            # Update the original message to show the archetype was set
            embed = discord.Embed(
                title="✅ Archetype Set!",
                color=0x00ff00,
                description=f"**{user.display_name}** - Archetype for **{archetype_data['commander_name']}** set to **{selected_archetype}**!"
            )
            
            try:
                await reaction.message.edit(embed=embed)
                await reaction.message.clear_reactions()
            except:
                pass
        else:
            # Error setting archetype
            error_embed = discord.Embed(
                title="❌ Error",
                color=0xff0000,
                description=msg
            )
            try:
                await reaction.message.edit(embed=error_embed)
            except:
                pass
        
        # Clean up the message data
        if message_id in self.archetype_messages:
            del self.archetype_messages[message_id]


def parse_bracketed_content(content: str) -> str:
    """Extract content between square brackets."""
    start = content.index('[') + 1
    return content[start:content.index(']')].lower()


def parse_braced_content(content: str) -> str:
    """Extract content between curly braces."""
    start = content.index('{') + 1
    return content[start:content.index('}')]
