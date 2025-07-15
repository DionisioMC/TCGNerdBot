import csv
import requests


def check_card_in_db(db_data, card, owner=None):
    """
    Checks if a card exists in the database and optionally filters by owner.

    Args:
        db_data (list of dict): A list of dictionaries representing the database, 
                                where each dictionary contains card information.
        card (dict): A dictionary containing the card details to search for. 
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
    Get comprehensive set statistics from the Scryfall API.

    Args:
        set_code (str): The set code to get statistics for.

    Returns:
        dict: Dictionary containing set information and statistics, or None if not found.
    """
    try:
        api = requests.get(
            f'https://api.scryfall.com/sets/{set_code.lower()}', timeout=10)
        if api.status_code == 200:
            set_data = api.json()

            # Get all cards in the set
            cards_api = requests.get(
                f'https://api.scryfall.com/cards/search?q=set:{set_code.lower()}', timeout=10)
            if cards_api.status_code == 200:
                cards_data = cards_api.json()

                # Count rarities and colors
                rarity_breakdown = {'common': 0,
                                    'uncommon': 0, 'rare': 0, 'mythic': 0}
                color_breakdown = {'white': 0, 'blue': 0, 'black': 0,
                                   'red': 0, 'green': 0, 'colorless': 0, 'multicolor': 0}

                for card in cards_data.get('data', []):
                    # Count rarity
                    rarity = card.get('rarity', 'unknown')
                    if rarity in rarity_breakdown:
                        rarity_breakdown[rarity] += 1

                    # Count colors
                    colors = card.get('colors', [])
                    if not colors:
                        color_breakdown['colorless'] += 1
                    elif len(colors) > 1:
                        color_breakdown['multicolor'] += 1
                    else:
                        color_map = {'W': 'white', 'U': 'blue',
                                     'B': 'black', 'R': 'red', 'G': 'green'}
                        for color in colors:
                            if color in color_map:
                                color_breakdown[color_map[color]] += 1

                return {
                    'set_info': {
                        'code': set_data.get('code', '').upper(),
                        'name': set_data.get('name', ''),
                        'release_date': set_data.get('released_at', ''),
                        'total_cards': set_data.get('card_count', 0)
                    },
                    'rarity_breakdown': rarity_breakdown,
                    'color_breakdown': color_breakdown
                }
    except Exception as e:
        print(f"Error getting set stats: {e}")

    return None


def quick_rarity_comparison_by_owner(collection, set_code, owner):
    """
    Compare an owner's collection to a specific set with rarity breakdown.

    Args:
        collection (list): The collection data
        set_code (str): The set code to compare against
        owner (str): The owner to filter by

    Returns:
        dict: Comparison results with completion percentages
    """
    try:
        # Get set statistics
        set_stats = get_set_stats(set_code)
        if not set_stats:
            return None

        # Get owner's cards from this set
        owner_cards = [card for card in collection
                       if (card.get('Set code', '').lower() == set_code.lower() or
                           card.get('Set name', '').lower() == set_code.lower())
                       and card.get('Owner', '') == owner]

        # Count by rarity
        owner_rarity_breakdown = {'common': 0,
                                  'uncommon': 0, 'rare': 0, 'mythic': 0}
        for card in owner_cards:
            rarity = card.get('Rarity', 'unknown').lower()
            if rarity in owner_rarity_breakdown:
                owner_rarity_breakdown[rarity] += 1

        total_owner_cards = len(owner_cards)
        total_set_cards = set_stats['set_info']['total_cards']
        completion_percentage = (
            total_owner_cards / total_set_cards * 100) if total_set_cards > 0 else 0

        return {
            'set_code': set_code.upper(),
            'set_name': set_stats['set_info']['name'],
            'your_total': total_owner_cards,
            'set_total': total_set_cards,
            'completion_percentage': completion_percentage,
            'your_rarity_breakdown': owner_rarity_breakdown,
            'set_rarity_breakdown': set_stats['rarity_breakdown']
        }
    except Exception as e:
        print(f"Error in quick_rarity_comparison_by_owner: {e}")
        return None


