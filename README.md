# TCGNerdBot

Do you like TCGs? Do you have a Discord server with your friends where you talk about these kinds of things? Then i have the perfect Bot to add to your server! TCGNerd!

After going through the process of adding the bot to your server (keep in mind that you will definitely need permition to see the content of messages and to send messages),  You will need instructions for your Bot to be useful once in a while right? Well, that code is located in bot.py! 

In the file you will certainly notice there are 2 variables there that seem to come from nowhere, right? Well my friend, that represents the token from the discord bot and the other the name of the server you added the bot to. You will need to add those in the form of a string in a .env file in order for the code to work. To be fair, the only indipensable variableyou need to add is DISCORD_TOKEN. You can always eliminate the section that will need the DISCORD_SERVER variable. 

After all this and installing all the necessary dependencies, you can test the code in the terminal by moving to the directory where the files are located and type ```python3 bot.p```

Current features:

    Getting an image of a card by writting its name inside [], curently working for magic: the gathering

Future features:

    Getting the definition of a keyword by writing the name inside []

    Cunsulting the price or legality of a card by writing the name of the card and then price or a format name to consult it
