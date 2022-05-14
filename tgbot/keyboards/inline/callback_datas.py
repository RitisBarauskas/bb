from aiogram.utils.callback_data import CallbackData

master_callback = CallbackData("master", "name", "id")
date_callback = CallbackData("date", "date_str", "entry_date")
hour_callback = CallbackData("hour", "id", "entry_hour")
service_callback = CallbackData("service", "id")
