from django.db import models


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
    empresa = models.CharField(max_length=150, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    etapa = models.CharField(max_length=20, choices=ETAPAS, default='PROSPECTO')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVO')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre