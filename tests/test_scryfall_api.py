"""
Test Scryfall API functionality - Core card lookup and data extraction.
"""

import sys
import asyncio
import json
from unittest.mock import patch, AsyncMock

# Fix imports for tests directory
from test_utils import fix_test_imports
fix_test_imports()

from scryfall_api import ScryfallAPI, get_card_price_eur, get_card_image_url


def test_scryfall_api():
    """Test Scryfall API functionality."""
    print("🧪 Testing Scryfall API...")
    
    # Test data - sample card response
    sample_card_data = {
        "name": "Lightning Bolt",
        "mana_cost": "{R}",
        "type_line": "Instant",
        "oracle_text": "Lightning Bolt deals 3 damage to any target.",
        "prices": {
            "eur": "0.50",
            "usd": "0.75"
        },
        "image_uris": {
            "normal": "https://cards.scryfall.io/normal/front/sample.jpg",
            "small": "https://cards.scryfall.io/small/front/sample.jpg"
        }
    }
    
    # Test price extraction
    print("Testing price extraction...")
    eur_price = get_card_price_eur(sample_card_data)
    if eur_price == "0.50":
        print("✅ EUR price extraction works correctly")
    else:
        print(f"❌ EUR price extraction failed: expected '0.50', got '{eur_price}'")
    
    # Test price extraction with missing EUR price
    no_eur_data = {
        "prices": {
            "usd": "0.75"
        }
    }
    eur_price_missing = get_card_price_eur(no_eur_data)
    if eur_price_missing is None:
        print("✅ Handles missing EUR price correctly")
    else:
        print(f"❌ Should return None for missing EUR price, got '{eur_price_missing}'")
    
    # Test image URL extraction
    print("Testing image URL extraction...")
    image_url = get_card_image_url(sample_card_data)
    expected_url = "https://cards.scryfall.io/normal/front/sample.jpg"
    if image_url == expected_url:
        print("✅ Image URL extraction works correctly")
    else:
        print(f"❌ Image URL extraction failed: expected '{expected_url}', got '{image_url}'")
    
    # Test image URL extraction with missing images
    no_image_data = {
        "name": "Test Card"
    }
    image_url_missing = get_card_image_url(no_image_data)
    if image_url_missing is None:
        print("✅ Handles missing image URLs correctly")
    else:
        print(f"❌ Should return None for missing images, got '{image_url_missing}'")
    
    # Test double-faced card image handling
    double_faced_data = {
        "card_faces": [
            {
                "image_uris": {
                    "normal": "https://cards.scryfall.io/normal/front/face1.jpg"
                }
            },
            {
                "image_uris": {
                    "normal": "https://cards.scryfall.io/normal/front/face2.jpg"
                }
            }
        ]
    }
    double_face_url = get_card_image_url(double_faced_data)
    expected_double_url = "https://cards.scryfall.io/normal/front/face1.jpg"
    if double_face_url == expected_double_url:
        print("✅ Double-faced card image extraction works correctly")
    else:
        print(f"❌ Double-faced card extraction failed: expected '{expected_double_url}', got '{double_face_url}'")


async def test_scryfall_api_calls():
    """Test actual API calls (mocked for reliability)."""
    print("\n🌐 Testing Scryfall API calls...")
    
    # Mock successful card lookup
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "name": "Lightning Bolt",
            "mana_cost": "{R}"
        })
        mock_get.return_value.__aenter__.return_value = mock_response
        
        result = await ScryfallAPI.get_card_by_name("Lightning Bolt")
        
        if result and result.get("name") == "Lightning Bolt":
            print("✅ Card lookup API call works correctly")
        else:
            print(f"❌ Card lookup failed: {result}")
    
    # Mock random card API
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "name": "Random Card",
            "type_line": "Creature"
        })
        mock_get.return_value.__aenter__.return_value = mock_response
        
        random_result = await ScryfallAPI.get_random_card()
        
        if random_result and random_result.get("name") == "Random Card":
            print("✅ Random card API call works correctly")
        else:
            print(f"❌ Random card lookup failed: {random_result}")
    
    # Mock API error handling
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response
        
        error_result = await ScryfallAPI.get_card_by_name("Nonexistent Card")
        
        if error_result is None:
            print("✅ API error handling works correctly")
        else:
            print(f"❌ Should return None for 404, got: {error_result}")


def test_edge_cases():
    """Test edge cases and error conditions."""
    print("\n🔧 Testing edge cases...")
    
    # Test with None input
    none_price = get_card_price_eur(None)
    none_image = get_card_image_url(None)
    
    if none_price is None and none_image is None:
        print("✅ Handles None input correctly")
    else:
        print(f"❌ None input handling failed: price={none_price}, image={none_image}")
    
    # Test with empty dict
    empty_price = get_card_price_eur({})
    empty_image = get_card_image_url({})
    
    if empty_price is None and empty_image is None:
        print("✅ Handles empty dict correctly")
    else:
        print(f"❌ Empty dict handling failed: price={empty_price}, image={empty_image}")
    
    # Test with malformed data
    malformed_data = {
        "prices": "not a dict",
        "image_uris": "not a dict"
    }
    
    try:
        malformed_price = get_card_price_eur(malformed_data)
        malformed_image = get_card_image_url(malformed_data)
        print("✅ Handles malformed data gracefully")
    except Exception as e:
        print(f"❌ Malformed data caused exception: {e}")


async def main():
    """Run all tests."""
    print("🚀 Starting Scryfall API Tests...\n")
    
    test_scryfall_api()
    await test_scryfall_api_calls()
    test_edge_cases()
    
    print("\n🎉 Scryfall API tests complete!")


if __name__ == "__main__":
    asyncio.run(main())
