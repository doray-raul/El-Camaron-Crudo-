from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible', 'creado_en')
    list_filter = ('disponible',)
    search_fields = ('nombre',)
