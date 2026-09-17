from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    ETAPAS = [
        ('PROSPECTO', 'Prospecto'),
        ('ACTIVO', 'Activo'),
        ('FRECUENTE', 'Frecuente'),
        ('INACTIVO', 'Inactivo'),
    ]

    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    etapa_crm = models.CharField(
        max_length=20,
        choices=ETAPAS,
        default='PROSPECTO'
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='ACTIVO'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Interaccion(models.Model):
    TIPOS = [
        ('LLAMADA', 'Llamada'),
        ('CORREO', 'Correo'),
        ('REUNION', 'Reunión'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='interacciones'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interacciones'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.cliente.nombre}'