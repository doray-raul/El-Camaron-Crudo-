from rest_framework import serializers

from .models import Cliente, Interaccion


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
        
        
class InteraccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaccion
        fields = [
            'id',
            'cliente',
            'usuario',
            'tipo',
            'fecha',
            'descripcion',
        ]
        read_only_fields = ['id']
        