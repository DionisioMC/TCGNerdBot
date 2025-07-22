"""Test upload command functionality"""
import sys
import traceback

try:
    from command_handlers import CommandHandlers
    from request_db import update_collection_with_owner_data
    print('✅ All imports successful')
    print('✅ CommandHandlers can be imported')
    print('✅ update_collection_with_owner_data function is available')
    
    # Test if the collection path exists
    from config import COLLECTION_PATH
    import os
    if os.path.exists(COLLECTION_PATH):
        print(f'✅ Collection path exists: {COLLECTION_PATH}')
    else:
        print(f'❌ Collection path missing: {COLLECTION_PATH}')
        
except Exception as e:
    print(f'❌ Import error: {e}')
    traceback.print_exc()
