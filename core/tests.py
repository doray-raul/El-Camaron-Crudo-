from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Cliente


class RegistroPublicoTests(TestCase):
    def test_public_registration_creates_one_customer_profile(self):
        response = self.client.post(reverse('registro'), {'username': 'cliente', 'email': 'cliente@example.com', 'telefono': '555', 'password1': 'safe-password-123', 'password2': 'safe-password-123'})
        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='cliente')
        profile = Cliente.objects.get(usuario=user)
        self.assertEqual(profile.correo, 'cliente@example.com')
        self.assertEqual(Cliente.objects.filter(usuario=user).count(), 1)
