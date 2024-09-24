import os

import discord
import requests
import json
from dotenv import load_dotenv

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
        card_name = message.content[start:message.content.index(']')]
        api = requests.get(f'https://api.scryfall.com/cards/named?exact={card_name}')
        data = api.json()
        image = data['image_uris']['normal']
        await message.channel.send(image)
    
    
client.run(TOKEN)