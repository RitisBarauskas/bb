from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, MasterViewSet, WorkingHoursViewSet

app_name = 'crm'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'masters', MasterViewSet)
router.register(r'workinghours', WorkingHoursViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
