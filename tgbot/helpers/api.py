import requests as requests

from tgbot.config import URL_API_CRM


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


