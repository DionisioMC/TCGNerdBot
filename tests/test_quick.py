#!/usr/bin/env python3
"""Quick test for archetype achievements"""

try:
    from achievements import achievement_manager
    print("✅ Achievements module loaded successfully")
    print(f"📊 Total achievements: {len(achievement_manager.achievements)}")
    
    # Check for archetype achievements
    archetype_achievements = [k for k in achievement_manager.achievements.keys() 
                            if 'archetype' in k or k.endswith('_master')]
    print(f"🏆 Archetype achievements found: {len(archetype_achievements)}")
    
    for achievement in archetype_achievements:
        print(f"  - {achievement}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
