from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/nuevo/', views.nuevo_cliente_view, name='nuevo_cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente_view, name='detalle_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente_view, name='editar_cliente'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]