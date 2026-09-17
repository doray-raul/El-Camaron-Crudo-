from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from productos.models import Producto

from .models import DetallePedido, Pedido


class ModelosDeVentaTests(TestCase):
    def test_pedido_y_detalle_conservan_las_tablas_historicas(self):
        usuario = get_user_model().objects.create_user(username='cliente')
        producto = Producto.objects.create(
            nombre='Producto de prueba',
            descripcion='Descripción',
            precio=Decimal('10.00'),
            imagen='img/Producto1.jpeg',
        )
        pedido = Pedido.objects.create(
            usuario=usuario,
            nombre_cliente='Cliente de prueba',
            correo='cliente@example.com',
            subtotal=Decimal('10.00'),
            total=Decimal('10.00'),
        )
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            nombre_producto=producto.nombre,
            precio_unitario=producto.precio,
            cantidad=1,
        )

        self.assertEqual(Pedido._meta.db_table, 'core_pedido')
        self.assertEqual(DetallePedido._meta.db_table, 'core_detallepedido')
        self.assertEqual(detalle.subtotal, Decimal('10.00'))
        self.assertEqual(pedido.detalles.get(), detalle)
