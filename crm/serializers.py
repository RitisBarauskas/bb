from .models import UserCRM, Master, WorkingHours, Price
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
    class Meta:
        model = WorkingHours
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'
