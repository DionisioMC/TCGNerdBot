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
    create_help_embed, split_message_into_chunks
)
from request_db import (
    get_cards_from_csv, get_cards_from_txt, request_owners,
    get_set_stats, quick_rarity_comparison_by_owner,
    compare_top_sets_by_owner, update_collection_with_owner_data
)
from daily_card import post_daily_card
from config import COLLECTION_PATH, EXAMPLE_REQUEST_PATH, EMBED_COLORS


class CommandHandlers:
    """Class containing all command handler methods for the bot."""
    
    def __init__(self, client: discord.Client, guild_id: int):
        self.client = client
        self.guild_id = guild_id
        self.collection_path = COLLECTION_PATH
    
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
        """Handle !help command."""
        try:
            embed = create_help_embed()
            await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send(f"❌ Error displaying help: {str(e)}")

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


def parse_bracketed_content(content: str) -> str:
    """Extract content between square brackets."""
    start = content.index('[') + 1
    return content[start:content.index(']')].lower()


def parse_braced_content(content: str) -> str:
    """Extract content between curly braces."""
    start = content.index('{') + 1
    return content[start:content.index('}')]
