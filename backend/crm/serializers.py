import datetime

from .models import UserCRM, Master, WorkingHours, Price, Service, Register
from rest_framework import serializers


class UserCRMSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCRM
        exclude = 'password',


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'


class WorkingHoursSerializer(serializers.ModelSerializer):

    entry_hour = serializers.SerializerMethodField()

    def get_entry_hour(self, obj):

        return obj.entry.time()

    class Meta:
        model = WorkingHours
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):

    service = ServiceSerializer()

    class Meta:
        model = Price
        fields = '__all__'


class WorkingOnlyDatesSerializer(serializers.ModelSerializer):
    """
    Сериализатор дат
    """

    class Meta:
        model = WorkingHours
        fields = ('entry_date',)


class RegisterCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор журнала записи
    """

    client = serializers.PrimaryKeyRelatedField(queryset=UserCRM.objects.all())
    working_hour = serializers.PrimaryKeyRelatedField(queryset=WorkingHours.objects.filter(
        state=True,
        entry__gte=datetime.datetime.now(),
    ).all())
    price = serializers.PrimaryKeyRelatedField(queryset=Price.objects.all())

    def create(self, validated_data):
        return Register.objects.create(**validated_data)

    class Meta:
        model = Register
        fields = '__all__'
