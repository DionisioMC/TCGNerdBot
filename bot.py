import os

import discord
import requests
import random
from dotenv import load_dotenv
from bs4 import BeautifulSoup

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
    if '[' and ']' in message.content:
        start = message.content.index('[') + 1
        card_name = message.content[start:message.content.index(']')].lower()
        api = requests.get(f'https://api.scryfall.com/cards/named?exact={card_name}')
        data = api.json()
        if api.status_code == 404:
            responses = ["The card doesn't exist, try again, bitch", "You fucked up", "Billions of years of evolution for you to not being able to type a card name correctly? We are doomed...", "Good job buddy, thats not it"]
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
    elif '{' and '}' in message.content:
        start = message.content.index('{') + 1
        keyword = message.content[start:message.content.index('}')]
        URL = f'https://mtg.fandom.com/wiki/{keyword}'
        page = requests.get(URL)
        wiki = BeautifulSoup(page.content, 'html.parser')
        result = wiki.find('table').prettify()
        await message.channel.send(result)
    
    
client.run(TOKEN)