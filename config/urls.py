from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),
    path('', include('core.urls')),
    path('crm/', include('crm.urls')),
]
