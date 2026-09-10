from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login, registro y páginas generales de Core
    path('', include('core.urls')),

    # CRM
    path('', include('crm.urls')),
]