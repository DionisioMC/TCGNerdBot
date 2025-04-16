import csv


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
        if card['Name'].lower() in card_db['Name'].lower() :
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
            print(f"{card['Name']} found in the database. Owners: {', '.join(unique_owners)}")
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
    

if __name__ == "__main__":
    cards = get_cards_from_txt('Example_request.txt')

    file_path = 'Colections//final_colection.csv'
    colection = get_cards_from_csv(file_path)
    
    get_known_owners(colection)
    request_owners(cards, colection)
    # request_owners(cards, colection, specific_owner='XorVitor')
