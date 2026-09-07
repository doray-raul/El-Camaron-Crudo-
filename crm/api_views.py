from rest_framework import viewsets

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer

    def get_queryset(self):
        queryset = Cliente.objects.all()

        estado = self.request.query_params.get('estado')
        etapa = self.request.query_params.get('etapa')
        search = self.request.query_params.get('search')

        if estado:
            queryset = queryset.filter(estado=estado)

        if etapa:
            queryset = queryset.filter(etapa=etapa)

        if search:
            queryset = queryset.filter(nombre__icontains=search)

        return queryset