from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_view, name='core_login'),
    path('logout/', views.logout_view, name='core_logout'),
    path('registro/', views.registro, name='registro'),
    path('productos/', views.productos_view, name='productos'),
    path('ubicacion/', views.ubicacion_view, name='ubicacion'),
    path('politicas/', views.politicas_privacidad, name='politicas'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('pago/', views.pago_view, name='pago'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]