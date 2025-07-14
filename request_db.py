import csv
import requests


def check_card_in_db(db_data, card, owner=None):
    """
    Checks if a card exists in the database and optionally filters by owner.

    Args:
        db_data (list of dict): A list of dictionaries representing the database, 
                                where each dictionary contains card information.if __name__ == "__main__":
    cards = get_cards_from_txt('Example_request.txt')

    file_path = 'Colections//final_colection.csv'
    colection = get_cards_from_csv(file_path)

    # get_known_owners(colection)
    # request_owners(cards, colection)
    # # request_owners(cards, colection, specific_owner='XorVitor')

    # Test set statistics
    set_code = 'FIN'  # Finale Dominaria United
    set_stats = get_set_stats(set_code)

    # Compare your collection to the set
    if set_stats:
        compare_collection_to_set(colection, set_code)rd (dict): A dictionary containing the card details to search for. 
                     Must include a 'Name' key.
        owner (str, optional): The owner to filter the search by. Defaults to None.

    Returns:
        list: A list of owners for the matching cards. If `owner` is specified, 
              only the matching owner's name is returned in the list.
    """
    list_owner = []
    for card_db in db_data:
        if card['Name'].lower() in card_db['Name'].lower():
            if owner:
                if card_db['Owner'] == owner:
                    list_owner.append(card_db['Owner'])
            else:
                list_owner.append(card_db['Owner'])
    return list_owner


def line_cleaner(lines):
    """
    Cleans and processes a list of card information strings.

    This function performs the following operations on the input list of strings:
    1. Removes any trailing newline characters (`\n`) from each line.
    2. Removes any text that comes after the first occurrence of ' (' in each line.
    3. Splits each line into two parts: the card number and the card name.
    4. Converts the processed lines into a list of dictionaries, where each dictionary
       contains the card number and name with the keys 'Number' and 'Name', respectively.

    Args:
        lines (list of str): A list of strings, where each string represents a card's information.

    Returns:
        list of dict: A list of dictionaries, where each dictionary contains:
            - 'Number' (str): The card's number.
            - 'Name' (str): The card's name.
    """
    # remove the '\n' from the end of the line
    cards = [card.strip() for card in lines]
    # remove all what cames after the (
    cards = [card.split(' (')[0] for card in cards]
    # separate the number from the name of the card
    cards = [card.split(' ', 1) for card in cards]
    # create a list of dictionaries with the cards
    cards = [{'Number': card[0], 'Name': card[1]} for card in cards]
    # print(cards)
    return cards


def get_cards_from_txt(file_path):
    """
    Reads a text file containing a list of card numbers and names, and processes the content.

    Args:
        file_path (str): The path to the text file containing the card information.

    Returns:
        list: A cleaned list of card information after processing each line.
    """
    # read a txt file with a list of number and name o the cards
    with open(file_path, 'r') as file:
        cards = file.readlines()
    return line_cleaner(cards)


