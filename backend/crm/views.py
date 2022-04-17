from datetime import datetime

from django.db.models import DateField
from django.db.models.functions import Cast
from rest_framework.response import Response

from .models import UserCRM, Master, WorkingHours, Price
from rest_framework import viewsets, views, status
from rest_framework import permissions
from .serializers import UserCRMSerializer, MasterSerializer, WorkingHoursSerializer, PriceSerializer, \
    WorkingOnlyDatesSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API пользователей
    """
    queryset = UserCRM.objects.all()
    serializer_class = UserCRMSerializer
    permission_classes = [permissions.IsAuthenticated]


class MasterViewSet(viewsets.ModelViewSet):
    """
    API всех мастеров
    """
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = [permissions.AllowAny]


class WorkingHoursViewSet(viewsets.ModelViewSet):
    """
    API всех рабочих часов
    """
    queryset = WorkingHours.objects.filter(entry__gte=datetime.now()).all()
    serializer_class = WorkingHoursSerializer
    permission_classes = [permissions.AllowAny]


class PriceViewSet(viewsets.ModelViewSet):
    """
    API всех стоимостей услуг
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.AllowAny]


class WorkingDatesView(views.APIView):
    """
    Возвращает список рабочих дат
    """
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk=None):

        if pk is None:
            return Response('Не указан ID мастера', status=status.HTTP_400_BAD_REQUEST)

        queryset = WorkingHours.objects.filter(
            master_id=pk,
            state=True,
            entry__gte=datetime.now(),
        ).values('entry_date').distinct()

        serializer = WorkingOnlyDatesSerializer(
            instance=queryset,
            many=True,
        )

        return Response(serializer.data)


class WorkingHoursView(views.APIView):
    """
    Возвращает список рабочих часов
    """
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk=None, entry_date=None):

        if pk is None:
            return Response('Некорректный запрос', status=status.HTTP_400_BAD_REQUEST)

        queryset = WorkingHours.objects.filter(
            master_id=pk,
            entry_date=entry_date,
            state=True,
            entry__gte=datetime.now(),
        ).all()

        serializer = WorkingHoursSerializer(
            instance=queryset,
            many=True,
        )

        return Response(serializer.data)


class PriceView(views.APIView):
    """
    Возвращает список услуг и их стоимость, фильтруя по мастеру
    """
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk=None):

        if pk is None:
            return Response('Некорректный запрос', status=status.HTTP_400_BAD_REQUEST)

        queryset = Price.objects.filter(master_id=pk)

        serializer = PriceSerializer(
            instance=queryset,
            many=True,
        )

        return Response(serializer.data)
