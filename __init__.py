"""
TCG Nerd Bot - A Discord bot for Magic: The Gathering card collection management.

This package contains modules for handling Discord bot functionality,
Scryfall API interactions, and card collection management.
"""

__version__ = "2.0.0"
__author__ = "TCG Nerd Bot Team"

# Package imports for easier access
from .scryfall_api import ScryfallAPI
from .discord_helpers import *
from .daily_card import post_daily_card, daily_card_task
from .command_handlers import CommandHandlers
from .config import *
