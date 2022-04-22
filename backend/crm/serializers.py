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


class UserCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания или обновления пользователя
    """

    phone = serializers.CharField()
    password = serializers.CharField(required=False)
    username = serializers.CharField()
    chat_id = serializers.CharField()

    def create(self, validated_data):
        return UserCRM.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.chat_id = validated_data.pop('chat_id')
        instance.telegram = validated_data.pop('telegram')
        instance.first_name = validated_data.pop('first_name')
        instance.last_name = validated_data.pop('last_name')
        instance.save()

        return instance

    class Meta:
        model = UserCRM
        fields = '__all__'
