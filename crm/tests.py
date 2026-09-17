from django.test import TestCase
from django.urls import resolve



class RutasAPITests(TestCase):
    def test_api_crm_sigue_registrada(self):
        match = resolve('/crm/api/clientes/')

        self.assertEqual(match.func.cls.__name__, 'ClienteViewSet')
