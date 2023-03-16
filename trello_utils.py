import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")


async def upload_file_to_trello_card(key, token, card_id, file_path):
    params = {"key": key, "token": token}
    url = f"https://api.trello.com/1/cards/{card_id}/attachments"

    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        with open(file_path, "rb") as file:
            file_name = os.path.basename(file_path)
            data.add_field("file", file, filename=file_name)
            async with session.post(url, params=params, data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to upload file: {response.status}")


async def create_trello_card(
    board_name, card_name, card_description, card_attachments=None
):
    board = board_name
    trello_list = board.list_lists()[3]
    card = trello_list.add_card(card_name, card_description)
    if card_attachments:
        for attachment_path in card_attachments:
            await upload_file_to_trello_card(
                TRELLO_API_KEY, TRELLO_API_TOKEN, card.id, attachment_path
            )
            os.remove(attachment_path)
    return True
