from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from .api_views import (
    ClienteViewSet,
    InteraccionCreateView,
    MetricasCRMView,
    MisInteraccionesView,
)


router = DefaultRouter()
router.register(r'api/clientes', ClienteViewSet, basename='cliente')


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('clientes/', views.clientes_view, name='clientes'),
    path('clientes/nuevo/', views.nuevo_cliente_view, name='nuevo_cliente'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente_view, name='detalle_cliente'),
    path('clientes/<int:cliente_id>/editar/', views.editar_cliente_view, name='editar_cliente'),
    path(
    'mi-actividad/',
    views.mi_actividad_view,
    name='mi_actividad'
),

path(
    'reportes-metricas/',
    views.reportes_metricas_view,
    name='reportes_metricas'
),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path(
    'usuarios/',
    views.usuarios_view,
    name='usuarios'
),

path(
    'usuarios/nuevo/',
    views.nuevo_usuario_view,
    name='nuevo_usuario'
),

path(
    'usuarios/<int:usuario_id>/editar/',
    views.editar_usuario_view,
    name='editar_usuario'
),

path(
    'perfil/',
    views.perfil_view,
    name='perfil'
),

path(
    'perfil/editar/',
    views.editar_perfil_view,
    name='editar_perfil'
),
]

urlpatterns += [
    path('api/interacciones/', InteraccionCreateView.as_view(), name='interaccion-create'),
    path('api/metricas/', MetricasCRMView.as_view()),
    path(
    'api/interacciones/mis-interacciones/',
    MisInteraccionesView.as_view(),
    name='mis-interacciones'
),
]


urlpatterns += router.urls
