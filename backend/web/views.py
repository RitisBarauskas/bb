import datetime
from django.shortcuts import render

from web.helpers import generate_work_hours
from crm.models import Master, WorkingHours


def index(request, day=None):
    today = datetime.date.today() + datetime.timedelta(days=1)

    masters = Master.objects.filter(state=True)
    result = {}
    for master in masters:
        entries = WorkingHours.objects.filter(entry_date=today, master=master)
        if not entries.exists():
            result[master] = None
            continue

        result[master] = entries

    context = {
        'data': result,
    }

    return render(request, 'web/index.html', context=context)


def workhours(request):
    """
    Метод формирования рабочих часов
    """
    DAYS = [f'day_{x}' for x in range(1, 8)]

    if request.method == 'POST':
        master = int(request.POST.get('master'))
        time_begin = int(request.POST.get('time_begin'))
        step = datetime.timedelta(minutes=int(request.POST.get('step')))
        time_end = int(request.POST.get('time_end'))

        entries = []
        for new_day in DAYS:
            day = request.POST.get(new_day)
            if not day:
                continue

            day = datetime.datetime.strptime(day, '%Y-%m-%d')
            entry_time = day + datetime.timedelta(hours=time_begin)
            finish_time = day + datetime.timedelta(hours=time_end)

            while entry_time < finish_time:
                entry = WorkingHours()
                entry.entry_date = day
                entry.entry = entry_time
                entry.master_id = master
                entries.append(entry)
                entry_time += step

        WorkingHours.objects.bulk_create(entries)
        return render(request, 'web/index.html')
    else:
        masters = Master.objects.filter(state=True)
        result = {}
        for master in masters:
            day = WorkingHours.objects.filter(
                master=master,
                state=True,
            ).only('entry_date').order_by('-entry_date').first()

            if day:
                day = day.entry_date

            today = datetime.date.today()
            if not day or (day and day < today):
                day = today
            days = {}
            day += datetime.timedelta(days=1)
            for new_day in DAYS:
                days[new_day] = day
                day += datetime.timedelta(days=1)

            result[master.id] = (master, days)

        context = {
            'data': result,
            'times': generate_work_hours(),
        }

        return render(request, 'web/work-hours.html', context=context)









