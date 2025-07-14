import os

import discord
import requests
import random
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from request_db import (get_cards_from_csv, get_cards_from_txt, request_owners,
                        get_set_stats, quick_rarity_comparison_by_owner, analyze_commander_sets_by_owner)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_SERVER')

intent = discord.Intents.default()
intent.message_content = True
intent.members = True

client = discord.Client(intents=intent)


@client.event
async def on_ready():

    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Card lookup with [card name]
    if '[' and ']' in message.content:
        start = message.content.index('[') + 1
        card_name = message.content[start:message.content.index(']')].lower()
        api = requests.get(
            f'https://api.scryfall.com/cards/named?exact={card_name}')
        data = api.json()
        if api.status_code == 404:
            responses = ["The card doesn't exist, try again, bitch", "You fucked up",
                         "Billions of years of evolution for you to not being able to type a card name correctly? We are doomed...", "Good job buddy, thats not it"]
            num = random.randint(0, len(responses) - 1)
            await message.channel.send(responses[num])
        elif 'price' in message.content:
            price = data['prices']['eur']
            await message.channel.send(price + ' euros')
        elif 'legal' in message.content:
            legal = data['legalities']['commander']
            await message.channel.send(legal)
        else:
            image = data['image_uris']['normal']
            await message.channel.send(image)

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
            value="`!setstats <SET>` - Get set statistics\n`!compare <SET>` - Compare your collection to a set\n`!commander` - Get Commander format recommendations",
            inline=False
        )

        embed.add_field(
            name="📁 File Upload",
            value="**Upload a .txt file** - Check who owns cards from your want list\n(Format: `1x Card Name` per line)",
            inline=False
        )

        embed.add_field(
            name="🎯 Examples",
            value="`!setstats MH3`\n`!compare OTJ`\n`!commander`\n`[Lightning Bolt]`\n`[Mana Crypt] price`\n📎 Upload `my_wants.txt`",
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


client.run(TOKEN)
