from datetime import datetime

from .models import UserCRM, Master, WorkingHours
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserCRMSerializer, MasterSerializer, WorkingHoursSerializer


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

