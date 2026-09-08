from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos_view, name='productos'),
    path('ubicacion/', views.ubicacion_view, name='ubicacion'),
    path('panel-admin/', views.admin_panel_view, name='admin_panel'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('politicas/', views.politicas_privacidad, name='politicas_privacidad'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('pago/', views.pago_view, name='pago'),
    # El panel es una pantalla del front; no requiere la app de administración
    # ni una base de datos.
    path('admin/', views.admin_panel_view),
]
