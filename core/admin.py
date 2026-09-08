from django.contrib import admin

from .models import DetallePedido, Pedido, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible', 'creado_en')
    list_filter = ('disponible',)
    search_fields = ('nombre',)


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('nombre_producto', 'precio_unitario', 'cantidad', 'subtotal')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_cliente', 'correo', 'total', 'estado', 'creado_en')
    list_filter = ('estado',)
    search_fields = ('nombre_cliente', 'correo')
    inlines = (DetallePedidoInline,)
