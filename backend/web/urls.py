from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('work-hours/', views.workhours, name='workhours'),
    path('', views.index, name='index'),
]