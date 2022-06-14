from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from data.config import ADMINS, BLACK_LIST
from states.trip import Trip

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if f'{message.from_user.id}' in ADMINS and f'{message.from_user.id}' not in BLACK_LIST:
        driver_id = message.from_user.id
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Учусь в вашей АвтоШколе", callback_data="study", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Связаться с АвтоШколой", callback_data="connect", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь", callback_data="help", messages="one"))
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"На связи автошкола драйв,\n"
                             f"Кликните ниже:", reply_markup=keyboard)
        await Trip.student_1.set()

    elif f'{message.from_user.id}' not in ADMINS:
        driver_id = message.from_user.id
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Добавить ник нового ученика", callback_data="nik_add", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Удалить ник ученика", callback_data="nik_del", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь", callback_data="help", messages="one"))
        await message.answer(f"Привет, {message.from_user.full_name}!\n"
                             f"На связи автошкола драйв,\n"
                             f"Кликните ниже:", reply_markup=keyboard)
        await Trip.admin_1.set()

