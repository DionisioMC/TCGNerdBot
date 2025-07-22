"""Test achievements.py for syntax and runtime errors"""
import ast
import traceback

try:
    print("🔍 Checking achievements.py for errors...")
    
    # Check syntax
    with open('achievements.py', 'r', encoding='utf-8') as f:
        source = f.read()
    
    tree = ast.parse(source)
    print('✅ Syntax check passed - no syntax errors found')
    
    # Check imports and basic functionality
    import achievements
    print('✅ Import check passed - module imported successfully')
    
    # Test basic functionality
    manager = achievements.AchievementManager('test.json', 'test.csv')
    print(f'✅ Achievement manager initialized with {len(manager.achievements)} achievements')
    
    # Check for duplicate imports or other issues
    import_lines = []
    for i, line in enumerate(source.split('\n'), 1):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            import_lines.append((i, line.strip()))
    
    print(f"\n📋 Found {len(import_lines)} import statements:")
    for line_num, line in import_lines:
        print(f"  Line {line_num}: {line}")
    
    # Check for potential duplicate imports
    import_statements = [line for _, line in import_lines]
    duplicates = []
    for i, stmt in enumerate(import_statements):
        if import_statements.count(stmt) > 1 and stmt not in duplicates:
            duplicates.append(stmt)
    
    if duplicates:
        print(f"\n⚠️  Found duplicate imports:")
        for dup in duplicates:
            print(f"  {dup}")
    else:
        print("\n✅ No duplicate imports found")
        
    print("\n🎯 Overall: achievements.py appears to be working correctly!")
    
except SyntaxError as e:
    print(f'❌ Syntax error found: {e}')
    print(f'   Line {e.lineno}: {e.text}')
except Exception as e:
    print(f'❌ Runtime error: {e}')
    traceback.print_exc()
