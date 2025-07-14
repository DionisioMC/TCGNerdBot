# TCGNerdBot 🃏

**Your Ultimate Magic: The Gathering Discord Collection Assistant!**


Do you like TCGs? Do you have a Discord server with your friends where you talk about these kinds of things? Then i have the perfect Bot to add to your server! TCGNerd!

After going through the process of adding the bot to your server (keep in mind that you will definitely need permition to see the content of messages and to send messages),  You will need instructions for your Bot to be useful once in a while right? Well, that code is located in bot.py! 

In the file you will certainly notice there are 2 variables there that seem to come from nowhere, right? Well my friend, that represents the token from the discord bot and the other the name of the server you added the bot to. You will need to add those in the form of a string in a .env file in order for the code to work. To be fair, the only indipensable variableyou need to add is DISCORD_TOKEN. You can always eliminate the section that will need the DISCORD_SERVER variable. 

After all this and installing all the necessary dependencies, you can test the code in the terminal by moving to the directory where the files are located and type ```python3 bot.py```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Required dependencies (install with `pip install -r requirements.txt`)

### Configuration
1. **Create a `.env` file** in the project directory with:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_SERVER=your_server_name_here
   ```

2. **Bot Permissions Required:**
   - Read Messages/View Channels
   - Send Messages
   - Read Message History
   - Attach Files
   - Use External Emojis

3. **Collection Database:**
   - Place your collection CSV export in `Collections/final_collection.csv`
   - Ensure the CSV has an "Owner" column to track card ownership

### Running the Bot
```bash
cd TCGNerdBot/TCGNerdBot
python bot.py
```

---

## 🎮 Features & Commands

### 🔍 **Card Lookup & Information**
- **`[Card Name]`** - Display card image
- **`[Card Name] price`** - Show current EUR price
- **`[Card Name] legal`** - Check Commander legality
- **`{keyword}`** - Search MTG Wiki for rules and definitions

*Powered by Scryfall API*

### 📊 **Collection Analysis (Personal)**
- **`!setstats <SET_CODE>`** - Get comprehensive set statistics
  - Rarity breakdown, color distribution, card types
  - Example: `!setstats MH3`

- **`!compare <SET_CODE>`** - Compare YOUR collection to a set
  - Personal completion percentages by rarity
  - Example: `!compare OTJ`

- **`!commander`** - Get personalized Commander format recommendations
  - Analyzes 70+ sets for optimal collection building
  - Priority scoring based on completion and format relevance

### 📁 **File Upload - Community Card Finding**
- **Upload `.txt` files** with your want lists to find who owns specific cards
- **Format:** `1x Card Name` per line
- **Returns:** Which users own each requested card across all collections
- **Perfect for:** Trading, borrowing cards, deck building

### 🛠️ **Privacy & Security**
- ✅ **Personal Commands:** Users can only view their own collection data
- ✅ **Community Features:** File uploads search all collections to facilitate trading
- ✅ **Owner-Based Filtering:** Multi-user collection support

---

## 📖 **Command Examples**

```
Card Lookup:
[Lightning Bolt]              → Shows card image
[Mana Crypt] price           → Shows price in EUR
[Command Tower] legal        → Checks Commander legality
{flying}                     → Searches MTG Wiki

Collection Analysis:
!setstats MH3               → Modern Horizons 3 statistics
!compare OTJ                → Your Outlaws of Thunder Junction progress
!commander                  → Your personalized Commander recommendations

File Upload:
📎 Upload my_wants.txt      → Find who owns cards in your want list
```

---

## 🎯 **Commander Analysis Features**

### **Comprehensive Set Coverage (70+ Sets)**
- **Recent High-Power Sets:** MH3, BLB, OTJ, MKM, LCI, WOE, LTR, MOM, ONE
- **Commander Products:** CLB, NCC, AFC, C21, CMR, C20, C19
- **Artifact Sets:** BRO, NEO, DMU, DOM, KLD, AER
- **Multicolor Sets:** SNC, GRN, RNA, WAR, RTR, GTC, DGM
- **Tribal Sets:** IXL, RIX, ISD, DKA, SOI, EMN, MID, VOW
- **And many more!**

### **Smart Recommendation System**
- **Completion Analysis:** Identifies sets with low completion for maximum gain
- **Rarity Focus:** Prioritizes rare/mythic gaps for valuable acquisitions
- **Format Relevance:** Scores sets based on Commander popularity and power level
- **Personalized Results:** Tailored to your specific collection

---

## 🏗️ **Technical Architecture**

### **Core Components**
- **`bot.py`** - Discord bot interface and command handling
- **`request_db.py`** - Collection analysis engine and API integration
- **MTG JSON API** - Set statistics and comprehensive card data
- **Scryfall API** - Individual card lookup, pricing, and color identity

### **Key Functions**
- **Set Statistics:** Real-time API data for any MTG set
- **Collection Filtering:** Owner-based multi-user support
- **Commander Scoring:** Algorithmic set relevance calculation
- **File Processing:** Automatic want list parsing and matching

---

## 🔧 **File Structure**
```
TCGNerdBot/
├── bot.py                   # Main Discord bot
├── request_db.py           # Collection analysis engine
├── Collections/
│   └── final_collection.csv  # Your collection database
├── Example_request.txt     # Sample want list format
├── .env                    # Environment variables
└── README.md              # This file
```

---

## 🎮 **Usage Scenarios**

### **Personal Collection Management**
- Track your collection completion across multiple sets
- Get recommendations for which sets to focus on next
- Analyze your collection's rarity and color distribution

### **Community Trading**
- Upload want lists to find who has the cards you need
- Help others find cards from your collection
- Facilitate borrowing for tournaments and events

### **Commander Deck Building**
- Get personalized set recommendations for Commander
- Find the most efficient sets to improve your collection
- Discover hidden gems in older sets

---

## 🚀 **Future Enhancements**

- **Format Legality:** Extended format checking beyond Commander
- **Price Tracking:** Historical price data and trend analysis
- **Deck Suggestions:** AI-powered deck recommendations
- **Trade Management:** Automated trade proposal system
- **Collection Statistics:** Advanced analytics and visualization

---

## 🤝 **Contributing**

Feel free to submit issues, feature requests, or pull requests to help improve TCGNerdBot!

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Ready to level up your Magic: The Gathering Discord experience? Add TCGNerdBot today!** 🎉
