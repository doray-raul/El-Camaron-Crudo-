from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre',
            'correo',
            'telefono',
            'etapa',
            'estado',
            'fecha_registro',
        ]
        read_only_fields = ['id', 'fecha_registro']