from rest_framework import viewsets
from .models import Cliente, Tienda, Contrato, SolicitudComercial
from .serializers import ClienteSerializer, TiendaSerializer, ContratoSerializer, SolicitudComercialSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    search_fields = ("nombres", "apellidos", "telefono", "correo", "ciudad")
    ordering_fields = ("nombres", "apellidos", "creado_en")

class TiendaViewSet(viewsets.ModelViewSet):
    queryset = Tienda.objects.all()
    serializer_class = TiendaSerializer
    search_fields = ("nombre", "direccion")

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related("cliente", "tienda", "creado_por").prefetch_related("productos", "pagos", "alertas")
    serializer_class = ContratoSerializer
    search_fields = ("numero", "cliente__nombres", "cliente__apellidos")
    filterset_fields = ("estado", "tienda", "cliente")
    ordering_fields = ("fecha_contrato", "fecha_entrega", "importe_original", "creado_en")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creado_por=user)

class SolicitudComercialViewSet(viewsets.ModelViewSet):
    queryset = SolicitudComercial.objects.select_related("contrato_creado", "creada_por")
    serializer_class = SolicitudComercialSerializer
    search_fields = ("client_name", "city", "channel", "template_code")
    filterset_fields = ("estado", "dress_type", "city")
    ordering_fields = ("creada_en", "event_date", "quoted_price")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creada_por=user)
