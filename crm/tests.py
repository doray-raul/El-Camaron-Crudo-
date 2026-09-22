from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Cliente, Interaccion


class CRMIntegrationTests(TestCase):
    def setUp(self):
        self.admin_group, _ = Group.objects.get_or_create(name='admin')
        self.employee_group, _ = Group.objects.get_or_create(name='empleado')
        self.admin = User.objects.create_user('admin', 'admin@example.com', 'password123')
        self.admin.groups.add(self.admin_group)
        self.employee = User.objects.create_user('employee', 'employee@example.com', 'password123')
        self.employee.groups.add(self.employee_group)
        self.public = User.objects.create_user('public', 'public@example.com', 'password123')
        self.client_record = Cliente.objects.create(nombre='Ana Cliente', correo='ana@example.com', telefono='123', etapa_crm='PROSPECTO')

    def test_public_user_cannot_enter_crm(self):
        self.client.force_login(self.public)
        self.assertEqual(self.client.get(reverse('dashboard')).status_code, 403)

    def test_employee_can_filter_clients_but_not_modify_or_delete(self):
        self.client.force_login(self.employee)
        self.assertContains(self.client.get(reverse('clientes') + '?etapa=PROSPECTO'), 'Ana Cliente')
        self.assertEqual(self.client.post(reverse('nuevo_cliente'), {}).status_code, 403)
        self.assertEqual(self.client.post(reverse('eliminar_cliente', args=[self.client_record.id])).status_code, 403)

    def test_admin_can_edit_and_delete_client(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('editar_cliente', args=[self.client_record.id]), {'nombre': 'Ana Actualizada', 'correo': 'ana@example.com', 'telefono': '456', 'etapa_crm': 'FRECUENTE', 'estado': 'ACTIVO'})
        self.assertRedirects(response, reverse('detalle_cliente', args=[self.client_record.id]))
        self.client_record.refresh_from_db()
        self.assertEqual(self.client_record.etapa_crm, 'FRECUENTE')
        self.assertRedirects(self.client.post(reverse('eliminar_cliente', args=[self.client_record.id])), reverse('clientes'))

    def test_interaction_uses_request_user_and_my_activity_is_scoped(self):
        other = User.objects.create_user('other', 'other@example.com', 'password123')
        other.groups.add(self.employee_group)
        Interaccion.objects.create(cliente=self.client_record, usuario=other, tipo='CORREO', descripcion='Otra')
        self.client.force_login(self.employee)
        response = self.client.post(reverse('nueva_interaccion'), {'cliente': self.client_record.id, 'tipo': 'LLAMADA', 'descripcion': 'Seguimiento'})
        self.assertRedirects(response, reverse('detalle_cliente', args=[self.client_record.id]))
        interaction = Interaccion.objects.get(descripcion='Seguimiento')
        self.assertEqual(interaction.usuario, self.employee)
        activity = self.client.get(reverse('mi_actividad'))
        self.assertContains(activity, 'Seguimiento')
        self.assertNotContains(activity, 'Otra')

    def test_admin_user_creation_assigns_group_without_interaction(self):
        self.client.force_login(self.admin)
        response = self.client.post(reverse('nuevo_usuario'), {'first_name': 'Eva', 'last_name': 'Empleado', 'email': 'eva@example.com', 'password': 'password123', 'password_confirmacion': 'password123', 'rol': 'empleado', 'is_active': 'on'})
        self.assertRedirects(response, reverse('usuarios'))
        user = User.objects.get(email='eva@example.com')
        self.assertTrue(user.groups.filter(name='empleado').exists())
        self.assertEqual(Interaccion.objects.count(), 0)

    def test_api_permissions_stage_and_metrics(self):
        api = APIClient()
        api.force_authenticate(self.employee)
        self.assertEqual(api.delete(reverse('cliente-detail', args=[self.client_record.id])).status_code, 403)
        self.assertEqual(api.put(reverse('cliente-cambiar-etapa', args=[self.client_record.id]), {'etapa_crm': 'ACTIVO'}, format='json').status_code, 403)
        self.assertEqual(api.get(reverse('cliente-detail', args=[self.client_record.id])).status_code, 200)
        api.force_authenticate(self.admin)
        response = api.put(reverse('cliente-cambiar-etapa', args=[self.client_record.id]), {'etapa_crm': 'ACTIVO'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(api.put(reverse('cliente-cambiar-etapa', args=[self.client_record.id]), {'etapa_crm': 'INVALIDA'}, format='json').status_code, 400)
        self.assertEqual(api.get(reverse('mis-interacciones')).status_code, 200)
        self.assertEqual(api.get('/crm/api/metricas/').status_code, 200)
