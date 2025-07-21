#!/usr/bin/env python3
"""
Test script to debug Tags extraction from EDHREC data.
"""

from edhrec_api import edhrec_api
import json

def test_tags_extraction():
    print("🔬 Testing Tags extraction from EDHREC data...")
    
    commander_name = "Atraxa, Praetors' Voice"
    print(f"🎯 Testing: {commander_name}")
    
    # Get commander data
    commander_data = edhrec_api.get_commander_data(commander_name)
    
    if not commander_data:
        print("   ❌ No commander data found")
        return
    
    print("   📊 Commander data structure:")
    print(f"      Root keys: {list(commander_data.keys())}")
    
    container = commander_data.get("container", {})
    print(f"      Container keys: {list(container.keys())}")
    
    if "panels" in container:
        panels = container.get("panels", {})
        print(f"      Panels keys: {list(panels.keys())}")
        
        if "links" in panels:
            links = panels.get("links", [])
            print(f"      Found {len(links)} link sections")
            
            tags_found = False
            for i, link_section in enumerate(links):
                header = link_section.get("header", "")
                items = link_section.get("items", [])
                print(f"         Section {i}: '{header}' ({len(items)} items)")
                
                if header == "Tags":
                    tags_found = True
                    print(f"         🏷️ Found Tags section with {len(items)} items:")
                    for j, item in enumerate(items[:10]):  # Show first 10 tags
                        tag_value = item.get("value", "")
                        cleaned_tag = edhrec_api._clean_tag_name(tag_value)
                        print(f"            {j+1}. '{tag_value}' → '{cleaned_tag}'")
                    
                    if len(items) > 10:
                        print(f"            ... and {len(items) - 10} more tags")
            
            if not tags_found:
                print("      ❌ No Tags section found in links")
        else:
            print("      ❌ No 'links' key in panels")
    else:
        print("      ❌ No 'panels' key in container")
        
        # Let's check if it's in the json_dict instead
        json_dict = container.get("json_dict", {})
        print(f"      json_dict keys: {list(json_dict.keys())}")
        
        # Check cardlists for alternative data
        cardlists = json_dict.get("cardlists", [])
        print(f"      Found {len(cardlists)} cardlists")
    
    # Test archetype extraction
    print("\n🧪 Testing archetype extraction...")
    archetypes_data = edhrec_api.get_commander_archetypes(commander_name)
    
    if archetypes_data:
        archetypes = archetypes_data.get('archetypes', [])
        most_popular = archetypes_data.get('most_popular', '')
        print(f"   ✅ Archetypes found: {archetypes[:5]}...")
        print(f"   🎭 Most Popular: {most_popular}")
    else:
        print("   ❌ No archetype data found")

if __name__ == "__main__":
    test_tags_extraction()
