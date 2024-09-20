import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

intent = discord.Intents.default()
intent.message_content = True
intent.members = True

client = discord.Client(intents=intent)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    
client.run(TOKEN)