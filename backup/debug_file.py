#!/usr/bin/env python3
"""
Debug script to find problematic lines in Example_request.txt
"""

def debug_file_parsing():
    try:
        with open('Example_request.txt', 'r') as file:
            lines = file.readlines()
        
        print(f"Total lines: {len(lines)}")
        
        problematic_lines = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                problematic_lines.append(f"Line {i}: Empty line")
            elif ' ' not in stripped:
                problematic_lines.append(f"Line {i}: No space found - '{stripped}'")
            else:
                # Test the split operation
                try:
                    after_parentheses = stripped.split(' (')[0]
                    parts = after_parentheses.split(' ', 1)
                    if len(parts) < 2:
                        problematic_lines.append(f"Line {i}: Split failed - '{stripped}' -> {parts}")
                    else:
                        # This line should be fine
                        pass
                except Exception as e:
                    problematic_lines.append(f"Line {i}: Exception - '{stripped}' - {e}")
        
        if problematic_lines:
            print("Problematic lines found:")
            for line in problematic_lines:
                print(line)
        else:
            print("No problematic lines found in parsing logic")
            
        # Test the actual line_cleaner function
        print("\nTesting line_cleaner function...")
        cards = [card.strip() for card in lines]
        cards = [card.split(' (')[0] for card in cards]
        print(f"After removing parentheses: {len(cards)} lines")
        
        cards_split = []
        for i, card in enumerate(cards):
            try:
                split_result = card.split(' ', 1)
                cards_split.append(split_result)
                if len(split_result) < 2:
                    print(f"Line {i+1}: Split issue - '{card}' -> {split_result}")
            except Exception as e:
                print(f"Line {i+1}: Exception during split - '{card}' - {e}")
        
        print(f"Split completed: {len(cards_split)} entries")
        
        # Test dictionary creation
        final_cards = []
        for i, card in enumerate(cards_split):
            try:
                if len(card) >= 2:
                    final_cards.append({'Number': card[0], 'Name': card[1]})
                else:
                    print(f"Line {i+1}: Cannot create dict - {card}")
            except Exception as e:
                print(f"Line {i+1}: Exception creating dict - {card} - {e}")
        
        print(f"Final result: {len(final_cards)} cards processed")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_file_parsing()
