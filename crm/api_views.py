from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cliente, Interaccion
from .serializers import ClienteSerializer, InteraccionSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer

    def get_queryset(self):
        queryset = Cliente.objects.all()

        estado = self.request.query_params.get('estado')
        etapa_crm = self.request.query_params.get('etapa_crm')
        search = self.request.query_params.get('search')

        if estado:
            queryset = queryset.filter(estado=estado)

        if etapa_crm:
            queryset = queryset.filter(etapa_crm=etapa_crm)

        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(correo__icontains=search)
            )

        return queryset

    @action(detail=True, methods=['put'], url_path='etapa')
    def cambiar_etapa(self, request, pk=None):
        cliente = self.get_object()

        etapa_crm = request.data.get('etapa_crm')

        if etapa_crm is None:
            return Response(
                {'error': 'El campo etapa_crm es obligatorio.'},
                status=400
            )

        etapas_validas = dict(Cliente.ETAPAS)

        if etapa_crm not in etapas_validas:
            return Response(
                {'error': 'La etapa_crm proporcionada no es válida.'},
                status=400
            )

        cliente.etapa_crm = etapa_crm
        cliente.save(update_fields=['etapa_crm'])

        serializer = self.get_serializer(cliente)

        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='interacciones')
    def interacciones(self, request, pk=None):
        cliente = self.get_object()
        queryset = cliente.interacciones.all()
        serializer = InteraccionSerializer(queryset, many=True)

        return Response(serializer.data)


class InteraccionCreateView(generics.CreateAPIView):
    queryset = Interaccion.objects.all()
    serializer_class = InteraccionSerializer