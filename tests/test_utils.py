"""
Fix import paths for test files after reorganization.
"""

import os
import sys

def fix_test_imports():
    """Add parent directory to Python path for test imports."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(tests_dir)
    
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
        print(f"✅ Added parent directory to path: {parent_dir}")

# Call this at the start of test files
fix_test_imports()
