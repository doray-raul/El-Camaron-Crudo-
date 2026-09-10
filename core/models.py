from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    imagen = models.CharField(max_length=255, help_text='Ruta dentro de core/static, por ejemplo img/Producto1.jpeg')
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        PAGADO = 'PAGADO', 'Pagado'
        EN_PREPARACION = 'EN_PREPARACION', 'En preparación'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='pedidos')
    nombre_cliente = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=25, blank=True)
    direccion = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.nombre_cliente}'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, null=True, blank=True, on_delete=models.SET_NULL, related_name='detalles_pedido')
    nombre_producto = models.CharField(max_length=120)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'detalle de pedido'
        verbose_name_plural = 'detalles de pedido'

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f'{self.cantidad} × {self.nombre_producto}'
