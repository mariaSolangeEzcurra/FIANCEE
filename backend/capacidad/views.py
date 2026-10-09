from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TemporadaDemanda, SimulacionContrato, ProductoSimulacion, OperacionSimulada
from .serializers import TemporadaDemandaSerializer, SimulacionContratoSerializer, ProductoSimulacionSerializer, OperacionSimuladaSerializer
from produccion.models import OperacionProducto
from personal.models import Trabajadora

class TemporadaDemandaViewSet(viewsets.ModelViewSet):
    queryset = TemporadaDemanda.objects.all()
    serializer_class = TemporadaDemandaSerializer
    search_fields = ("nombre", "observaciones")
    filterset_fields = ("activa",)
    ordering_fields = ("fecha_inicio", "fecha_fin", "factor_demanda")

class SimulacionContratoViewSet(viewsets.ModelViewSet):
    queryset = SimulacionContrato.objects.select_related("creada_por").prefetch_related("productos__operaciones")
    serializer_class = SimulacionContratoSerializer
    filterset_fields = ("resultado", "fecha_entrega_solicitada")
    ordering_fields = ("fecha_simulacion", "fecha_entrega_solicitada", "horas_requeridas")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creada_por=user)

class ProductoSimulacionViewSet(viewsets.ModelViewSet):
    queryset = ProductoSimulacion.objects.select_related("simulacion").prefetch_related("operaciones")
    serializer_class = ProductoSimulacionSerializer
    filterset_fields = ("simulacion", "tipo_producto", "tipo_trabajo", "origen_taller")

class OperacionSimuladaViewSet(viewsets.ModelViewSet):
    queryset = OperacionSimulada.objects.select_related("producto_simulado", "tipo_operacion", "centro_trabajo")
    serializer_class = OperacionSimuladaSerializer
    filterset_fields = ("producto_simulado", "tipo_operacion", "centro_trabajo")
    ordering_fields = ("orden", "horas_estimadas")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def resumen_capacidad(request):
    operaciones_activas = OperacionProducto.objects.exclude(estado__in=[OperacionProducto.Estado.TERMINADA, OperacionProducto.Estado.CANCELADA])
    horas = operaciones_activas.aggregate(total=Sum("horas_estimadas"))["total"] or 0
    return Response({
        "trabajadoras_activas": Trabajadora.objects.filter(activa=True).count(),
        "operaciones_pendientes_o_en_curso": operaciones_activas.count(),
        "horas_estimadas_pendientes_o_en_curso": horas,
        "temporadas_activas": TemporadaDemanda.objects.filter(activa=True).count(),
        "simulaciones": SimulacionContrato.objects.count(),
        "nota": "Resumen inicial de carga estimada; la capacidad horaria disponible por semana se implementará como cálculo de planificación en una siguiente iteración."
    })
