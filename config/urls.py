from django.contrib import admin
from django.urls import include, path

from core import views as core_views
from crm import views as crm_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('productos/', core_views.productos_view, name='productos'),
    path('ubicacion/', core_views.ubicacion_view, name='ubicacion'),
    path('panel-admin/', core_views.admin_panel_view, name='admin_panel'),
    path('registro/', core_views.registro, name='registro'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('politicas/', core_views.politicas_privacidad, name='politicas_privacidad'),
    path('carrito/', core_views.carrito_view, name='carrito'),
    path('pago/', core_views.pago_view, name='pago'),
    path('crm/login/', crm_views.login_view, name='crm_login'),
    path('crm/logout/', crm_views.logout_view, name='crm_logout'),
    path('crm/', include('crm.urls')),
]
