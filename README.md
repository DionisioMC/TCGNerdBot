# TCGNerdBot

Do you like TCGs? Do you have a Discord server with your friends where you talk about these kinds of things? Then I have the perfect Bot to add to your server! **TCGNerdBot** - your comprehensive Magic: The Gathering collection assistant!

This bot helps you and your friends manage your card collections, find card information, analyze set completion, and make informed decisions about your Magic: The Gathering purchases. Whether you're looking for specific cards, checking prices, or planning your next booster box purchase, TCGNerdBot has you covered!

## Getting Started

After going through the process of adding the bot to your server (keep in mind that you will definitely need permission to see the content of messages and to send messages), you'll find all the bot logic in `bot.py`!

In the file you will notice there are 2 environment variables that come from a `.env` file: the Discord bot token and optionally the server ID. You will need to add these in the form of strings in a `.env` file for the code to work. The only indispensable variable you need to add is `DISCORD_TOKEN`. You can always eliminate the section that needs the `DISCORD_SERVER` variable.

After setting up the environment variables and installing all the necessary dependencies, you can test the code in the terminal by navigating to the directory where the files are located and typing `python3 bot.py`

## Current Features

### 🔍 Card Lookup

- **Card Images**: Get an image of any Magic: The Gathering card by writing its name inside `[card name]`
- **Price Checking**: Get the current EUR price of a card by adding "price" to your message. Example: `[Sol Ring] price`
- **Commander Legality**: Check if a card is legal in Commander format by adding "legal" to your message. Example: `[Mana Crypt] legal`

### 📚 Wiki Integration

- **MTG Wiki Search**: Search the MTG Wiki by writing a keyword inside `{keyword}`

### 📊 Collection Management & Analysis

- **File Upload Analysis**: Upload a .txt file with your want list (format: `1x Card Name` per line) to see who in your group owns those cards
- **Set Statistics**: Use `!setstats <SET_CODE>` to get comprehensive statistics about any Magic set, including rarity breakdown and color distribution
- **Personal Collection Comparison**: Use `!compare <SET_CODE>` to see how your collection compares to a specific set
- **Complete Collection Overview**: Use `!compareall` to get a comprehensive overview of your collection across all sets you own cards from
- **Commander Format Recommendations**: Use `!commander` to get personalized recommendations for Commander format based on your collection

### 🤖 Bot Interaction

- **Help System**: Use `!help` or `!commands` to see all available commands with examples
- **Mention Response**: Mention the bot to check your collection against a predefined want list

### 🔧 Technical Features

- All card data powered by the **Scryfall API**
- Collection data management through CSV files
- Discord embed formatting for rich, organized responses
- Error handling with user-friendly messages
- Support for both set codes and set names

## Setup Instructions

1. Add the bot to your Discord server (requires message reading and sending permissions)
2. Create a `.env` file in the bot directory with your Discord bot token:

   ```env
   DISCORD_TOKEN=your_bot_token_here
   DISCORD_SERVER=your_server_id_here
   ```

   Note: `DISCORD_TOKEN` is required, `DISCORD_SERVER` is optional

3. Install required dependencies (discord.py, requests, python-dotenv, beautifulsoup4)
4. Place your collection CSV file in the `Collections/` directory as `final_collection.csv`
5. Run the bot: `python3 bot.py`

## Collection File Format

Your collection CSV should include these columns:

- `Name`: Card name
- `Set code`: Magic set code (e.g., "MH3")
- `Set name`: Full set name
- `Rarity`: Card rarity (common, uncommon, rare, mythic)
- `Owner`: Owner's name
- `Quantity`: Number of copies owned

## Future Features

- Enhanced format legality checking for all formats
- Advanced collection analytics and insights
- Trade suggestion system
- Price trend tracking
- Deck building assistance
