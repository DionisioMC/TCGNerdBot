"""
Simple test for the daily card functionality.
"""
import asyncio
from scryfall_api import ScryfallAPI
from discord_helpers import create_daily_card_embed

async def test_daily_card():
    """Test the daily card functionality."""
    print("🧪 Testing Daily Card functionality...")
    
    # Test getting a random card
    print("📡 Fetching random card from Scryfall...")
    card_data = await ScryfallAPI.get_random_card()
    
    if card_data:
        print(f"✅ Random card fetched: {card_data.get('name', 'Unknown')}")
        print(f"   Set: {card_data.get('set_name', 'Unknown')}")
        print(f"   Type: {card_data.get('type_line', 'Unknown')}")
        
        # Test embed creation
        try:
            embed = create_daily_card_embed(card_data)
            print("✅ Daily card embed created successfully")
            print(f"   Embed title: {embed.title}")
            print(f"   Number of fields: {len(embed.fields)}")
        except Exception as e:
            print(f"❌ Error creating embed: {e}")
    else:
        print("❌ Failed to fetch random card")

if __name__ == "__main__":
    asyncio.run(test_daily_card())
