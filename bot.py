import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from trello import TrelloClient
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
from trello_utils import create_trello_card
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_SECRET = os.getenv("TRELLO_API_SECRET")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
SAVE_DIR = os.getenv("SAVE_DIR")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
attachments = []

# Создаем экземпляр клиента Trello
client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_API_TOKEN
)

# Создаем список досок Trello
boards = client.list_boards()[4], client.list_boards()[5]
boards_name = boards[0].name, boards[1].name
basedir = os.path.abspath(os.path.dirname(__file__))


# Определяем состояния FSM
class NewCard(StatesGroup):
    waiting_to_start = State()
    waiting_for_board = State()
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_attachment = State()


# Создаем директорию attachments, если ее еще нет
if not os.path.exists("attachments"):
    os.makedirs("attachments")

# Создаем бота и диспетчер
bot = Bot(token=str(TOKEN))
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware(logger))


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    reply_markup = types.ReplyKeyboardRemove()
    await message.answer(
        "To create a new card, enter the /new_bug command.",
        reply_markup=reply_markup
    )
    await NewCard.waiting_to_start.set()


# Обработчик команды /new_bug
@dp.message_handler(commands=["new_bug"], state=NewCard.waiting_to_start)
async def process_start(message: types.Message, state: FSMContext):
    global attachments
    attachments = []
    board_names = [str(boards[0].name), str(boards[1].name)]
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in board_names:
        reply_markup.add(name)
    await message.answer(
        "Select the board to create a new card on:",
        reply_markup=reply_markup
    )
    await NewCard.waiting_for_board.set()


# Обработчик выбора доски
@dp.message_handler(
    Text(equals=[boards[0].name,
                 boards[1].name]),
    state=NewCard.waiting_for_board
)
async def process_board(message: types.Message, state: FSMContext):
    reply_markup = types.ReplyKeyboardRemove()

    board_name = message.text
    board = next(filter(lambda b: b.name == board_name, boards), None)
    if not board:
        await message.answer(
            "The selected board was not found!",
            reply_markup=reply_markup
        )
        return

    async with state.proxy() as data:
        data["board"] = board.name

    await message.answer(
        "Enter the card's title:",
        reply_markup=reply_markup
    )
    await NewCard.waiting_for_name.set()


# Обработчик ввода названия карточки
@dp.message_handler(state=NewCard.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await message.answer(
        """
        Enter the card description:

        Example:
        Версия приложения: 4.2.22
        Сервер: ReсX Верификация
        Устройство: 980 С Двумя камерами
        Шаги воспроизведения:
            Загрузить приложение
            Водим мимо считки браслетом
        Ожидание:
            Обработка запроса и последующее взаимодействие с демоном и с биометрией
        Реальность:
            Через некоторое количество повторений данной процедуры приложение падет
            и больше не поднимается, подробности на видео в аттаче"""
    )
    await NewCard.waiting_for_description.set()


# Обработчик ввода описания карточки
@dp.message_handler(state=NewCard.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text

    done_button = types.KeyboardButton("/done")
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(done_button)
    await message.answer(
        "Attach files to the card (if any), or enter /done to create the card:",
        reply_markup=reply_markup,
    )
    await NewCard.waiting_for_attachment.set()


# Обработчик прикрепленных файлов
@dp.message_handler(
    content_types=types.ContentTypes.ANY, state=NewCard.waiting_for_attachment
)
async def process_attachment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.content_type == "text":
            if message.text == "/done":
                await process_done(message, state)
            else:
                await message.answer(
                    "Please attach files or enter /done to create the card:"
                )
        else:
            attachments.append(await attachments_get(message.document))
            await message.answer("Файл успешно добавлен!")
            await message.answer(
                "If you want to add more files, attach them to the message, or enter /done to create the card:"
            )
            await NewCard.waiting_for_attachment.set()


async def attachments_get(document):
    file = await bot.get_file(document.file_id)
    filename = document.file_name
    file_path = os.path.join(str(SAVE_DIR), filename)
    await file.download(file_path)
    return file_path


# Обработчик комманды done
@dp.message_handler(commands=["done"], state=NewCard.waiting_for_attachment)
async def process_done(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        close_keyboard = types.ReplyKeyboardRemove()
        board = data["board"]
        board = next(filter(lambda b: b.name == board, boards), None)
        card_name = data["name"]
        card_description = data["description"]
        if card_attachments := attachments:
            await create_trello_card(
                board, card_name, card_description, card_attachments
            )
        else:
            await create_trello_card(board, card_name, card_description)
        await message.answer(
            "Card successfully created!",
            reply_markup=close_keyboard
        )
    await state.finish()
    await NewCard.waiting_to_start.set()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
