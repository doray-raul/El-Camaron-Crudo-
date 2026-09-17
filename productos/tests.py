from django.test import TestCase
from django.urls import reverse

from .models import Producto


class CatalogoPublicoTests(TestCase):
    def test_ruta_de_productos_conserva_su_url_publica(self):
        response = self.client.get(reverse('productos'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productos.html')

    def test_producto_usa_la_tabla_historica(self):
        self.assertEqual(Producto._meta.db_table, 'core_producto')
