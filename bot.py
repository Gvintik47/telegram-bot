from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import random
import os

TOKEN = "7087944729:AAGt9hKn8uj53oPXJeUqe38dSPlcskiId-c"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

films = ["Вверх", "ВАЛЛ-И", "В лес, где мерцают светлячки"]

def get_film():
    return random.choice(films)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Открыть", callback_data="open_letter")
    keyboard.add(button)
    await bot.send_photo(message.chat.id, photo=open("envelope.jpg", "rb"), caption="Нажми, чтобы открыть письмо", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "open_letter")
async def open_letter(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Получить валентинку", callback_data="get_valentine")
    keyboard.add(button)
    await bot.send_photo(callback_query.message.chat.id, photo=open("letter.jpg", "rb"), caption="Вы успешно прочли письмо", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "get_valentine")
async def get_valentine(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Согласиться", callback_data="accept_date")
    button2 = types.InlineKeyboardButton("Отказать", callback_data="decline_date")
    keyboard.add(button1, button2)
    await bot.send_photo(callback_query.message.chat.id, photo=open("valentine.jpg", "rb"), caption="Вам пришло приглашение на интернет-свидание", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "accept_date")
async def accept_date(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Выбрать что смотреть", callback_data="choose_movie")
    keyboard.add(button)
    await bot.send_message(callback_query.message.chat.id, "Время свидания: 8 вечера по Киеву или 11 по Алматы", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "choose_movie")
async def choose_movie(callback_query: types.CallbackQuery):
    movie = get_film()
    await bot.send_message(callback_query.message.chat.id, f"Ваш выбор: {movie}\nЖду скрин и тебя, люблю 💕")

@dp.callback_query_handler(lambda c: c.data == "decline_date")
async def decline_date(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Перезапустить", callback_data="restart")
    keyboard.add(button)
    await bot.send_message(callback_query.message.chat.id, "😔", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "restart")
async def restart(callback_query: types.CallbackQuery):
    await start(callback_query.message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
