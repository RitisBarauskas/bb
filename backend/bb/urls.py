from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('crm/', include('crm.urls', namespace='crm')),
    path('admin/', admin.site.urls),
    path('', include('web.urls', namespace='web')),
]
