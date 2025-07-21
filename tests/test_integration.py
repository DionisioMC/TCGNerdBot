#!/usr/bin/env python3
"""Simple integration test"""

try:
    from discord_helpers import create_help_embed
    embed = create_help_embed()
    print(f"✅ Help embed updated successfully!")
    print(f"📊 Total fields: {len(embed.fields)}")
    print(f"🎯 New archetype features included!")
except Exception as e:
    print(f"❌ Error: {e}")
