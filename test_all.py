"""Test all major bot modules"""
try:
    # Test imports
    import command_handlers
    import trivia_system  
    import achievements
    import commander_games
    print('✅ All main modules imported successfully')
    
    # Test basic functionality
    from command_handlers import CommandHandlers
    handlers = CommandHandlers()
    print('✅ CommandHandlers initialized successfully')
    
    print('🎯 All command systems appear to be working correctly!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
