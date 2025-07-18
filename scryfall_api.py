"""
Scryfall API interaction module for the TCG Nerd Bot.
Handles all communication with the Scryfall API for card data.
"""

import requests
from typing import Optional, Dict, Any
from config import SCRYFALL_API_BASE_URL, API_TIMEOUT


class ScryfallAPI:
    """Class to handle Scryfall API interactions."""
    
    BASE_URL = SCRYFALL_API_BASE_URL
    TIMEOUT = API_TIMEOUT
    
    @classmethod
    async def get_random_card(cls) -> Optional[Dict[str, Any]]:
        """
        Fetch a random card from Scryfall API.
        
        Returns:
            Dict containing card data or None if error occurred.
        """
        try:
            response = requests.get(f'{cls.BASE_URL}/cards/random', timeout=cls.TIMEOUT)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching random card: HTTP {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Network error fetching random card: {e}")
            return None
    
    @classmethod
    async def get_card_by_name(cls, card_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a specific card by name from Scryfall API.
        
        Args:
            card_name: The exact name of the card to search for.
            
        Returns:
            Dict containing card data or None if error occurred.
        """
        try:
            response = requests.get(
                f'{cls.BASE_URL}/cards/named?exact={card_name}', 
                timeout=cls.TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None  # Card not found
            else:
                print(f"Error fetching card '{card_name}': HTTP {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Network error fetching card '{card_name}': {e}")
            return None


def get_card_price_eur(card_data: Dict[str, Any]) -> Optional[str]:
    """
    Extract EUR price from card data.
    
    Args:
        card_data: Card data from Scryfall API.
        
    Returns:
        EUR price as string or None if not available.
    """
    prices = card_data.get('prices', {})
    return prices.get('eur')


def get_card_image_url(card_data: Dict[str, Any]) -> Optional[str]:
    """
    Extract image URL from card data.
    
    Args:
        card_data: Card data from Scryfall API.
        
    Returns:
        Image URL or None if not available.
    """
    image_uris = card_data.get('image_uris', {})
    return image_uris.get('normal')
