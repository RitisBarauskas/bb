from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, MasterViewSet, WorkingHoursViewSet, PriceViewSet, WorkingDatesView, WorkingHoursView, \
    PriceView, UserCRMView, UserGetOrCreate, RegisterCreate

app_name = 'crm'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'masters', MasterViewSet)
# router.register(r'workinghours', WorkingHoursViewSet)
router.register(r'price', PriceViewSet)

urlpatterns = [
    path('working-dates/<str:pk>/', WorkingDatesView.as_view(), name='working-dates'),
    path('working-hours/<str:pk>/<str:entry_date>', WorkingHoursView.as_view(), name='working-hours'),
    path('master-service/<str:pk>', PriceView.as_view(), name='master-service'),
    path('get-user/<str:pk>', UserCRMView.as_view(), name='get-user'),
    path('get-or-create-user', UserGetOrCreate.as_view(), name='get-or-create-user'),
    path('create-register', RegisterCreate.as_view(), name='create-register'),
    path('', include(router.urls)),
]
