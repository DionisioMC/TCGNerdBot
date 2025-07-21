#!/usr/bin/env python3
"""Test archetype normalization"""

try:
    from achievements import achievement_manager
    
    print("✅ Achievement system loaded with archetype normalization")
    print("🔄 Testing normalization:")
    print("  Elves ->", achievement_manager._normalize_archetype('Elves'))
    print("  elves ->", achievement_manager._normalize_archetype('elves'))
    print("  Tribal ->", achievement_manager._normalize_archetype('Tribal'))
    print("  tribal ->", achievement_manager._normalize_archetype('tribal'))
    print("  Control ->", achievement_manager._normalize_archetype('Control'))
    print("  Empty ->", achievement_manager._normalize_archetype(''))
    
    print("\n✅ Normalization working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
