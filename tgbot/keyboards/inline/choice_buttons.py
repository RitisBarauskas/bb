from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..inline.callback_datas import (date_callback, hour_callback,
                                     master_callback, service_callback)


def get_masters_keyboard(masters):
    """
    Получаем клавиатуру мастеров
    """
    buttons = []

    for master in masters:
        button = InlineKeyboardButton(
            text=master['name'],
            callback_data=master_callback.new(name=master['name'], id=master['id'])
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="Отмена", callback_data="next")
        ]
    ])

    return keyboard


def get_dates_keyboard(dates):
    """
    Метод получения клавиатуры дат
    """

    buttons = []

    for date in dates:
        button = InlineKeyboardButton(
            text=date['entry_date'],
            callback_data=date_callback.new(date_str=date['entry_date'], entry_date=date['entry_date'])
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[:3],
        buttons[3:],
    ])

    return keyboard


def get_hours_keyboard(hours):
    """
        Метод получения клавиатуры времени
        """

    buttons = []

    for hour in hours:
        time = hour['entry_hour'].replace(':', '-')[0:-3]
        button = InlineKeyboardButton(
            text=time,
            callback_data=hour_callback.new(id=hour['id'], entry_hour=time)
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[:5],
        buttons[5:],
    ])

    return keyboard


def get_services_keyboard(master_services):
    """
        Метод получения клавиатуры услуг, которые оказывает мастер
        """

    buttons = []

    for service in master_services:
        service_name = service['service']['name']
        button = InlineKeyboardButton(
            text=service_name,
            callback_data=service_callback.new(id=service['id'])
        )
        buttons.append(button)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        buttons[:1],
        buttons[1:2],
        buttons[2:3],
        buttons[3:4],
    ])

    return keyboard
