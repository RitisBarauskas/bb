import requests as requests
from decouple import config

URL_API_CRM = config('URL_API_CRM')


async def get_user(chat_id):
    """
    Получает пользователя
    """

    response = requests.get(URL_API_CRM + '/get-user/' + str(chat_id))

    return response.json()


async def ger_or_create_user(contact, chat):
    """
    Получает пользователя или создает нового
    """

    data = {
        'phone': contact.phone_number,
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'chat_id': contact.user_id,
        'telegram': chat.username,
    }

    response = requests.post(f"{URL_API_CRM}/get-or-create-user", data=data)

    return response.json()

async def get_masters():
    """
    Получает список мастеров
    """

    response = requests.get(URL_API_CRM+'/masters')

    return response.json()


async def get_masters_dates(master_id):
    """
    Получает список рабочих дат по ID мастера
    """

    response = requests.get(URL_API_CRM + '/working-dates/' + str(master_id))

    return response.json()


async def get_masters_hours(master_id, date):
    """
    Получает список рабочих часов определенного мастера в определенный день
    """

    response = requests.get(URL_API_CRM + '/working-hours/' + str(master_id) + '/' + str(date))

    return response.json()


async def get_masters_services(master_id):
    """
    Получает список того, что может сделать мастер
    """

    response = requests.get(URL_API_CRM + '/master-service/' + str(master_id))

    return response.json()


async def create_register(user_id, working_hour_id, price_id):
    """
    Создает новую запись в БД
    """

    data = {
        'user_id': user_id,
        'working_hour_id': working_hour_id,
        'price_id': price_id,
    }

    response = requests.post(f'{URL_API_CRM}/create-register', data=data)

    return response.json()