def analyze_commander_sets_by_owner(collection, owner):
    """
    Analyze which sets would be best for Commander format based on owner's collection.

    Args:
        collection (list): The collection data
        owner (str): The owner to analyze

    Returns:
        list: List of set recommendations sorted by score
    """
    try:
        # Get all unique sets in owner's collection
        owner_sets = set()
        for card in collection:
            if card.get('Owner', '') == owner:
                set_code = card.get('Set code', '')
                if set_code:
                    owner_sets.add(set_code)

        recommendations = []

        for set_code in owner_sets:
            comparison = quick_rarity_comparison_by_owner(
                collection, set_code, owner)
            if comparison:
                # Calculate Commander score based on rare/mythic completion
                rare_mythic_owned = comparison['your_rarity_breakdown']['rare'] + \
                    comparison['your_rarity_breakdown']['mythic']
                rare_mythic_total = comparison['set_rarity_breakdown']['rare'] + \
                    comparison['set_rarity_breakdown']['mythic']
                rare_mythic_completion = (
                    rare_mythic_owned / rare_mythic_total * 100) if rare_mythic_total > 0 else 0

                # Simple scoring algorithm (can be improved)
                commander_score = min(
                    10, (rare_mythic_completion / 10) + (comparison['completion_percentage'] / 20))
                recommendation_score = (
                    rare_mythic_completion * 0.6) + (comparison['completion_percentage'] * 0.4)

                recommendations.append({
                    'set_code': comparison['set_code'],
                    'set_name': comparison['set_name'],
                    'completion_rate': comparison['completion_percentage'],
                    'rare_mythic_completion': rare_mythic_completion,
                    'commander_score': round(commander_score, 1),
                    'recommendation_score': round(recommendation_score, 1)
                })

        # Sort by recommendation score
        return sorted(recommendations, key=lambda x: x['recommendation_score'], reverse=True)

    except Exception as e:
        print(f"Error in analyze_commander_sets_by_owner: {e}")
        return []


def get_all_sets_in_collection(collection):
    """
    Get all unique sets present in the collection.

    Args:
        collection (list): The collection data

    Returns:
        list: List of dictionaries with set information
    """
    sets_dict = {}

    for card in collection:
        set_code = card.get('Set code', '')
        set_name = card.get('Set name', '')

        if set_code and set_code not in sets_dict:
            sets_dict[set_code] = {
                'code': set_code,
                'name': set_name,
                'card_count': 0
            }

        if set_code in sets_dict:
            sets_dict[set_code]['card_count'] += int(card.get('Quantity', 1))

    return list(sets_dict.values())


def compare_all_sets_by_owner(collection, owner):
    """
    Compare an owner's collection completion rate across all sets they own cards from.

    Args:
        collection (list): The collection data
        owner (str): The owner to analyze

    Returns:
        list: List of set comparisons sorted by completion percentage
    """
    try:
        # Get all sets in the owner's collection
        owner_sets = set()
        for card in collection:
            if card.get('Owner', '') == owner:
                set_code = card.get('Set code', '')
                if set_code:
                    owner_sets.add(set_code)

        comparisons = []

        for set_code in owner_sets:
            comparison = quick_rarity_comparison_by_owner(
                collection, set_code, owner)
            if comparison:
                comparisons.append(comparison)

        # Sort by completion percentage
        return sorted(comparisons, key=lambda x: x['completion_percentage'], reverse=True)

    except Exception as e:
        print(f"Error in compare_all_sets_by_owner: {e}")
        return []


def compare_top_sets_by_owner(collection, owner, top_count=15):
    """
    Compare an owner's collection completion rate for their top sets only.
    This is much faster than analyzing all sets.

    Args:
        collection (list): The collection data
        owner (str): The owner to analyze
        top_count (int): Number of top sets to analyze (default: 15)

    Returns:
        list: List of set comparisons sorted by completion percentage
    """
    try:
        # First, count cards per set for this owner (fast operation)
        set_card_counts = {}
        for card in collection:
            if card.get('Owner', '') == owner:
                set_code = card.get('Set code', '')
                if set_code:
                    if set_code not in set_card_counts:
                        set_card_counts[set_code] = {
                            'count': 0,
                            'set_name': card.get('Set name', set_code)
                        }
                    set_card_counts[set_code]['count'] += 1

        # Get top sets by card count
        top_sets = sorted(set_card_counts.items(),
                          key=lambda x: x[1]['count'],
                          reverse=True)[:top_count]

        # Only do detailed comparison for top sets
        comparisons = []
        for set_code, _ in top_sets:
            comparison = quick_rarity_comparison_by_owner(
                collection, set_code, owner)
            if comparison:
                comparisons.append(comparison)

        # Sort by completion percentage
        return sorted(comparisons, key=lambda x: x['completion_percentage'], reverse=True)

    except Exception as e:
        print(f"Error in compare_top_sets_by_owner: {e}")
        return []


if __name__ == "__main__":
    cards = get_cards_from_txt('Example_request.txt')

    file_path = 'Colections//final_colection.csv'
    colection = get_cards_from_csv(file_path)

    # get_known_owners(colection)
    # request_owners(cards, colection)
    # # request_owners(cards, colection, specific_owner='XorVitor')

    get_set_stats('FIN')
