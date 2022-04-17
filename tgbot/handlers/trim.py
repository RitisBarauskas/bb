import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.helpers.api import get_masters, get_masters_dates, get_masters_hours, get_masters_services
from tgbot.helpers.states import OrderTrim
from tgbot.keyboards.inline.callback_datas import master_callback, date_callback, hour_callback
from tgbot.keyboards.inline.choice_buttons import get_masters_keyboard, get_dates_keyboard, get_hours_keyboard, \
    get_services_keyboard
from tgbot.loader import dp, bot


@dp.message_handler(Command("trim"), state='*')
async def order_trim(message: Message):
    """
    Инициализация записи и выбор мастера
    """

    chat_id = getattr(message.chat, 'id')

    user = get_or_create_user(chat_id)

    masters = await get_masters()
    keyboard = get_masters_keyboard(masters)

    await message.answer(text="К кому пойдешь?", reply_markup=keyboard)
    await OrderTrim.waiting_for_master.set()


@dp.callback_query_handler(master_callback.filter(), state=OrderTrim.waiting_for_master)
async def order_date(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Установим дату записи
    """
    await call.message.edit_reply_markup(reply_markup=None)
    master_id = callback_data.get('id')
    master_name = callback_data.get('name')
    await state.update_data(master_id=master_id)
    await state.update_data(master_name=master_name)
    await call.message.answer(f'{master_name} - отличный выбор.')
    logging.info(f"{callback_data}")

    master_dates = await get_masters_dates(master_id)
    keyboard = get_dates_keyboard(master_dates)

    await call.message.answer(text="На какую дату записать?", reply_markup=keyboard)
    await OrderTrim.waiting_for_date.set()


@dp.callback_query_handler(date_callback.filter(), state=OrderTrim.waiting_for_date)
async def order_time(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await call.message.edit_reply_markup(reply_markup=None)
    entry_date = callback_data.get('entry_date')
    date_str = callback_data.get('date_str')
    order = await state.get_data()
    master_id = order['master_id']
    await call.message.answer(f'{date_str}. Запомнил.')
    logging.info(f"{callback_data}")

    master_hours = await get_masters_hours(master_id, entry_date)
    keyboard = get_hours_keyboard(master_hours)

    await call.message.answer(text="Во сколько ждать тебя?", reply_markup=keyboard)
    await OrderTrim.waiting_for_time.set()


@dp.callback_query_handler(hour_callback.filter(), state=OrderTrim.waiting_for_time)
async def order_service(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await call.message.edit_reply_markup(reply_markup=None)
    entry_hour = callback_data.get('entry_hour')
    working_hour_id = callback_data.get('id')

    await state.update_data(working_hour_id=working_hour_id)
    order = await state.get_data()
    master_id = order['master_id']

    await call.message.answer(f'{entry_hour}. Выбор сделан.')
    logging.info(f"{callback_data}")

    master_services = await get_masters_services(master_id)
    keyboard = get_services_keyboard(master_services)

    await call.message.answer(text="Что тебе нужно сделать?", reply_markup=keyboard)
    await OrderTrim.waiting_for_service.set()


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.answer("Вы отменили эту покупку!", show_alert=True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)
