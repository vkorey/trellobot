## Trello Bot

This bot helps you create new Trello cards directly from Telegram. It supports attaching files and adding them to the card as well. The bot prompts the user to select a board, enter the card's title and description, and attach files if necessary.


### Configuration

To set up the bot, you need to provide the following environment variables in a .env file:

```
TOKEN: Your Telegram bot token.
TRELLO_API_KEY: Your Trello API key.
TRELLO_API_SECRET: Your Trello API secret.
TRELLO_API_TOKEN: Your Trello API token.
SAVE_DIR: The directory where the attached files will be saved.
BOARDS_COLUMNS: A comma-separated list of board and column indices. For example: 0.0,1.0.
ALLOWED_USERS: A comma-separated list of Telegram user IDs that are allowed to use the bot. 
```


### Boards and columns

To customize the bot for your needs, you can set the `BOARDS_COLUMNS` environment variable in the `.env` file:

1.  Select the Trello boards and columns you want to use with your bot by specifying them in the `BOARDS_COLUMNS` environment variable. The format should be `board_index.column_index`, separated by commas if you want to use multiple boards:
```
BOARDS_COLUMNS=4.3, 5.3
```

This will select the 5th and 6th boards (remember, the index is zero-based) and the 4th column in each board.

To list all your boards and their indices, you can run the following script:
```python
all_boards = client.list_boards()
for idx, board in enumerate(all_boards):
    print(f"{idx}: {board.name}")
```

2. To list all the columns in a board and their indices, you can run the following script:
```python
all_lists = board.list_lists()
for idx, trello_list in enumerate(all_lists):
    print(f"{idx}: {trello_list.name}")
```

Make sure to update the `BOARDS_COLUMNS` variable in the `.env` file according to the indices of the boards and columns you want to use.


### Access Restrictions

By default, the bot only allows users with specific Telegram IDs to use its functionality. To grant access to a user, add their Telegram ID to the ALLOWED_USERS environment variable in the .env file.

For example:

```
ALLOWED_USERS=123456789,987654321
```

This will grant access to users with Telegram IDs 987654321 and 123456789.

If you want to allow all users to access the bot without restrictions, you can remove the ALLOWED_USERS variable from the .env file or set it to an empty value.


### Installation

1.  Make sure you have Python 3.7 or higher installed.
    
2.  Clone the repository:
   ```bash
git clone https://github.com/vkorey/trellobot
cd trellobot
```
3. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:
```
pip install -r requirements.txt
```

5. Create a `.env` file in the project's root folder and add the following variables:
```
TOKEN=<your bot token>
TRELLO_API_KEY=<your Trello API key>
TRELLO_API_SECRET=<your Trello API secret>
TRELLO_API_TOKEN=<your Trello API token>
SAVE_DIR=attachments
BOARDS_COLUMNS: <A comma-separated list of board and column indices. For example: 0.0,1.0.>
ALLOWED_USERS: <A comma-separated list of Telegram user IDs that are allowed to use the bot.>
```


### Running

To run the bot, execute the following command:
```
python bot.py
```


### Usage

1.  Find your bot on Telegram and start a chat with it.
2.  Enter the `/start` command and follow the bot's instructions to create a new Trello card.
3.  The bot will ask you to select a board, enter the card's title and description, and attach files if necessary.
4.  Enter the `/done` command when you have finished entering the card's information. The bot will create the card on the specified board and send you a confirmation.