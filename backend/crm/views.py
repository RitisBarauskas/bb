from datetime import datetime

from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from .models import Master, Price, UserCRM, WorkingHours
from .serializers import (MasterSerializer, PriceSerializer,
                          RegisterCreateSerializer,
                          UserCreateOrUpdateSerializer, UserCRMSerializer,
                          WorkingHoursSerializer, WorkingOnlyDatesSerializer)


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


class UserCRMView(views.APIView):
    """
    Получает или возвращает нового юзера
    """

    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk=None):
        if pk is None:
            return Response('Некорректный запрос', status=status.HTTP_400_BAD_REQUEST)

        queryset = UserCRM.objects.filter(chat_id=int(pk))

        result = {'data': None}

        if queryset.exists():
            result = UserCRMSerializer(
                instance=queryset,
                many=True,
            ).data[0]

        return Response(result)


class UserGetOrCreate(views.APIView):
    """
    Метод получения или регистрации пользователя
    """

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):

        phone = request.POST['phone']
        chat_id = request.POST['chat_id']
        try:
            first_name = request.POST['first_name']
        except KeyError:
            first_name = 'NoName'
        try:
            last_name = request.POST['last_name']
        except KeyError:
            last_name = 'NoLastName'
        telegram = request.POST['telegram']

        queryset = UserCRM.objects.filter(phone=phone)

        context = {'request': request}
        data = {
            'chat_id': chat_id,
            'first_name': first_name,
            'last_name': last_name,
            'telegram': telegram,
            'phone': phone,
            'username': phone,
        }

        if queryset.exists():
            serializer = UserCreateOrUpdateSerializer(
                instance=queryset.get(),
                data=data,
                context=context,
            )
        else:
            serializer = UserCreateOrUpdateSerializer(data=data, context=context)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class RegisterCreate(views.APIView):
    """
    Создает новую запись
    """

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):

        client_id = request.POST['user_id']
        working_hour_id = request.POST['working_hour_id']
        price_id = request.POST['price_id']

        context = {'request': request}
        data = {
            'client': int(client_id),
            'working_hour': int(working_hour_id),
            'price': int(price_id),
        }

        serializer = RegisterCreateSerializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
