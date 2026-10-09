from rest_framework import viewsets
from .models import VestidoStock, OrdenTrabajoInterna, ProductoTrabajo, NotaProducto, EvidenciaProducto, ModificacionProducto
from .serializers import (VestidoStockSerializer, OrdenTrabajoInternaSerializer, ProductoTrabajoSerializer,
                          NotaProductoSerializer, EvidenciaProductoSerializer, ModificacionProductoSerializer)

class VestidoStockViewSet(viewsets.ModelViewSet):
    queryset = VestidoStock.objects.all()
    serializer_class = VestidoStockSerializer
    search_fields = ("codigo", "nombre", "tipo")
    filterset_fields = ("disponible", "tipo")
    ordering_fields = ("codigo", "nombre", "creado_en")

class OrdenTrabajoInternaViewSet(viewsets.ModelViewSet):
    queryset = OrdenTrabajoInterna.objects.select_related("vestido_stock", "creado_por").prefetch_related("productos", "pagos")
    serializer_class = OrdenTrabajoInternaSerializer
    search_fields = ("numero", "vestido_stock__codigo", "motivo")
    filterset_fields = ("estado", "vestido_stock")
    ordering_fields = ("fecha_ingreso", "fecha_objetivo", "creado_en")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creado_por=user)

class ProductoTrabajoViewSet(viewsets.ModelViewSet):
    queryset = ProductoTrabajo.objects.select_related("contrato", "orden_interna", "contrato__cliente").prefetch_related("operaciones", "pruebas", "notas", "evidencias", "modificaciones", "costos", "alertas")
    serializer_class = ProductoTrabajoSerializer
    search_fields = ("codigo", "nombre", "coleccion", "corte_id")
    filterset_fields = ("tipo", "complejidad", "taller", "estado", "prioridad", "contrato", "orden_interna")
    ordering_fields = ("fecha_entrega", "evento_fecha", "precio", "creado_en")

class NotaProductoViewSet(viewsets.ModelViewSet):
    queryset = NotaProducto.objects.select_related("producto", "autor")
    serializer_class = NotaProductoSerializer
    filterset_fields = ("producto", "tipo")
    ordering_fields = ("fecha",)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(autor=user)

class EvidenciaProductoViewSet(viewsets.ModelViewSet):
    queryset = EvidenciaProducto.objects.select_related("producto", "subido_por")
    serializer_class = EvidenciaProductoSerializer
    filterset_fields = ("producto",)
    ordering_fields = ("fecha_carga",)

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(subido_por=user)

class ModificacionProductoViewSet(viewsets.ModelViewSet):
    queryset = ModificacionProducto.objects.select_related("producto", "aprobada_por")
    serializer_class = ModificacionProductoSerializer
    filterset_fields = ("producto", "estado")
    ordering_fields = ("solicitada_en", "fecha_aprobacion")

    def perform_update(self, serializer):
        instance = self.get_object()
        new_status = serializer.validated_data.get("estado", instance.estado)
        if new_status == ModificacionProducto.Estado.APROBADA and instance.estado != new_status:
            from django.utils import timezone
            user = self.request.user if self.request.user.is_authenticated else None
            serializer.save(aprobada_por=user, fecha_aprobacion=timezone.now())
        else:
            serializer.save()
