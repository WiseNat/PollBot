# PollBot
A simple poll bot for Discord

## Setup
If you actually want to setup this bot you'll need to do all of the following steps and install the correct dependencies.

Dependency  | Website URL
------------|------------
Python 3.6+ | https://www.python.org/
discord.py  | https://discordpy.readthedocs.io/en/latest/intro.html#prerequisites
Google Client Library | https://developers.google.com/sheets/api/quickstart/python#step_2_install_the_google_client_library


### Discord Developer Portal
1. Go to [this website](https://discord.com/developers/applications) and sign in with your Discord account
2. Click "New Application"
    1. Give it a name
    2. Click "Create"
3. Click on the application you just made
4. Go to the Bot tab on the left
5. Click "Add Bot" and agree to make the bot
6. Scroll down to "Privileged Gateway Intents" and turn on the "Server Members Intent"
7. Scroll back up and under where you input the bots username click the "Copy" button to copy the bots Token


### Github Repository
1. Clone this repository or download it
2. Add a file to the repository called "token.secret"
3. Open the "token.secret" file in a text editor and paste in your bots Token
4. Save changes to "token.secret"


### Getting Autopolling to work (Optional)
1. Go to [this website](https://developers.google.com/sheets/api/quickstart/python#step_1_turn_on_the) and click "Enable the Google Sheets API"
2. Choose a name for your project and hit next
3. Choose Desktop App and hit create
4. Click "Download Client Configuration" and save it to your repository


**If you want to disable Autopolling then you'll have to remove the appropriate code under the commands.py file**


### Inviting the Bot
1. Copy this link and paste it somewhere temporary - notepad for example
    1. https://discordapp.com/oauth2/authorize?client_id=INSERT_CLIENT_ID_HERE&scope=bot&permissions=355392
2. Go back to the [Discord Developer Portal](https://discord.com/developers/applications) and sign in if you have to
3. Go to the application you created earlier
4. Click on "Copy" under Client ID
5. Replace the "INSERT_CLIENT_ID_HERE" in the link with the Client ID you just copied
6. Copy the link and go to it in your web browser
7. Follow through with inviting the bot to whatever server you wish


### Running the Bot
1. Navigate back to your PollBot repository
2. Run the "bot.py" Python file

After ~5 seconds the bot should come online. Enjoy! If you find any bugs then feel free to let me know on here under "Issues". I'd love to fix them.

As a quick sidenote, whenever you run the autopoll command for a new spreadsheet, it'll prompt you to Authorise for that spreadsheet to have it's data read.
