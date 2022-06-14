from bd_google import service, spreadsheetId, send_student, frame, send_avto


id_std = 2134513
name = 'Хисматуллин Ильшат'
group = 12

for i in range(10):
    send_student(id_std, name, group+i)

send_avto('Н448ОМ')

from bd_google import num_st

frame(0, num_st+2, 1, 4)
print('Запуск бота')
from aiogram import executor

from loader import dp
import middlewares, handlers
from utils.notify_admins import on_startup_notify

async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)