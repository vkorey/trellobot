## Trello Bot for Creating Cards

This program is a simple Telegram bot that allows users to create Trello cards directly from the chat. The bot prompts the user to select a board, enter the card's title and description, and attach files if necessary.

### Customization

To customize the bot for your needs, you can modify the following lines in the `bot.py` file:

1.  Select the Trello boards you want to use with your bot by changing the indices in the following lines:
```python
boards = client.list_boards()[4], client.list_boards()[5]
boards_name = boards[0].name, boards[1].name
```

Replace the numbers inside the square brackets with the indices of the boards you want to use. To list all your boards and their indices, you can run the following script:
```python
all_boards = client.list_boards()
for idx, board in enumerate(all_boards):
    print(f"{idx}: {board.name}")
```

2. Choose the column in which to add the card in the `create_trello_card` function:
```python
trello_list = board.list_lists()[3]
```

Replace the number inside the square brackets with the index of the column you want to use. To list all the columns in a board and their indices, you can run the following script:
```python
all_lists = board.list_lists()
for idx, trello_list in enumerate(all_lists):
    print(f"{idx}: {trello_list.name}")
```


### Installation

1.  Make sure you have Python 3.7 or higher installed.
    
2.  Clone the repository:
   ```bash
git clone https://github.com/vkorey/trellobot
cd trello-bot
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the project's root folder and add the following variables:
```
TOKEN=<your bot token>
TRELLO_API_KEY=<your Trello API key>
TRELLO_API_SECRET=<your Trello API secret>
TRELLO_API_TOKEN=<your Trello API token>
SAVE_DIR=attachments
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