"""
Fix achievements.py field names in bulk
"""

# Read the file
with open('achievements.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count original issues
print("Original issues found:")
date_count = content.count("row['date']")
time_count = content.count("row['time']")
colors_count = content.count("row['colors']")
print(f"  row date: {date_count}")
print(f"  row time: {time_count}")  
print(f"  row colors: {colors_count}")

# Make replacements
# Replace date + time parsing
content = content.replace(
    "datetime.strptime(f\"{row['date']} {row['time']}\", '%Y-%m-%d %H:%M')",
    "datetime.strptime(row['game_date'], '%Y-%m-%d %H:%M:%S')"
)

# Replace game keys that use date_time_players format
content = content.replace(
    "f\"{row['date']}_{row['time']}_{row['total_players']}\"",
    "f\"{row['game_date']}_{row['total_players']}\""
)

# Replace any remaining colors references
content = content.replace("row['colors']", "row['commander_colors']")

# Write the file back
with open('achievements.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nBulk replacements completed!")
