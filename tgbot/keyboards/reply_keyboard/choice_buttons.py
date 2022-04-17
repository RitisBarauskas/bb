from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_share_phone_keyboard():
    """
    Возвращает клавиатуру отправки своего номера телефона
    """

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton(
            text='Держи, бро, номерок!',
            request_contact=True,
        )
    )

    return keyboard
