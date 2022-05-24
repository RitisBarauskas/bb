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
