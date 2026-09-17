from django.test import TestCase


class PaginasPublicasTests(TestCase):
    def test_paginas_publicas_renderizan(self):
        for ruta in ('/', '/login/', '/registro/', '/ubicacion/', '/politicas/', '/carrito/', '/pago/'):
            with self.subTest(ruta=ruta):
                response = self.client.get(ruta)
                self.assertEqual(response.status_code, 200)
