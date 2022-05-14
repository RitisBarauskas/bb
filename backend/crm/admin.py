from django.contrib import admin

from .models import Master, Price, Register, Service, UserCRM, WorkingHours


@admin.register(UserCRM)
class UserCRMAdmin(admin.ModelAdmin):
    pass


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    pass


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    pass
