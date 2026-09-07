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
        etapa = self.request.query_params.get('etapa')
        search = self.request.query_params.get('search')

        if estado:
            queryset = queryset.filter(estado=estado)

        if etapa:
            queryset = queryset.filter(etapa=etapa)

        if search:
            queryset = queryset.filter(nombre__icontains=search)

        return queryset
    
    @action(detail=True, methods=['get'], url_path='interacciones')
    def interacciones(self, request, pk=None):
        cliente = self.get_object()
        queryset = cliente.interacciones.all()
        serializer = InteraccionSerializer(queryset, many=True)
        return Response(serializer.data)


class InteraccionCreateView(generics.CreateAPIView):
    queryset = Interaccion.objects.all()
    serializer_class = InteraccionSerializer