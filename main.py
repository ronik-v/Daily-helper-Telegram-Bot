from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from config import bot_token

from MessageText import START_COMMAND, HELP_COMMAND
from Finance import GetInfoAboutRate
from DailyNews import DailyNews
from Weather import GetWeather

from transliterate import translit
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Помощь', 'Новости', 'Курсы валют', 'Погода']
keyboard.add(*buttons)


class WeatherForm(StatesGroup):
    city = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(
        reply_markup=keyboard,
        chat_id=message.from_user.id,
        text=START_COMMAND,
        parse_mode='HTML'
    )


@dp.message_handler(lambda message: message.text == 'Помощь')
async def process_help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=HELP_COMMAND,
        parse_mode='HTML'
    )


@dp.message_handler(lambda message: message.text == 'Новости')
async def news_command(message: types.Message):
    NEWS = DailyNews().__call__()
    for key, value in zip(NEWS.keys(), NEWS.values()):
        await bot.send_message(message.from_id, f"{key} --- {value}")


@dp.message_handler(lambda message: message.text == 'Курсы валют')
async def rate_command(message: types.Message):
    for obj in GetInfoAboutRate().__call__():
        await bot.send_message(message.from_id, obj)


@dp.message_handler(lambda message: message.text == 'Погода')
async def weather_handler(message: types.Message):
    await WeatherForm.city.set()
    await message.answer('Введите название города')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(state=WeatherForm.city)
async def weather_command(message: types.Message, state: FSMContext):
    en_city = translit(message.text, reversed=True)
    for obj in GetWeather(en_city).__call__():
        await bot.send_message(message.from_id, obj)
    await state.finish()


if __name__ == '__main__':
    try:
        executor.start_polling(dp)
    except OSError:
        exit(1)
