"""
Test script to verify archetype reaction functionality is properly implemented.
"""

import sys
import inspect

# Fix imports for tests directory
from test_utils import fix_test_imports
fix_test_imports()

from command_handlers import CommandHandlers
from commander_games import commander_manager
import discord

def test_archetype_reaction_setup():
    """Test if all archetype reaction components are properly set up."""
    print("🧪 Testing Archetype Reaction Setup...")
    
    # Check if CommandHandlers has the new method
    if hasattr(CommandHandlers, 'handle_archetype_reaction'):
        print("✅ handle_archetype_reaction method exists")
        
        # Check method signature
        method = getattr(CommandHandlers, 'handle_archetype_reaction')
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())
        
        if 'reaction' in params and 'user' in params:
            print("✅ handle_archetype_reaction has correct parameters")
        else:
            print("❌ handle_archetype_reaction has incorrect parameters")
    else:
        print("❌ handle_archetype_reaction method missing!")
    
    # Check if CommandHandlers has archetype_messages tracking
    dummy_client = type('DummyClient', (), {})()
    handlers = CommandHandlers(dummy_client, 123456)
    
    if hasattr(handlers, 'archetype_messages'):
        print("✅ archetype_messages tracking initialized")
    else:
        print("❌ archetype_messages tracking missing!")
    
    # Check if commander_manager has set_archetype method
    if hasattr(commander_manager, 'set_archetype'):
        print("✅ set_archetype method exists in commander_manager")
        
        # Check method signature
        method = getattr(commander_manager, 'set_archetype')
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())
        
        if 'game_id' in params and 'user_id' in params and 'archetype' in params:
            print("✅ set_archetype has correct parameters")
        else:
            print("❌ set_archetype has incorrect parameters")
    else:
        print("❌ set_archetype method missing from commander_manager!")
    
    # Check if required imports exist
    try:
        from commander_games import create_archetype_selection_embed, get_archetype_emojis
        print("✅ Archetype embed functions importable")
    except ImportError as e:
        print(f"❌ Archetype embed functions missing: {e}")
    
    print("\n🎉 Archetype reaction setup test complete!")

if __name__ == "__main__":
    test_archetype_reaction_setup()
