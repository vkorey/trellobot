import os
from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")


async def create_trello_card(
    board_name, column_index, card_name, card_description, boards, card_attachments=None
):
    board = next(filter(lambda b: b.name == board_name, boards), None)
    trello_list = board.list_lists()[column_index]
    card = trello_list.add_card(card_name, card_description)
    if card_attachments:
        for attachment_path in card_attachments:
            with open(attachment_path, "rb") as file:  # Open the file in binary mode
                card.attach(name=os.path.basename(attachment_path), file=file)
            os.remove(attachment_path)
    return True
