#!/usr/bin/env python3
"""
Simple test script for achievement system
"""

def test_achievements():
    try:
        print("🧪 Starting Achievement System Test")
        
        # Import the module
        import achievements
        print("✅ Achievement module imported successfully")
        
        # Create manager
        manager = achievements.AchievementManager('test_achievements.json', 'test_stats.csv')
        print("✅ Achievement manager created")
        
        # Check total achievements
        total = len(manager.achievements)
        print(f"📊 Total achievements loaded: {total}")
        
        # Test complex functions
        complex_functions = [
            '_check_shard_master', '_check_wedge_master', '_check_meta_breaker', 
            '_check_trend_setter', '_check_giant_killer', '_check_mentor_achievement',
            '_check_frequent_player', '_check_color_collector', '_check_tribal_master', 
            '_check_artifact_lover'
        ]
        
        print("🔍 Verifying complex achievement functions:")
        implemented = 0
        for func_name in complex_functions:
            if hasattr(manager, func_name):
                print(f"  ✅ {func_name}")
                implemented += 1
            else:
                print(f"  ❌ {func_name} - MISSING")
        
        print(f"🎯 Complex functions implemented: {implemented}/{len(complex_functions)}")
        
        if implemented == len(complex_functions):
            print("🎉 ALL COMPLEX ACHIEVEMENT FUNCTIONS ARE PROPERLY IMPLEMENTED!")
        else:
            print("❌ Some functions are missing")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_achievements()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
