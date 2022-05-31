import datetime


def generate_work_hours():
    """
    Генерирует список рабочих часов
    """
    time_begin = 10
    times = []
    while time_begin < 22:
        times.append(time_begin)
        time_begin += 1

    return times

def generate_hours():
    """
    Генерирует список рабочих часов
    """
    time_begin = datetime.datetime.strptime('2022-05-31', '%Y-%m-%d') + datetime.timedelta(hours=10)
    time_end = datetime.datetime.strptime('2022-05-31', '%Y-%m-%d') + datetime.timedelta(hours=21)
    step = datetime.timedelta(minutes=30)
    times = []
    while time_begin <= time_end:
        times.append(time_begin)
        time_begin += step

    return times