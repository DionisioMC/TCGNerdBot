"""
EDHREC API interaction module for the TCG Nerd Bot.
Handles communication with EDHREC website for commander archetype data.
Based on the pyedhrec library approach.
"""

import requests
import re
import json
import random
from typing import Optional, Dict, List, Any
from config import API_TIMEOUT


# User agents for web scraping (similar to pyedhrec)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Safari/605.1.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.3'
]


def get_random_user_agent() -> str:
    """Get a random user agent for requests."""
    return random.choice(USER_AGENTS)


class EDHRECAPI:
    """Class to handle EDHREC website interactions using web scraping approach."""
    
    BASE_URL = "https://edhrec.com"
    TIMEOUT = API_TIMEOUT
    DEFAULT_BUILD_ID = "mI7k8IZ23x74LocK_h-qe"  # Fallback build ID from pyedhrec
    
    def __init__(self):
        """Initialize the EDHREC API client."""
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "application/json",
            "User-Agent": get_random_user_agent()
        }
        self.current_build_id = None
    
    @staticmethod
    def format_card_name(card_name: str) -> str:
        """
        Format card name for EDHREC URLs (based on pyedhrec implementation).
        
        Args:
            card_name: Raw commander name
            
        Returns:
            Formatted name for EDHREC URLs
        """
        # card names are all lower case
        card_name = card_name.lower()
        # Spaces need to be converted to hyphens
        card_name = card_name.replace(" ", "-")
        # remove apostrophes
        card_name = card_name.replace("'", "")
        # remove commas
        card_name = card_name.replace(",", "")
        return card_name
    
    def get_build_id(self) -> Optional[str]:
        """
        Get the current NextJS build ID from EDHREC homepage.
        
        Returns:
            Build ID string or None if not found
        """
        try:
            response = self.session.get(self.BASE_URL, timeout=self.TIMEOUT)
            response.raise_for_status()
            
            home_page_content = response.text
            script_block_regex = r'<script id="__NEXT_DATA__" type="application/json">(.*)</script>'
            script_matches = re.findall(script_block_regex, home_page_content)
            
            if script_matches:
                props_str = script_matches[0]
                try:
                    props_data = json.loads(props_str)
                    return props_data.get("buildId")
                except json.JSONDecodeError:
                    return None
            return None
            
        except requests.RequestException as e:
            print(f"Error fetching build ID: {e}")
            return None
    
    def check_build_id(self) -> bool:
        """
        Ensure we have a valid build ID.
        
        Returns:
            True if build ID is available
        """
        if not self.current_build_id:
            self.current_build_id = self.get_build_id()
            # If we couldn't get the current buildId we'll try to fall back to a known static string
            if not self.current_build_id:
                self.current_build_id = self.DEFAULT_BUILD_ID
        return True
    
    def build_nextjs_uri(self, endpoint: str, card_name: str, theme: str = None) -> tuple:
        """
        Build NextJS data URI for EDHREC API requests.
        
        Args:
            endpoint: API endpoint (e.g., 'commanders')
            card_name: Commander name
            theme: Optional theme filter
            
        Returns:
            Tuple of (URI, query_params)
        """
        self.check_build_id()
        formatted_card_name = self.format_card_name(card_name)
        
        query_params = {
            "commanderName": formatted_card_name
        }
        
        uri = f"{self.BASE_URL}/_next/data/{self.current_build_id}/{endpoint}/{formatted_card_name}"
        
        if theme:
            uri += f"/{theme}"
            query_params["themeName"] = theme
        else:
            uri += ".json"
        
        return uri, query_params
    
    @staticmethod
    def extract_nextjs_data(response_data: Dict) -> Optional[Dict]:
        """
        Extract data from NextJS response.
        
        Args:
            response_data: Raw response data
            
        Returns:
            Extracted data or None
        """
        if "pageProps" in response_data:
            return response_data.get("pageProps", {}).get("data")
        return None
    
    def get_commander_data(self, commander_name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch commander data from EDHREC using NextJS API.
        
        Args:
            commander_name: The name of the commander to search for.
            
        Returns:
            Dict containing commander data or None if error occurred.
        """
        try:
            commander_uri, params = self.build_nextjs_uri("commanders", commander_name)
            response = self.session.get(commander_uri, params=params, timeout=self.TIMEOUT)
            
            if response.status_code == 200:
                response_data = response.json()
                data = self.extract_nextjs_data(response_data)
                return data
            elif response.status_code == 404:
                print(f"Commander not found on EDHREC: {commander_name}")
                return None
            else:
                print(f"Error fetching commander data: HTTP {response.status_code}")
                return None
                
        except requests.RequestException as e:
            print(f"Network error fetching commander data: {e}")
            return None
        except Exception as e:
            print(f"Error processing commander data: {e}")
            return None
    
    def get_commander_archetypes(self, commander_name: str) -> Optional[Dict[str, List[str]]]:
        """
        Get available archetypes for a commander from EDHREC.
        
        Args:
            commander_name: The name of the commander.
            
        Returns:
            Dict with 'archetypes' list and 'most_popular' string, or None if error.
        """
        try:
            commander_data = self.get_commander_data(commander_name)
            if not commander_data:
                return None
            
            # Extract archetype information from commander data
            container = commander_data.get("container", {})
            themes = container.get("themes", [])
            
            archetypes = []
            most_popular = None
            
            if themes:
                # Extract theme names as archetypes
                for theme in themes:
                    theme_name = theme.get("name", "")
                    if theme_name:
                        archetypes.append(theme_name)
                        
                # The first theme is usually the most popular
                if archetypes:
                    most_popular = archetypes[0]
            
            # If no themes found, try to extract from other sections
            if not archetypes:
                # Look for cardlist sections that might indicate archetypes
                json_dict = container.get("json_dict", {})
                cardlists = json_dict.get("cardlists", [])
                
                for cardlist in cardlists:
                    header = cardlist.get("header", "")
                    tag = cardlist.get("tag", "")
                    
                    # Map common cardlist tags to archetype names
                    tag_to_archetype = {
                        "topcards": "Value Engine",
                        "creatures": "Creature-based",
                        "instants": "Control",
                        "sorceries": "Spell-slinger", 
                        "artifacts": "Artifact",
                        "enchantments": "Enchantment",
                        "utilitylands": "Utility Lands",
                        "manaartifacts": "Ramp"
                    }
                    
                    if tag in tag_to_archetype:
                        archetype_name = tag_to_archetype[tag]
                        if archetype_name not in archetypes:
                            archetypes.append(archetype_name)
            
            # Provide fallback archetypes if none found
            if not archetypes:
                # Use our fallback archetypes based on commander identity
                identity = commander_data.get("identity", [])
                archetypes = self._get_fallback_archetypes_for_identity(identity)
                most_popular = archetypes[0] if archetypes else "Midrange"
            
            return {
                'archetypes': archetypes[:10],  # Limit to 10 archetypes
                'most_popular': most_popular or (archetypes[0] if archetypes else "Midrange")
            }
            
        except Exception as e:
            print(f"Error extracting archetypes for {commander_name}: {e}")
            return None
    
    def _get_fallback_archetypes_for_identity(self, identity: List[str]) -> List[str]:
        """
        Get fallback archetypes based on color identity.
        
        Args:
            identity: List of color symbols (e.g., ['W', 'U', 'B'])
            
        Returns:
            List of appropriate archetype names
        """
        # Map color combinations to likely archetypes
        identity_set = set(identity) if identity else set()
        
        base_archetypes = ["Midrange", "Control", "Aggro", "Combo"]
        
        # Add color-specific archetypes
        if 'W' in identity_set:
            base_archetypes.extend(["Tokens", "Lifegain", "Equipment"])
        if 'U' in identity_set:
            base_archetypes.extend(["Spell-slinger", "Draw-Go", "Artifacts"])
        if 'B' in identity_set:
            base_archetypes.extend(["Reanimator", "Sacrifice", "Aristocrats"])
        if 'R' in identity_set:
            base_archetypes.extend(["Burn", "Dragons", "Goblins"])
        if 'G' in identity_set:
            base_archetypes.extend(["Ramp", "Big Mana", "Elves"])
        
        # Remove duplicates and return
        return list(dict.fromkeys(base_archetypes))


# Create a global instance
edhrec_api = EDHRECAPI()


# Fallback archetypes with emojis (used when EDHREC API fails)
FALLBACK_ARCHETYPES = [
    "Aggro", "Control", "Combo", "Midrange", "Ramp", "Tokens", 
    "Voltron", "Tribal", "Reanimator", "Artifacts", "Enchantments", 
    "Spell-slinger", "Lifegain", "Mill", "Stax", "Big Mana", 
    "Dragons", "Elves", "Goblins", "Zombies", "Angels", "Vampires", 
    "Equipment", "Aristocrats"
]

# Emoji mappings for archetype selection
ARCHETYPE_EMOJIS = {
    "Aggro": "⚡",
    "Control": "🛡️", 
    "Combo": "🔄",
    "Midrange": "⚖️",
    "Ramp": "🌱",
    "Tokens": "👥",
    "Voltron": "🤖",
    "Tribal": "🏘️",
    "Reanimator": "💀",
    "Artifacts": "⚙️",
    "Enchantments": "✨",
    "Spell-slinger": "🎭",
    "Lifegain": "❤️",
    "Mill": "📚",
    "Stax": "🔒",
    "Big Mana": "💰",
    "Dragons": "🐉",
    "Elves": "🧝",
    "Goblins": "👹",
    "Zombies": "🧟",
    "Angels": "👼",
    "Vampires": "🧛",
    "Equipment": "⚔️",
    "Aristocrats": "👑"
}


def get_archetype_emoji(archetype: str) -> str:
    """Get emoji for an archetype."""
    return ARCHETYPE_EMOJIS.get(archetype, "🎯")


def normalize_archetype(archetype: str) -> str:
    """Normalize archetype names for consistency."""
    # Handle special case: Elves should be treated as Tribal
    if archetype.lower() in ['elves', 'elf']:
        return 'Tribal'
    return archetype
