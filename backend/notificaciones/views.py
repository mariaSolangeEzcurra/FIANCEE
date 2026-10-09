from rest_framework import viewsets
from .models import Alerta
from .serializers import AlertaSerializer

class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.select_related("contrato", "producto", "operacion", "destinatario")
    serializer_class = AlertaSerializer
    filterset_fields = ("tipo", "estado", "contrato", "producto", "operacion", "destinatario")
    search_fields = ("titulo", "mensaje")
    ordering_fields = ("fecha_programada", "fecha_atencion", "creada_en")