def get_cards_from_csv(file_path):
    """
    Reads a CSV file and returns a collection of rows as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file to be read.

    Returns:
        list[dict]: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        colection = [row for row in csv_reader]
    return colection


def request_owners(cards, colection, specific_owner=None):
    """
    Searches for card owners in a database and organizes the results.

    Args:
        cards (list): A list of dictionaries representing cards. Each dictionary should contain a 'Name' key.
        colection (object): The database or collection to search for card ownership.
        specific_owner (str, optional): A specific owner to filter the search. Defaults to None.

    Returns:
        None: The function prints the results directly, including:
            - Cards found in the database and their respective owners.
            - A summary of owners and the cards they own.
            - A list of unique cards found in the database.
    """
    list_foundeds = []
    dict_card_by_owners = {}
    result = ""
    for card in cards:
        list_owners = check_card_in_db(colection, card, specific_owner)
        if not list_owners == []:
            unique_owners = list(set(list_owners))
            for owner in unique_owners:
                if owner not in dict_card_by_owners:
                    dict_card_by_owners[owner] = []
                dict_card_by_owners[owner].append(card['Name'])
            print(
                f"{card['Name']} found in the database. Owners: {', '.join(unique_owners)}")
            list_foundeds.append(card['Name'])
    for owner in dict_card_by_owners:
        result += f"Owner: {owner}, Cards: {', '.join(dict_card_by_owners[owner])}\n"
    return result


def get_known_owners(colection):
    """
    Prints the unique owners of cards in the given collection.

    Args:
        colection (list of dict): A list of dictionaries where each dictionary 
                                  represents a card and contains an 'Owner' key.

    Returns:
        None
    """
    print('Known owners:')
    owners = set()
    for card in colection:
        owners.add(card['Owner'])
    for owner in owners:
        print(owner)


def get_cards_of_set(colection, set_name):
    """
    Retrieves cards from a collection that belong to a specific set.

    Args:
        colection (list of dict): A list of dictionaries representing the card collection.
        set_name (str): The name of the set to filter cards by.

    Returns:
        list: A list of dictionaries representing the cards in the specified set.
    """
    return [card for card in colection if (card['Set name'].lower() == set_name.lower() or card['Set code'].lower() == set_name.lower())]


def get_set_stats(set_code):
    """
    Get comprehensive statistics for a Magic: The Gathering set including rarity breakdown and color distribution.

    Args:
        set_code (str): The 3-letter set code (e.g., 'FIN', 'MOM', 'ONE')

    Returns:
        dict: A dictionary containing set statistics including rarity and color breakdowns
    """
    api = requests.get(f'https://mtgjson.com/api/v5/{set_code}.json')

    if api.status_code != 200:
        print(f"Error: Set {set_code} not found or API error.")
        return None

    set_data = api.json()['data']
    cards = set_data.get('cards', [])

    # Basic set info
    set_name = set_data.get('name', 'Unknown')
    release_date = set_data.get('releaseDate', 'Unknown')
    total_cards = len(cards)

    # Initialize counters
    rarity_count = {'common': 0, 'uncommon': 0,
                    'rare': 0, 'mythic': 0, 'special': 0}
    color_count = {'white': 0, 'blue': 0, 'black': 0,
                   'red': 0, 'green': 0, 'colorless': 0, 'multicolor': 0}
    type_count = {'creature': 0, 'instant': 0, 'sorcery': 0, 'enchantment': 0,
                  'artifact': 0, 'planeswalker': 0, 'land': 0, 'other': 0}

    # Process each card
    for card in cards:
        # Count rarities
        rarity = card.get('rarity', '').lower()
        if rarity in rarity_count:
            rarity_count[rarity] += 1
        else:
            rarity_count['special'] += 1

        # Count colors
        colors = card.get('colors', [])
        if not colors:
            color_count['colorless'] += 1
        elif len(colors) == 1:
            color_map = {'W': 'white', 'U': 'blue',
                         'B': 'black', 'R': 'red', 'G': 'green'}
            for color in colors:
                if color in color_map:
                    color_count[color_map[color]] += 1
        else:
            color_count['multicolor'] += 1

        # Count card types
        type_line = card.get('type', '').lower()
        if 'creature' in type_line:
            type_count['creature'] += 1
        elif 'instant' in type_line:
            type_count['instant'] += 1
        elif 'sorcery' in type_line:
            type_count['sorcery'] += 1
        elif 'enchantment' in type_line:
            type_count['enchantment'] += 1
        elif 'artifact' in type_line:
            type_count['artifact'] += 1
        elif 'planeswalker' in type_line:
            type_count['planeswalker'] += 1
        elif 'land' in type_line:
            type_count['land'] += 1
        else:
            type_count['other'] += 1

    # Create results dictionary
    stats = {
        'set_info': {
            'name': set_name,
            'code': set_code.upper(),
            'release_date': release_date,
            'total_cards': total_cards
        },
        'rarity_breakdown': rarity_count,
        'color_breakdown': color_count,
        'type_breakdown': type_count
    }

    # Print formatted results
    print(f"\n=== SET STATISTICS: {set_name} ({set_code.upper()}) ===")
    print(f"Release Date: {release_date}")
    print(f"Total Cards: {total_cards}")

    print("\n--- RARITY BREAKDOWN ---")
    for rarity, count in rarity_count.items():
        if count > 0:
            percentage = (count / total_cards) * 100
            print(f"{rarity.capitalize()}: {count} ({percentage:.1f}%)")

    print("\n--- COLOR BREAKDOWN ---")
    for color, count in color_count.items():
        if count > 0:
            percentage = (count / total_cards) * 100
            print(f"{color.capitalize()}: {count} ({percentage:.1f}%)")

    print("\n--- TYPE BREAKDOWN ---")
    for card_type, count in type_count.items():
        if count > 0:
            percentage = (count / total_cards) * 100
            print(f"{card_type.capitalize()}: {count} ({percentage:.1f}%)")

    return stats


def compare_collection_to_set(colection, set_code):
    """
    Compare your collection to the official set statistics to see completion percentage.

    Args:
        colection (list): Your card collection from CSV
        set_code (str): The 3-letter set code to compare against

    Returns:
        dict: Comparison statistics
    """
    # Get official set stats
    set_stats = get_set_stats(set_code)
    if not set_stats:
        return None

    # Get your cards from this set
    your_cards = get_cards_of_set(colection, set_code)

    if not your_cards:
        print(
            f"\nYou don't have any cards from set {set_code} in your collection.")
        return None

    # Initialize your collection counters
    your_rarity = {'common': 0, 'uncommon': 0,
                   'rare': 0, 'mythic': 0, 'special': 0}

    # Count your cards by rarity
    for card in your_cards:
        rarity = card.get('Rarity', '').lower()
        if rarity in your_rarity:
            your_rarity[rarity] += 1
        else:
            your_rarity['special'] += 1

    # Get color breakdown using API calls
    your_colors = analyze_collection_colors(your_cards)

    # Calculate completion percentages
    total_you_have = len(your_cards)
    total_in_set = set_stats['set_info']['total_cards']
    overall_completion = (total_you_have / total_in_set) * 100

    print(f"\n=== COLLECTION COMPARISON: {set_stats['set_info']['name']} ===")
    print(
        f"Your cards: {total_you_have} / {total_in_set} ({overall_completion:.1f}% complete)")

    print("\n--- RARITY COMPLETION ---")
    for rarity in your_rarity:
        you_have = your_rarity[rarity]
        set_has = set_stats['rarity_breakdown'][rarity]
        if set_has > 0:
            completion = (you_have / set_has) * 100
            print(f"{rarity.capitalize()}: {you_have}/{set_has} ({completion:.1f}%)")

    print("\n--- COLOR COMPLETION ---")
    for color in your_colors:
        you_have = your_colors[color]
        set_has = set_stats['color_breakdown'][color]
        if set_has > 0:
            completion = (you_have / set_has) * 100
            print(f"{color.capitalize()}: {you_have}/{set_has} ({completion:.1f}%)")

    return {
        'your_total': total_you_have,
        'set_total': total_in_set,
        'completion_percentage': overall_completion,
        'your_rarity_breakdown': your_rarity,
        'your_color_breakdown': your_colors
    }


def get_card_color_identity(card_name, set_code=None):
    """
    Get color identity for a card using Scryfall API.

    Args:
        card_name (str): The name of the card
        set_code (str, optional): Set code to help with exact matching

    Returns:
        list: Color identity as list of letters (e.g., ['W', 'U'] for Azorius)
    """
    try:
        # Use exact name search on Scryfall
        if set_code:
            url = f'https://api.scryfall.com/cards/named?exact={card_name}&set={set_code}'
        else:
            url = f'https://api.scryfall.com/cards/named?exact={card_name}'

        response = requests.get(url)

        if response.status_code == 200:
            card_data = response.json()
            return card_data.get('color_identity', [])
        else:
            # If exact match fails, try fuzzy search
            url = f'https://api.scryfall.com/cards/named?fuzzy={card_name}'
            response = requests.get(url)
            if response.status_code == 200:
                card_data = response.json()
                return card_data.get('color_identity', [])
            else:
                print(
                    f"Warning: Could not find color identity for '{card_name}'")
                return []
    except Exception as e:
        print(f"Error getting color identity for '{card_name}': {e}")
        return []


def analyze_collection_colors(your_cards):
    """
    Analyze color distribution of your collection by fetching color identity from API.

    Args:
        your_cards (list): List of cards from your collection

    Returns:
        dict: Color breakdown of your collection
    """
    your_colors = {'white': 0, 'blue': 0, 'black': 0,
                   'red': 0, 'green': 0, 'colorless': 0, 'multicolor': 0}

    print("Analyzing color identity for your cards... (this may take a moment)")

    for i, card in enumerate(your_cards):
        if i % 10 == 0:  # Progress indicator
            print(f"Processing card {i+1}/{len(your_cards)}...")

        card_name = card.get('Name', '')
        set_code = card.get('Set code', '')

        # Get color identity from API
        color_identity = get_card_color_identity(card_name, set_code)

        # Categorize the card
        if not color_identity:
            your_colors['colorless'] += 1
        elif len(color_identity) == 1:
            color_map = {'W': 'white', 'U': 'blue',
                         'B': 'black', 'R': 'red', 'G': 'green'}
            color = color_identity[0]
            if color in color_map:
                your_colors[color_map[color]] += 1
        else:
            your_colors['multicolor'] += 1

        # Small delay to be respectful to the API
        import time
        time.sleep(0.1)

    return your_colors


def quick_rarity_comparison(colection, set_code):
    """
    Quick comparison that only analyzes rarity (no API calls needed).
    Use this for faster analysis when you don't need color data.

    Args:
        colection (list): Your card collection from CSV
        set_code (str): The 3-letter set code to compare against

    Returns:
        dict: Rarity comparison statistics
    """
    # Get official set stats
    set_stats = get_set_stats(set_code)
    if not set_stats:
        return None

    # Get your cards from this set
    your_cards = get_cards_of_set(colection, set_code)

    if not your_cards:
        print(
            f"\nYou don't have any cards from set {set_code} in your collection.")
        return None

    # Initialize your collection counters
    your_rarity = {'common': 0, 'uncommon': 0,
                   'rare': 0, 'mythic': 0, 'special': 0}

    # Count your cards by rarity
    for card in your_cards:
        rarity = card.get('Rarity', '').lower()
        if rarity in your_rarity:
            your_rarity[rarity] += 1
        else:
            your_rarity['special'] += 1

    # Calculate completion percentages
    total_you_have = len(your_cards)
    total_in_set = set_stats['set_info']['total_cards']
    overall_completion = (total_you_have / total_in_set) * 100

    print(
        f"\n=== QUICK RARITY COMPARISON: {set_stats['set_info']['name']} ===")
    print(
        f"Your cards: {total_you_have} / {total_in_set} ({overall_completion:.1f}% complete)")

    print("\n--- RARITY COMPLETION ---")
    for rarity in your_rarity:
        you_have = your_rarity[rarity]
        set_has = set_stats['rarity_breakdown'][rarity]
        if set_has > 0:
            completion = (you_have / set_has) * 100
            print(f"{rarity.capitalize()}: {you_have}/{set_has} ({completion:.1f}%)")

    return {
        'your_total': total_you_have,
        'set_total': total_in_set,
        'completion_percentage': overall_completion,
        'your_rarity_breakdown': your_rarity
    }


def filter_collection_by_owner(collection, owner_name):
    """
    Filter collection to only include cards owned by a specific person.

    Args:
        collection (list): Full collection from CSV
        owner_name (str): Name of the owner to filter by

    Returns:
        list: Filtered collection containing only the owner's cards
    """
    return [card for card in collection if card.get('Owner', '').lower() == owner_name.lower()]


def get_username_from_mention(message_content):
    """
    Extract username from Discord message. Handles @mentions and plain usernames.

    Args:
        message_content (str): Discord message content

    Returns:
        str: Username or None if not found
    """
    import re

    # Look for patterns like "for @username" or "for username"
    patterns = [
        r'for\s+@?(\w+)',          # "for @username" or "for username"
        r'user\s+@?(\w+)',         # "user @username" or "user username"
        r'owner\s+@?(\w+)',        # "owner @username" or "owner username"
        r'@(\w+)',                 # Just "@username"
    ]

    for pattern in patterns:
        match = re.search(pattern, message_content, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def quick_rarity_comparison_by_owner(collection, set_code, owner_name=None):
    """
    Quick comparison that analyzes rarity for a specific owner (no API calls needed).

    Args:
        collection (list): Your card collection from CSV
        set_code (str): The 3-letter set code to compare against
        owner_name (str, optional): Filter by owner name. If None, uses full collection.

    Returns:
        dict: Rarity comparison statistics for the owner
    """
    # Filter collection by owner if specified
    if owner_name:
        owner_collection = filter_collection_by_owner(collection, owner_name)
        if not owner_collection:
            print(
                f"\nNo cards found for owner '{owner_name}' in the collection.")
            return None
    else:
        owner_collection = collection

    # Get official set stats
    set_stats = get_set_stats(set_code)
    if not set_stats:
        return None

    # Get owner's cards from this set
    your_cards = get_cards_of_set(owner_collection, set_code)

    if not your_cards:
        owner_text = f" for {owner_name}" if owner_name else ""
        print(
            f"\nNo cards from set {set_code} found{owner_text} in the collection.")
        return None

    # Initialize your collection counters
    your_rarity = {'common': 0, 'uncommon': 0,
                   'rare': 0, 'mythic': 0, 'special': 0}

    # Count your cards by rarity
    for card in your_cards:
        rarity = card.get('Rarity', '').lower()
        if rarity in your_rarity:
            your_rarity[rarity] += 1
        else:
            your_rarity['special'] += 1

    # Calculate completion percentages
    total_you_have = len(your_cards)
    total_in_set = set_stats['set_info']['total_cards']
    overall_completion = (total_you_have / total_in_set) * 100

    owner_text = f" ({owner_name})" if owner_name else ""
    print(
        f"\n=== QUICK RARITY COMPARISON: {set_stats['set_info']['name']}{owner_text} ===")
    print(
        f"Cards: {total_you_have} / {total_in_set} ({overall_completion:.1f}% complete)")

    print("\n--- RARITY COMPLETION ---")
    for rarity in your_rarity:
        you_have = your_rarity[rarity]
        set_has = set_stats['rarity_breakdown'][rarity]
        if set_has > 0:
            completion = (you_have / set_has) * 100
            print(f"{rarity.capitalize()}: {you_have}/{set_has} ({completion:.1f}%)")

    return {
        'your_total': total_you_have,
        'set_total': total_in_set,
        'completion_percentage': overall_completion,
        'your_rarity_breakdown': your_rarity,
        'owner_name': owner_name
    }


def analyze_commander_sets(colection, target_sets=None):
    """
    Analyze multiple sets to recommend which ones to focus on for Commander format.

    Args:
        colection (list): Your card collection from CSV
        target_sets (list, optional): Specific sets to analyze. If None, analyzes popular Commander sets.

    Returns:
        dict: Analysis results with recommendations
    """
    # Comprehensive Commander sets (recent and classic)
    if target_sets is None:
        target_sets = [
            # Recent High-Power Sets (2023-2025)
            'MH3',  # Modern Horizons 3 - High power level
            'BLB',  # Bloomburrow - Animal tribal
            'OTJ',  # Outlaws of Thunder Junction - Crime themes
            'MKM',  # Murders at Karlov Manor - Detective themes
            'LCI',  # Lost Caverns of Ixalan - Tribal support
            'WOE',  # Wilds of Eldraine - Adventure mechanics
            'LTR',  # Lord of the Rings - Commander popular
            'MOM',  # March of the Machine - Multiverse
            'ONE',  # Phyrexia: All Will Be One - High power

            # Commander Products & Legends Sets
            'CLB',  # Commander Legends: Battle for Baldur's Gate
            'NCC',  # New Capenna Commander
            'AFC',  # Adventures in the Forgotten Realms Commander
            'C21',  # Commander 2021
            'CMR',  # Commander Legends
            'C20',  # Commander 2020
            'C19',  # Commander 2019

            # Artifact & Historic Sets
            'BRO',  # The Brothers' War - Artifacts matter
            'NEO',  # Kamigawa: Neon Dynasty - Artifacts & enchantments
            'DMU',  # Dominaria United - Legends/Historic
            'DOM',  # Dominaria - Historic matters
            'KLD',  # Kaladesh - Artifacts & energy
            'AER',  # Aether Revolt - Artifacts

            # Multicolor & Guild Sets
            'SNC',  # Streets of New Capenna - 3-color families
            'GRN',  # Guilds of Ravnica
            'RNA',  # Ravnica Allegiance
            'WAR',  # War of the Spark - Planeswalkers
            'RTR',  # Return to Ravnica
            'GTC',  # Gatecrash
            'DGM',  # Dragon's Maze

            # Tribal & Theme Sets
            'IXL',  # Ixalan - Pirates, Vampires, Merfolk, Dinosaurs
            'RIX',  # Rivals of Ixalan
            'ISD',  # Innistrad - Humans, Zombies, Spirits
            'DKA',  # Dark Ascension
            'SOI',  # Shadows over Innistrad
            'EMN',  # Eldritch Moon
            'MID',  # Innistrad: Midnight Hunt
            'VOW',  # Innistrad: Crimson Vow
            'ZEN',  # Zendikar - Landfall
            'WWK',  # Worldwake
            'ROE',  # Rise of the Eldrazi
            'BFZ',  # Battle for Zendikar
            'OGW',  # Oath of the Gatewatch
            'ZNR',  # Zendikar Rising

            # High-Power Modern Sets
            'MH2',  # Modern Horizons 2
            'MH1',  # Modern Horizons
            'TSR',  # Time Spiral Remastered
            'UMA',  # Ultimate Masters
            'MM3',  # Modern Masters 2017
            'EMA',  # Eternal Masters

            # Specialty & Supplemental
            'CNS',  # Conspiracy
            'CN2',  # Conspiracy: Take the Crown
            'BBD',  # Battlebond - Partner mechanics
            '2X2',  # Double Masters 2022
            '2XM',  # Double Masters
            'JMP',  # Jumpstart

            # Wedge & Shard Sets
            'KTK',  # Khans of Tarkir - 3-color wedges
            'FRF',  # Fate Reforged
            'DTK',  # Dragons of Tarkir
            'ALA',  # Shards of Alara
            'CON',  # Conflux
            'ARB',  # Alara Reborn

            # Enchantment & God Sets
            'THS',  # Theros - Enchantments matter
            'BNG',  # Born of the Gods
            'JOU',  # Journey into Nyx
            'THB',  # Theros Beyond Death

            # Recent Standard with Commander Appeal
            'ELD',  # Throne of Eldraine
            'STX',  # Strixhaven - Spells matter
            'AFR',  # Adventures in the Forgotten Realms
            'KHM',  # Kaldheim - Norse mythology
        ]

    print("=== COMMANDER SET ANALYSIS ===")
    print("Analyzing sets for Commander format potential...\n")

    results = []

    for set_code in target_sets:
        try:
            # Get set stats
            set_stats = get_set_stats(set_code)
            if not set_stats:
                continue

            # Get your cards from this set
            your_cards = get_cards_of_set(colection, set_code)

            if not your_cards:
                completion_rate = 0
                rare_mythic_completion = 0
                total_you_have = 0
            else:
                # Calculate completion rates
                total_you_have = len(your_cards)
                total_in_set = set_stats['set_info']['total_cards']
                completion_rate = (total_you_have / total_in_set) * 100

                # Focus on rares and mythics for Commander
                your_rare_mythic = sum(1 for card in your_cards
                                       if card.get('Rarity', '').lower() in ['rare', 'mythic'])
                set_rare_mythic = set_stats['rarity_breakdown']['rare'] + \
                    set_stats['rarity_breakdown']['mythic']
                rare_mythic_completion = (
                    your_rare_mythic / set_rare_mythic * 100) if set_rare_mythic > 0 else 0

            # Commander relevance scoring
            commander_score = calculate_commander_score(set_stats, set_code)

            results.append({
                'set_code': set_code,
                'set_name': set_stats['set_info']['name'],
                'release_date': set_stats['set_info']['release_date'],
                'total_cards': set_stats['set_info']['total_cards'],
                'your_cards': total_you_have,
                'completion_rate': completion_rate,
                'rare_mythic_completion': rare_mythic_completion,
                'commander_score': commander_score,
                'recommendation_score': calculate_recommendation_score(completion_rate, rare_mythic_completion, commander_score)
            })

        except Exception as e:
            print(f"Error analyzing set {set_code}: {e}")
            continue

    # Sort by recommendation score
    results.sort(key=lambda x: x['recommendation_score'], reverse=True)

    # Display results
    print("=" * 80)
    print(f"{'SET':<8} {'NAME':<25} {'COMPLETE':<10} {'R/M%':<8} {'CMD':<5} {'SCORE':<7} {'RECOMMENDATION'}")
    print("=" * 80)

    for result in results:
        recommendation = get_recommendation_text(
            result['recommendation_score'])
        print(f"{result['set_code']:<8} {result['set_name'][:24]:<25} "
              f"{result['completion_rate']:.1f}%{'':<5} {result['rare_mythic_completion']:.1f}%{'':<4} "
              f"{result['commander_score']:<5} {result['recommendation_score']:.1f}{'':<4} {recommendation}")

    print("\n=== TOP 3 RECOMMENDATIONS FOR COMMANDER ===")
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. {result['set_name']} ({result['set_code']})")
        print(f"   • Overall completion: {result['completion_rate']:.1f}%")
        print(
            f"   • Rare/Mythic completion: {result['rare_mythic_completion']:.1f}%")
        print(f"   • Commander relevance: {result['commander_score']}/10")
        print(
            f"   • Why: {get_detailed_recommendation(result['set_code'], result)}")

    return results


def analyze_commander_sets_by_owner(collection, owner_name=None, target_sets=None):
    """
    Analyze multiple sets to recommend which ones to focus on for Commander format (filtered by owner).

    Args:
        collection (list): Your card collection from CSV
        owner_name (str, optional): Filter by owner name. If None, uses full collection.
        target_sets (list, optional): Specific sets to analyze. If None, analyzes popular Commander sets.

    Returns:
        dict: Analysis results with recommendations for the specific owner
    """
    # Filter collection by owner if specified
    if owner_name:
        owner_collection = filter_collection_by_owner(collection, owner_name)
        if not owner_collection:
            print(
                f"\nNo cards found for owner '{owner_name}' in the collection.")
            return None
        print(f"=== COMMANDER SET ANALYSIS FOR {owner_name.upper()} ===")
    else:
        owner_collection = collection
        print("=== COMMANDER SET ANALYSIS ===")

    # Comprehensive Commander sets (recent and classic)
    if target_sets is None:
        target_sets = [
            # Recent High-Power Sets (2023-2025)
            'MH3',  # Modern Horizons 3 - High power level
            'BLB',  # Bloomburrow - Animal tribal
            'OTJ',  # Outlaws of Thunder Junction - Crime themes
            'MKM',  # Murders at Karlov Manor - Detective themes
            'LCI',  # Lost Caverns of Ixalan - Tribal support
            'WOE',  # Wilds of Eldraine - Adventure mechanics
            'LTR',  # Lord of the Rings - Commander popular
            'MOM',  # March of the Machine - Multiverse
            'ONE',  # Phyrexia: All Will Be One - High power

            # Commander Products & Legends Sets
            'CLB',  # Commander Legends: Battle for Baldur's Gate
            'NCC',  # New Capenna Commander
            'AFC',  # Adventures in the Forgotten Realms Commander
            'C21',  # Commander 2021
            'CMR',  # Commander Legends
            'C20',  # Commander 2020
            'C19',  # Commander 2019

            # Artifact & Historic Sets
            'BRO',  # The Brothers' War - Artifacts matter
            'NEO',  # Kamigawa: Neon Dynasty - Artifacts & enchantments
            'DMU',  # Dominaria United - Legends/Historic
            'DOM',  # Dominaria - Historic matters
            'KLD',  # Kaladesh - Artifacts & energy
            'AER',  # Aether Revolt - Artifacts

            # Multicolor & Guild Sets
            'SNC',  # Streets of New Capenna - 3-color families
            'GRN',  # Guilds of Ravnica
            'RNA',  # Ravnica Allegiance
            'WAR',  # War of the Spark - Planeswalkers
            'RTR',  # Return to Ravnica
            'GTC',  # Gatecrash
            'DGM',  # Dragon's Maze

            # Tribal & Theme Sets
            'IXL',  # Ixalan - Pirates, Vampires, Merfolk, Dinosaurs
            'RIX',  # Rivals of Ixalan
            'ISD',  # Innistrad - Humans, Zombies, Spirits
            'DKA',  # Dark Ascension
            'SOI',  # Shadows over Innistrad
            'EMN',  # Eldritch Moon
            'MID',  # Innistrad: Midnight Hunt
            'VOW',  # Innistrad: Crimson Vow
            'ZEN',  # Zendikar - Landfall
            'WWK',  # Worldwake
            'ROE',  # Rise of the Eldrazi
            'BFZ',  # Battle for Zendikar
            'OGW',  # Oath of the Gatewatch
            'ZNR',  # Zendikar Rising

            # High-Power Modern Sets
            'MH2',  # Modern Horizons 2
            'MH1',  # Modern Horizons
            'TSR',  # Time Spiral Remastered
            'UMA',  # Ultimate Masters
            'MM3',  # Modern Masters 2017
            'EMA',  # Eternal Masters

            # Specialty & Supplemental
            'CNS',  # Conspiracy
            'CN2',  # Conspiracy: Take the Crown
            'BBD',  # Battlebond - Partner mechanics
            '2X2',  # Double Masters 2022
            '2XM',  # Double Masters
            'JMP',  # Jumpstart

            # Wedge & Shard Sets
            'KTK',  # Khans of Tarkir - 3-color wedges
            'FRF',  # Fate Reforged
            'DTK',  # Dragons of Tarkir
            'ALA',  # Shards of Alara
            'CON',  # Conflux
            'ARB',  # Alara Reborn

            # Enchantment & God Sets
            'THS',  # Theros - Enchantments matter
            'BNG',  # Born of the Gods
            'JOU',  # Journey into Nyx
            'THB',  # Theros Beyond Death

            # Recent Standard with Commander Appeal
            'ELD',  # Throne of Eldraine
            'STX',  # Strixhaven - Spells matter
            'AFR',  # Adventures in the Forgotten Realms
            'KHM',  # Kaldheim - Norse mythology
        ]

    print("Analyzing sets for Commander format potential...\n")

    results = []

    for set_code in target_sets:
        try:
            # Get set stats (suppress output by capturing it)
            import io
            import sys
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()

            set_stats = get_set_stats(set_code)

            sys.stdout = old_stdout  # Restore stdout

            if not set_stats:
                continue

            # Get owner's cards from this set
            your_cards = get_cards_of_set(owner_collection, set_code)

            if not your_cards:
                completion_rate = 0
                rare_mythic_completion = 0
                total_you_have = 0
            else:
                # Calculate completion rates
                total_you_have = len(your_cards)
                total_in_set = set_stats['set_info']['total_cards']
                completion_rate = (total_you_have / total_in_set) * 100

                # Focus on rares and mythics for Commander
                your_rare_mythic = sum(1 for card in your_cards
                                       if card.get('Rarity', '').lower() in ['rare', 'mythic'])
                set_rare_mythic = set_stats['rarity_breakdown']['rare'] + \
                    set_stats['rarity_breakdown']['mythic']
                rare_mythic_completion = (
                    your_rare_mythic / set_rare_mythic * 100) if set_rare_mythic > 0 else 0

            # Commander relevance scoring
            commander_score = calculate_commander_score(set_stats, set_code)

            results.append({
                'set_code': set_code,
                'set_name': set_stats['set_info']['name'],
                'release_date': set_stats['set_info']['release_date'],
                'total_cards': set_stats['set_info']['total_cards'],
                'your_cards': total_you_have,
                'completion_rate': completion_rate,
                'rare_mythic_completion': rare_mythic_completion,
                'commander_score': commander_score,
                'recommendation_score': calculate_recommendation_score(completion_rate, rare_mythic_completion, commander_score)
            })

        except Exception as e:
            print(f"Error analyzing set {set_code}: {e}")
            continue

    # Sort by recommendation score
    results.sort(key=lambda x: x['recommendation_score'], reverse=True)

    # Display results
    owner_text = f" FOR {owner_name.upper()}" if owner_name else ""
    print("=" * 80)
    print(f"{'SET':<8} {'NAME':<25} {'COMPLETE':<10} {'R/M%':<8} {'CMD':<5} {'SCORE':<7} {'RECOMMENDATION'}")
    print("=" * 80)

    for result in results:
        recommendation = get_recommendation_text(
            result['recommendation_score'])
        print(f"{result['set_code']:<8} {result['set_name'][:24]:<25} "
              f"{result['completion_rate']:.1f}%{'':<5} {result['rare_mythic_completion']:.1f}%{'':<4} "
              f"{result['commander_score']:<5} {result['recommendation_score']:.1f}{'':<4} {recommendation}")

    print(f"\n=== TOP 3 RECOMMENDATIONS FOR COMMANDER{owner_text} ===")
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. {result['set_name']} ({result['set_code']})")
        print(f"   • Overall completion: {result['completion_rate']:.1f}%")
        print(
            f"   • Rare/Mythic completion: {result['rare_mythic_completion']:.1f}%")
        print(f"   • Commander relevance: {result['commander_score']}/10")
        print(
            f"   • Why: {get_detailed_recommendation(result['set_code'], result)}")

    return results


def calculate_commander_score(set_stats, set_code):
    """
    Calculate a Commander format relevance score (1-10) based on set characteristics.
    """
    score = 5  # Base score

    # Higher scores for sets known to be Commander-relevant
    commander_sets = {
        'MH3': 9,   # Modern Horizons - always high power
        'LTR': 9,   # LOTR - extremely popular in Commander
        'CLB': 10,  # Commander Legends - designed for Commander
        'NCC': 9,   # Commander product
        'LCI': 8,   # Ixalan tribal themes
        'MOM': 8,   # Multiverse themes
        'ONE': 8,   # High power Phyrexian cards
        'WOE': 7,   # Adventure mechanics
        'BRO': 7,   # Artifact themes
        'DMU': 8,   # Legendary matters
    }

    if set_code in commander_sets:
        score = commander_sets[set_code]

    # Adjust based on multicolor percentage (Commander loves multicolor)
    multicolor_pct = (set_stats['color_breakdown']['multicolor'] /
                      set_stats['set_info']['total_cards']) * 100
    if multicolor_pct > 20:
        score += 1
    elif multicolor_pct > 15:
        score += 0.5

    # Adjust based on legendary/artifact density (rough approximation)
    creature_pct = (set_stats['type_breakdown'].get(
        'creature', 0) / set_stats['set_info']['total_cards']) * 100
    if creature_pct > 60:  # Creature-heavy sets often good for Commander
        score += 0.5

    return min(10, max(1, score))


def calculate_recommendation_score(completion_rate, rare_mythic_completion, commander_score):
    """
    Calculate an overall recommendation score for focusing on a set.
    Higher score = better target for investment.
    """
    # Lower completion = higher potential gain
    completion_factor = max(0, 100 - completion_rate) / 100

    # Lower rare/mithic completion = higher potential for valuable cards
    rare_mythic_factor = max(0, 100 - rare_mythic_completion) / 100

    # Commander relevance multiplier
    commander_factor = commander_score / 10

    # Weighted score: 40% completion gap, 40% rare/mythic gap, 20% commander relevance
    score = (completion_factor * 4 + rare_mythic_factor *
             4 + commander_factor * 2) * 10

    return score


def get_recommendation_text(score):
    """Get recommendation text based on score."""
    if score >= 8:
        return "🔥 PRIORITY"
    elif score >= 6:
        return "⭐ GOOD TARGET"
    elif score >= 4:
        return "✓ CONSIDER"
    else:
        return "• LOW PRIORITY"


def get_detailed_recommendation(set_code, result):
    """Get detailed recommendation text for a set."""
    reasons = {
        'MH3': "Extremely high power level cards, many Commander staples",
        'LTR': "Massively popular in Commander, unique mechanics and themes",
        'CLB': "Designed specifically for Commander format",
        'NCC': "Commander precon cards, many format staples",
        'LCI': "Strong tribal themes (Dinosaurs, Pirates, Merfolk, Vampires)",
        'MOM': "Multiverse cards, high power level, planeswalker density",
        'ONE': "Phyrexian mana and toxic mechanics, very powerful cards",
        'WOE': "Adventure mechanics and enchantment themes",
        'BRO': "Artifact-heavy set, great for artifact commanders",
        'DMU': "Legendary matters, historic themes, domain mechanics"
    }

    base_reason = reasons.get(set_code, "Good power level for Commander")

    if result['completion_rate'] < 20:
        return f"{base_reason}. Low completion means high potential gains."
    elif result['rare_mythic_completion'] < 15:
        return f"{base_reason}. Missing most rare/mythic cards."
    else:
        return f"{base_reason}. Good foundation to build upon."


if __name__ == "__main__":
    # cards = get_cards_from_txt('Example_request.txt')

    file_path = 'Collections/final_collection.csv'
    colection = get_cards_from_csv(file_path)

    # get_known_owners(colection)
    # request_owners(cards, colection)
    # # request_owners(cards, colection, specific_owner='XorVitor')

    # Commander set analysis
    print("Analyzing your collection for Commander format recommendations...")
    analyze_commander_sets(colection)

    # Analyze Commander sets
    analyze_commander_sets(colection)
