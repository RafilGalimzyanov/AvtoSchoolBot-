from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import callback_data
from aiogram.utils.markdown import hlink

from data.config import ADMINS, BLACK_LIST
from loader import dp, bot
from states.trip import Trip
from bd_google import service, spreadsheetId, send_student, frame, send_avto, num_avto, verify_id, verify_name


@dp.callback_query_handler(text="study", state=Trip.student_1)
async def go_ord(query: types.CallbackQuery, state: FSMContext):
    driver_id = query.message.chat.id
    driver_name = query.from_user.full_name
    if verify_name(query.from_user.username) == True:
        await bot.delete_message(driver_id, query.message.message_id)
        send_student(f'{driver_id}', f'{driver_name}', '06-721')
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Моё расписание", callback_data="timetable", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Откатанные часы", callback_data="rode", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Помощь", callback_data="help", messages="one"))
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="start", messages="one"))
        await bot.send_message(chat_id=driver_id,text="Личный кабинет \n ", reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="start", messages="one"))
        await bot.send_message(chat_id=driver_id, text="Ваших данных нет в базе. Отправьте администратору "
                                                       "Ваш никнейм с просьбой включить в БД  \n "
                               , reply_markup=keyboard)
        await state.finish()

@dp.callback_query_handler(text="timetable", state=Trip.student_1)
async def go_ord(query: types.CallbackQuery):
    driver_id = query.message.chat.id
    await bot.delete_message(driver_id, query.message.message_id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="study", messages="one"))
    timetabel = verify_id(driver_id)
    await bot.send_message(chat_id=driver_id,text=f"{[timetabel[i] for i in range(len(timetabel))]}"
                                                 "\n За 2 часа до занятий будет отправлено уведомление.", reply_markup=keyboard)
    '''await bot.send_message(chat_id=driver_id,text=f"Авто: Н448ОМ \n"
                                                  f"\n"
                                                  f"Понедельник: 9:00 - 10:00 \n"
                                                  f"Вторник: 12:00 - 13:00 \n"
                                                  f"Среда: 10:00 - 11:00 \n"
                                                  f"Четверг: 13:00 - 14:00 \n"
                                                 "\n За 2 часа до занятий будет отправлено уведомление.", reply_markup=keyboard)'''

@dp.callback_query_handler(text="rode", state=Trip.student_1)
async def go_ord(query: types.CallbackQuery):
    driver_id = query.message.chat.id
    await bot.delete_message(driver_id, query.message.message_id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="study", messages="one"))
    await bot.send_message(chat_id=driver_id,text="Откатано: 8 ч. из 40 ч.", reply_markup=keyboard)


@dp.callback_query_handler(text="help", state=Trip.student_1)
async def go_ord(query: types.CallbackQuery):
    driver_id = query.message.chat.id
    await bot.delete_message(driver_id, query.message.message_id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="study", messages="one"))
    await bot.send_message(chat_id=driver_id,text="Данный бот предназначен для удобной связи с автошколой \n"
                                                  "Если возникли вопросы, обращайтесь: 89083395505", reply_markup=keyboard)
