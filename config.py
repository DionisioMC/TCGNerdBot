"""
Configuration file for the TCG Nerd Bot.
Contains constants and configuration settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER = os.getenv('DISCORD_SERVER')

# File paths
COLLECTION_PATH = 'Collections/final_collection.csv'
EXAMPLE_REQUEST_PATH = 'Example_request.txt'

# API settings
SCRYFALL_API_BASE_URL = "https://api.scryfall.com"
API_TIMEOUT = 10

# Daily card settings
DAILY_CARD_TIME_HOUR = 10  # 10 AM
DAILY_CARD_TIME_MINUTE = 0

# Discord message limits
MAX_MESSAGE_LENGTH = 1900  # Discord limit is 2000, leave some buffer

# Channel name preferences for daily cards
PREFERRED_CHANNEL_NAMES = ['general', 'chat', 'main', 'cards', 'daily']

# Rarity emojis
RARITY_EMOJIS = {
    'common': '⚪',
    'uncommon': '🔵', 
    'rare': '🟡',
    'mythic': '🔴',
    'special': '🌟'
}

# Color emojis
COLOR_EMOJIS = {
    'white': '⚪', 
    'blue': '🔵', 
    'black': '⚫',
    'red': '🔴', 
    'green': '🟢', 
    'colorless': '⚪', 
    'multicolor': '🌈'
}

# Discord embed colors
EMBED_COLORS = {
    'daily_card': 0xffd700,
    'set_stats': 0x00ff00,
    'collection_overview': 0x00d4aa,
    'comparison': 0xff9900,
    'help': 0x00ffff,
    'card_ownership': 0x9932cc,
    'success': 0x00ff00
}
