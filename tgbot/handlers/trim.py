import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from helpers.api import get_masters, get_masters_dates, get_masters_hours, get_masters_services, \
    get_user, ger_or_create_user, create_register
from helpers.states import OrderTrim
from keyboards.inline.callback_datas import master_callback, date_callback, hour_callback, service_callback
from keyboards.inline.choice_buttons import get_masters_keyboard, get_dates_keyboard, get_hours_keyboard, \
    get_services_keyboard
from keyboards.reply_keyboard.choice_buttons import get_share_phone_keyboard
from loader import dp, bot


@dp.message_handler(content_types=['contact'])
async def contact(message: Message, state: FSMContext):
    """
    Получает номер телефона
    """

    if message.contact is None:
        await message.answer("Что-то пошло не так. Давай попробуем еще раз")
        return

    await message.answer(
        'Благодуха, номер получен. Сейчас найдем тебя или создадим новый профиль',
        reply_markup=types.ReplyKeyboardRemove(),
    )

    user = await ger_or_create_user(message.contact, message.chat)

    if user:
        await message.answer(text=f"Привет, {user['first_name']}")
        await state.update_data(user_id=user['id'])
        masters = await get_masters()
        keyboard = get_masters_keyboard(masters)

        await message.answer(text="К кому пойдешь?", reply_markup=keyboard)
        await OrderTrim.waiting_for_master.set()


@dp.message_handler(Command("trim"), state='*')
async def order_trim(message: Message, state: FSMContext):
    """
    Инициализация записи и выбор мастера
    """

    chat_id = getattr(message.chat, 'id')
    username = getattr(message.chat, 'username')

    user = await get_user(chat_id)
    try:
        await message.answer(text=f"Привет, {user['first_name']}")
        await state.update_data(user_id=user['id'])
        masters = await get_masters()
        keyboard = get_masters_keyboard(masters)

        await message.answer(text="К кому пойдешь?", reply_markup=keyboard)
        await OrderTrim.waiting_for_master.set()
    except KeyError:
        keyboard = get_share_phone_keyboard()
        await message.answer(
            text=f"Привет, {username}. Похоже, мы впервые тут общаемся. Подскажи свой номер телефона",
            reply_markup=keyboard,
        )


@dp.callback_query_handler(master_callback.filter(), state=OrderTrim.waiting_for_master)
async def order_date(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Установим дату записи
    """
    await call.message.edit_reply_markup(reply_markup=None)
    master_id = callback_data.get('id')
    master_name = callback_data.get('name')
    await call.message.answer(f'{master_name} - отличный выбор.')
    await state.update_data(master_id=master_id)
    await state.update_data(master_name=master_name)
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


@dp.callback_query_handler(service_callback.filter(), state=OrderTrim.waiting_for_service)
async def order_service(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await call.message.edit_reply_markup(reply_markup=None)
    price_id = callback_data.get('id')

    order = await state.get_data()
    working_hour_id = order['working_hour_id']
    user_id = order['user_id']

    await call.message.answer('Принято. Сейчас запишем...')
    logging.info(f"{callback_data}")

    check_order = await create_register(user_id, working_hour_id, price_id)

    try:
        if check_order['state'] == 'new_register':
            call.message.answer('Готово.')
    except KeyError:
        call.message.answer('Возникла засада с записью. Попробуй чуть позже. Либо позвони Романычу, он все сделает.')


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.answer("Процесс записи абортирован!", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)
