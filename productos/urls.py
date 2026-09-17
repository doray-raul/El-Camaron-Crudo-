from django.urls import path

from . import views


urlpatterns = [
    path('productos/', views.productos_view, name='productos'),
]
