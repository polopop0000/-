import asyncio
import sys
from aiogram import Bot, Dispatcher

from app.handlers import router

if sys.platform.startswith("win"): #проверка запуска кода на windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #исправление проблемы асинхронности на windows

async def main(): #функция запуска бота
    bot = Bot(token='TOKEN') #создание объекта бота и импорт токена
    dp = Dispatcher()
    dp.include_router(router) #подключение всех обработчиков из hendlers.py
    await dp.start_polling(bot) #запуск бота


if __name__ == '__main__': #проверка запуска файла
    try:
        asyncio.run(main()) #запуск асинхронной функции main()
    except KeyboardInterrupt: #остановка бота(Ctrl+C)
        print('Бот выключен')
