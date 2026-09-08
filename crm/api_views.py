from datetime import timedelta
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import EsAdminOEmpleadoSinEliminar
from .models import Cliente, Interaccion
from .serializers import ClienteSerializer, InteraccionSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    permission_classes = [EsAdminOEmpleadoSinEliminar]
    
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

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
class MetricasCRMView(generics.GenericAPIView):

    def get(self, request):
        fecha_limite = timezone.now() - timedelta(days=30)

        total_clientes = Cliente.objects.count()

        clientes_activos = Cliente.objects.filter(
            estado='ACTIVO'
        ).count()

        clientes_inactivos = Cliente.objects.filter(
            estado='INACTIVO'
        ).count()

        interacciones_por_cliente = Cliente.objects.annotate(
            total_interacciones=Count('interacciones')
        ).values(
            'id',
            'nombre',
            'total_interacciones'
        )

        clientes_sin_interaccion_reciente = Cliente.objects.exclude(
            interacciones__fecha__gte=fecha_limite
        ).values(
            'id',
            'nombre'
        )

        return Response({
            'total_clientes': total_clientes,
            'clientes_activos': clientes_activos,
            'clientes_inactivos': clientes_inactivos,
            'interacciones_por_cliente': list(
                interacciones_por_cliente
            ),
            'clientes_sin_interaccion_reciente': list(
                clientes_sin_interaccion_reciente
            ),
        })
        
        
class MisInteraccionesView(generics.ListAPIView):
    serializer_class = InteraccionSerializer

    def get_queryset(self):
        return Interaccion.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha')