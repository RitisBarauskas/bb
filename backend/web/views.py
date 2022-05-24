import datetime
from django.shortcuts import render

from web.helpers import generate_work_hours
from crm.models import Master, WorkingHours

def index(request):
    return render(request, 'web/index.html')


def workhours(request):
    """
    Метод формирования рабочих часов
    """
    if request.method == 'POST':
        pass
    else:
        masters = Master.objects.filter(state=True)
        result = {}
        for master in masters:
            day = WorkingHours.objects.filter(
                master=master,
                state=True,
            ).only('entry_date').order_by('-entry_date').first()

            today = datetime.date.today()
            if not day or (day and day < today):
                day = today
            days = {}
            day += datetime.timedelta(days=1)
            for new_day in range(1, 8):
                days[f'day{new_day}'] = day
                day += datetime.timedelta(days=1)

            result[master.id] = (master, days)

        context = {
            'data': result,
            'times': generate_work_hours(),
        }

        return render(request, 'web/work-hours.html', context=context)









