import os
from typing import Optional
import asyncio
from datetime import datetime, time, timedelta

import discord
import requests
import random
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from request_db import (get_cards_from_csv, get_cards_from_txt, request_owners,
                        get_set_stats, quick_rarity_comparison_by_owner, analyze_commander_sets_by_owner,
                        compare_top_sets_by_owner)

load_dotenv()
TOKEN: Optional[str] = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

intent = discord.Intents.default()
intent.message_content = True
# intent.members = True  # Disabled - requires privileged intent

client = discord.Client(intents=intent)


async def get_random_card():
    """Fetch a random card from Scryfall API"""
    try:
        response = requests.get('https://api.scryfall.com/cards/random', timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching random card: HTTP {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Network error fetching random card: {e}")
        return None


async def post_daily_card():
    """Post the daily random card to the guild's general channel"""
    try:
        guild = discord.utils.get(client.guilds, id=int(GUILD))
        if not guild:
            print("Guild not found for daily card posting")
            return
        
        # Try to find a general channel (common channel names)
        channel = None
        for ch in guild.text_channels:
            if ch.name.lower() in ['general', 'chat', 'main', 'cards', 'daily']:
                channel = ch
                break
        
        # If no specific channel found, use the first available text channel
        if not channel:
            channel = guild.text_channels[0] if guild.text_channels else None
            
        if not channel:
            print("No suitable channel found for daily card posting")
            return
            
        card_data = await get_random_card()
        if card_data:
            embed = discord.Embed(
                title="🌟 Daily Random Card",
                color=0xffd700,
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
            rarity_emojis = {
                'common': '⚪',
                'uncommon': '🔵', 
                'rare': '🟡',
                'mythic': '🔴',
                'special': '🌟'
            }
            rarity_emoji = rarity_emojis.get(rarity, '❓')
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
            
            await channel.send(embed=embed)
            print(f"Daily card posted successfully: {card_data.get('name', 'Unknown')}")
        else:
            await channel.send("❌ Failed to fetch today's random card. Try again later!")
            
    except Exception as e:
        print(f"Error posting daily card: {e}")


async def daily_card_task():
    """Background task that runs daily at 10 AM"""
    await client.wait_until_ready()
    
    while not client.is_closed():
        now = datetime.now()
        # Calculate next 10 AM
        next_run = now.replace(hour=10, minute=0, second=0, microsecond=0)
        
        # If it's already past 10 AM today, schedule for tomorrow
        if now.hour >= 10:
            next_run += timedelta(days=1)
        
        # Calculate seconds until next run
        seconds_until_run = (next_run - now).total_seconds()
        
        print(f"Daily card task scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Wait until it's time
        await asyncio.sleep(seconds_until_run)
        
        # Post the daily card
        await post_daily_card()
        
        # Wait 24 hours before next iteration (in case of small timing discrepancies)
        await asyncio.sleep(24 * 60 * 60)



@client.event
async def on_ready():

    guild = discord.utils.get(client.guilds, id=int(GUILD))

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    # Start the daily card task
    asyncio.create_task(daily_card_task())
    print("Daily card task started - will post random cards at 10:00 AM daily")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Card lookup with [card name]
    if '[' and ']' in message.content:
        start = message.content.index('[') + 1
        card_name = message.content[start:message.content.index(']')].lower()

        try:
            api = requests.get(
                f'https://api.scryfall.com/cards/named?exact={card_name}', timeout=10)

            if api.status_code == 404:
                responses = ["The card doesn't exist, try again, bitch", "You fucked up",
                             "Billions of years of evolution for you to not being able to type a card name correctly? We are doomed...", "Good job buddy, thats not it"]
                num = random.randint(0, len(responses) - 1)
                await message.channel.send(responses[num])
                return
            elif api.status_code != 200:
                await message.channel.send(f"❌ API error: HTTP {api.status_code}")
                return

            data = api.json()

            if 'price' in message.content:
                prices = data.get('prices', {})
                eur_price = prices.get('eur')
                if eur_price:
                    await message.channel.send(f"{eur_price} euros")
                else:
                    await message.channel.send("❌ EUR price not available for this card")
            elif 'legal' in message.content:
                legalities = data.get('legalities', {})
                commander_legal = legalities.get('commander', 'unknown')
                await message.channel.send(f"Commander legality: {commander_legal}")
            else:
                image_uris = data.get('image_uris', {})
                image_url = image_uris.get('normal')
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

    # Wiki lookup with {keyword}
    elif '{' and '}' in message.content:
        start = message.content.index('{') + 1
        keyword = message.content[start:message.content.index('}')]
        URL = f'https://mtg.fandom.com/wiki/{keyword}'
        page = requests.get(URL)
        wiki = BeautifulSoup(page.content, 'html.parser')
        result = wiki.find('table').prettify()
        await message.channel.send(result)

    # Handle file uploads - Card list checking
    elif message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.txt'):
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
                    cards = get_cards_from_txt(temp_filename)

                    # Load collection
                    file_path = 'Collections/final_collection.csv'
                    collection = get_cards_from_csv(file_path)

                    # Find owners for all cards (not filtered by requester)
                    result = request_owners(cards, collection)

                    if result.strip():
                        # Split result into manageable chunks for Discord
                        max_length = 1900  # Discord message limit is 2000 chars
                        if len(result) > max_length:
                            chunks = [result[i:i+max_length]
                                      for i in range(0, len(result), max_length)]

                            embed = discord.Embed(
                                title=f"🎯 Card Ownership Results for {attachment.filename}",
                                color=0x9932cc,
                                description="Here's who owns the cards you're looking for:"
                            )
                            await message.channel.send(embed=embed)

                            for i, chunk in enumerate(chunks, 1):
                                await message.channel.send(f"**Results (Part {i}/{len(chunks)}):**\n```\n{chunk}\n```")
                        else:
                            embed = discord.Embed(
                                title=f"🎯 Card Ownership Results for {attachment.filename}",
                                color=0x9932cc,
                                description="Here's who owns the cards you're looking for:"
                            )
                            embed.add_field(
                                name="📋 Results", value=f"```\n{result}\n```", inline=False)
                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("❌ No cards from your list were found in any collection.")

                    # Clean up temp file
                    import os
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)

                except Exception as e:
                    await message.channel.send(f"❌ Error processing file: {str(e)}")

                break  # Only process first .txt file if multiple attachments

    # Set statistics command: !setstats <SET_CODE>
    elif message.content.startswith('!setstats'):
        try:
            set_code = message.content.split()[1].upper()
            await message.channel.send(f"📊 Analyzing set statistics for **{set_code}**...")

            # Get set stats (this will print to console, we need to capture it)
            stats = get_set_stats(set_code)
            if stats:
                embed = discord.Embed(
                    title=f"📊 Set Statistics: {stats['set_info']['name']}",
                    color=0x00ff00
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
                        percentage = (
                            count / stats['set_info']['total_cards']) * 100
                        rarity_text += f"**{rarity.capitalize()}:** {count} ({percentage:.1f}%)\n"

                embed.add_field(name="🎴 Rarity Breakdown",
                                value=rarity_text, inline=True)

                # Color breakdown
                color_text = ""
                color_emojis = {'white': '⚪', 'blue': '🔵', 'black': '⚫',
                                'red': '🔴', 'green': '🟢', 'colorless': '⚪', 'multicolor': '🌈'}
                for color, count in stats['color_breakdown'].items():
                    if count > 0:
                        percentage = (
                            count / stats['set_info']['total_cards']) * 100
                        emoji = color_emojis.get(color, '🎨')
                        color_text += f"{emoji} **{color.capitalize()}:** {count} ({percentage:.1f}%)\n"

                embed.add_field(name="🎨 Color Distribution",
                                value=color_text, inline=False)

                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"❌ Set **{set_code}** not found or API error.")
        except IndexError:
            await message.channel.send("❌ Please provide a set code! Usage: `!setstats <SET_CODE>`\nExample: `!setstats MH3`")
        except Exception as e:
            await message.channel.send(f"❌ Error analyzing set: {str(e)}")

    # Commander analysis command: !commander
    elif message.content.startswith('!commander'):
        try:
            # Always use the message author's Discord username (no access to other users)
            username = str(message.author.display_name)
            await message.channel.send("🎯 Analyzing **your** collection for Commander recommendations...")

            # Load collection
            file_path = 'Collections/final_collection.csv'
            collection = get_cards_from_csv(file_path)

            # Get commander analysis with owner filtering
            results = analyze_commander_sets_by_owner(collection, username)

            if results:
                embed = discord.Embed(
                    title=f"🎯 Commander Recommendations for {username}",
                    color=0x9932cc,
                    description="Based on your collection and Commander format relevance"
                )

                # Top 3 recommendations
                for i, result in enumerate(results[:3], 1):
                    recommendation_emoji = "🔥" if result['recommendation_score'] >= 8 else "⭐" if result[
                        'recommendation_score'] >= 6 else "✓"

                    embed.add_field(
                        name=f"{recommendation_emoji} #{i} {result['set_name']} ({result['set_code']})",
                        value=f"**Completion:** {result['completion_rate']:.1f}%\n**R/M Completion:** {result['rare_mythic_completion']:.1f}%\n**CMD Score:** {result['commander_score']}/10",
                        inline=True
                    )

                embed.add_field(
                    name="💡 Quick Guide",
                    value="🔥 = Priority Target\n⭐ = Good Investment\n✓ = Consider\n\nUse `!compare <SET>` for detailed analysis!",
                    inline=False
                )

                await message.channel.send(embed=embed)
            else:
                await message.channel.send("❌ No collection data found for **you** or error analyzing Commander sets.")
        except Exception as e:
            await message.channel.send(f"❌ Error with Commander analysis: {str(e)}")

    # Compare all sets command: !compareall
    elif message.content.startswith('!compareall'):
        try:
            # Always use the message author's Discord username
            username = str(message.author.display_name)
            await message.channel.send("📊 Analyzing **your** top collection sets...")

            # Load collection
            file_path = 'Collections/final_collection.csv'
            collection = get_cards_from_csv(file_path)

            # Get comparison for top 15 sets with owner filtering (optimized)
            comparisons = compare_top_sets_by_owner(
                collection, username, top_count=15)

            if comparisons:
                embed = discord.Embed(
                    title=f"📊 Collection Overview for {username}",
                    color=0x00d4aa,
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
                    value=completion_text[:1000] +
                    ("..." if len(completion_text) > 1000 else ""),
                    inline=False
                )

                # Calculate overall stats
                total_owned = sum(comp['your_total'] for comp in comparisons)
                total_possible = sum(comp['set_total'] for comp in comparisons)
                overall_completion = (
                    total_owned / total_possible * 100) if total_possible > 0 else 0

                embed.add_field(
                    name="📈 Overall Statistics",
                    value=f"**Total Cards:** {total_owned:,}\n**Overall Completion:** {overall_completion:.1f}%\n**Sets with 50%+ completion:** {len([c for c in comparisons if c['completion_percentage'] >= 50])}",
                    inline=True
                )

                embed.add_field(
                    name="💡 Quick Actions",
                    value="Use `!compare <SET>` for detailed set analysis\nUse `!commander` for format recommendations",
                    inline=True
                )

                await message.channel.send(embed=embed)
            else:
                await message.channel.send("❌ No collection data found for **you**.")
        except Exception as e:
            await message.channel.send(f"❌ Error analyzing your collection: {str(e)}")

    # Collection comparison command: !compare <SET_CODE>
    elif message.content.startswith('!compare'):
        try:
            parts = message.content.split()
            set_code = parts[1].upper()

            # Always use the message author's Discord username (no access to other users)
            username = str(message.author.display_name)
            await message.channel.send(f"🔍 Comparing **your** collection to **{set_code}**...")

            # Load collection
            file_path = 'Collections/final_collection.csv'
            collection = get_cards_from_csv(file_path)

            # Get comparison with owner filtering
            comparison = quick_rarity_comparison_by_owner(
                collection, set_code, username)

            if comparison:
                embed = discord.Embed(
                    title=f"🔍 Collection Comparison: {set_code}",
                    color=0xff9900,
                    description=f"**Your** progress: **{comparison['your_total']} / {comparison['set_total']} cards ({comparison['completion_percentage']:.1f}% complete)**"
                )

                # Rarity completion
                rarity_text = ""
                for rarity, count in comparison['your_rarity_breakdown'].items():
                    if count > 0:
                        rarity_text += f"**{rarity.capitalize()}:** {count} cards\n"

                embed.add_field(name="🎴 Collection by Rarity",
                                value=rarity_text or "No cards found", inline=True)
                embed.add_field(
                    name="💡 Tip", value="Use `!commander` for personalized recommendations!", inline=False)

                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"❌ **You** don't have any cards from set **{set_code}** or set not found.")
        except IndexError:
            await message.channel.send("❌ Please provide a set code! Usage: `!compare <SET_CODE>`\nExample: `!compare OTJ`")
        except Exception as e:
            await message.channel.send(f"❌ Error comparing collection: {str(e)}")

    # Test daily card command (manual trigger)
    elif message.content.startswith('!dailycard') or message.content.startswith('!randomcard'):
        try:
            await message.channel.send("🎲 Fetching a random card for you...")
            await post_daily_card()
        except Exception as e:
            await message.channel.send(f"❌ Error fetching random card: {str(e)}")

    # Help command
    elif message.content.startswith('!help') or message.content.startswith('!commands'):
        embed = discord.Embed(
            title="🤖 TCG Nerd Bot Commands",
            color=0x00ffff,
            description="Your Magic: The Gathering collection assistant!"
        )

        embed.add_field(
            name="🔍 Card Lookup",
            value="`[card name]` - Show card image\n`[card name] price` - Show EUR price\n`[card name] legal` - Check Commander legality",
            inline=False
        )

        embed.add_field(
            name="📚 Wiki Lookup",
            value="`{keyword}` - Search MTG Wiki",
            inline=False
        )

        embed.add_field(
            name="📊 Collection Analysis",
            value="`!setstats <SET>` - Get set statistics\n`!compare <SET>` - Compare your collection to a set\n`!compareall` - Compare your top collection sets\n`!commander` - Get Commander format recommendations",
            inline=False
        )

        embed.add_field(
            name="🌟 Daily Features",
            value="`!dailycard` or `!randomcard` - Get a random MTG card\n� **Auto daily cards at 10:00 AM**",
            inline=False
        )

        embed.add_field(
            name="�📁 File Upload",
            value="**Upload a .txt file** - Check who owns cards from your want list\n(Format: `1x Card Name` per line)",
            inline=False
        )

        embed.add_field(
            name="🎯 Examples",
            value="`!setstats MH3`\n`!compare OTJ`\n`!compareall`\n`!commander`\n`!dailycard`\n`[Lightning Bolt]`\n`[Mana Crypt] price`\n📎 Upload `my_wants.txt`",
            inline=False
        )

        await message.channel.send(embed=embed)

    # Original collection request when bot is mentioned
    if client.user.mentioned_in(message):
        cards = get_cards_from_txt('Example_request.txt')

        file_path = 'Collections/final_collection.csv'  # Updated path
        collection = get_cards_from_csv(file_path)

        # Only show requester's collection, not all owners
        username = str(message.author.display_name)
        await message.channel.send(request_owners(cards, collection, specific_owner=username))


if TOKEN:
    client.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN environment variable not set!")
