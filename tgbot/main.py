import asyncio
import logging
from os import getenv

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import BotCommand

TG_TOKEN = getenv('TG_TOKEN')

masters = ["Ромыч", "Никитос"]
dates = ['15.04', '16.04', '17.04', '18.04']
times = ['10:00', '12:00', '15:30', '17:30']
services = ['голову', 'голову с бородой']


class OrderTrim(StatesGroup):
    """
    Список состояний для записи на стрижку
    """
    waiting_for_master = State()
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_service = State()


async def set_order_master(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for master in masters:
        keyboard.add(master)
    await message.answer("К кому пойдешь?", reply_markup=keyboard)
    await OrderTrim.waiting_for_master.set()


async def set_order_date(message: types.Message, state: FSMContext):
    if message.text not in masters:
        await message.answer("Не понял, повтори. К кому идешь?")
        return
    await state.update_data(master=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for order_date in dates:
        keyboard.add(order_date)
    await OrderTrim.next()
    await message.answer("Теперь давай решим, когда пойдешь?", reply_markup=keyboard)


async def set_order_time(message: types.Message, state: FSMContext):
    if message.text not in dates:
        await message.answer("Не понял, повтори. Когда идешь?")
        return
    await state.update_data(date=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for order_time in times:
        keyboard.add(order_time)
    await OrderTrim.next()
    await message.answer("оК. На какое время записать?", reply_markup=keyboard)


async def set_order_service(message: types.Message, state: FSMContext):
    if message.text not in times:
        await message.answer("Не понял, повтори. На сколько записать?")
        return
    await state.update_data(time=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for order_service in services:
        keyboard.add(order_service)
    await OrderTrim.next()
    await message.answer("Отлично. Что будем делать?", reply_markup=keyboard)


async def finish_order(message: types.Message, state: FSMContext):
    if message.text not in services:
        await message.answer("Не понял. Что ты хочешь себе подрезать?")
        return
    await state.update_data(service=message.text)
    user_data = await state.get_data()
    await message.answer(f"{user_data['master']} ждет тебя в {user_data['time']} {user_data['date']}\n"
                         f"Будем делать тебе красиво {user_data['service']}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Записаться на стрижку: (/trim).",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_trim(dp: Dispatcher):
    dp.register_message_handler(set_order_master, commands="trim", state="*")
    dp.register_message_handler(set_order_date, state=OrderTrim.waiting_for_master)
    dp.register_message_handler(set_order_time, state=OrderTrim.waiting_for_date)
    dp.register_message_handler(set_order_service, state=OrderTrim.waiting_for_time)
    dp.register_message_handler(finish_order, state=OrderTrim.waiting_for_service)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")


logger = logging.getLogger(__name__)

# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/trim", description="Хочу на стрижку"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")


    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_trim(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())