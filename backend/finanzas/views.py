from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Pago, ConfiguracionFinanciera, Gasto, CostoProducto
from .serializers import PagoSerializer, ConfiguracionFinancieraSerializer, GastoSerializer, CostoProductoSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.select_related("contrato", "orden_interna", "registrado_por")
    serializer_class = PagoSerializer
    filterset_fields = ("contrato", "orden_interna", "metodo", "anulado")
    search_fields = ("referencia", "observaciones", "contrato__numero", "orden_interna__numero")
    ordering_fields = ("fecha_pago", "importe")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(registrado_por=user)

class ConfiguracionFinancieraViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionFinanciera.objects.all()
    serializer_class = ConfiguracionFinancieraSerializer
    ordering_fields = ("vigente_desde", "meta_mensual")

class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer
    search_fields = ("concepto", "observaciones")
    filterset_fields = ("pagado",)
    ordering_fields = ("fecha_vencimiento", "importe", "fecha_pago")

class CostoProductoViewSet(viewsets.ModelViewSet):
    queryset = CostoProducto.objects.select_related("producto")
    serializer_class = CostoProductoSerializer
    filterset_fields = ("producto", "tipo")
    search_fields = ("tipo", "concepto", "producto__codigo")
    ordering_fields = ("fecha", "importe")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def resumen_financiero(request):
    hoy = timezone.localdate()
    inicio_mes = hoy.replace(day=1)
    pagos = Pago.objects.filter(anulado=False, fecha_pago__date__gte=inicio_mes, fecha_pago__date__lte=hoy).aggregate(total=Sum("importe"))["total"] or Decimal("0.00")
    gastos_pagados = Gasto.objects.filter(pagado=True, fecha_pago__gte=inicio_mes, fecha_pago__lte=hoy).aggregate(total=Sum("importe"))["total"] or Decimal("0.00")
    costos = ConfiguracionFinanciera.objects.filter(vigente_desde__lte=hoy).filter(vigente_hasta__isnull=True) | ConfiguracionFinanciera.objects.filter(vigente_desde__lte=hoy, vigente_hasta__gte=hoy)
    configuracion = costos.order_by("-vigente_desde").first()
    fijos = configuracion.total_costos_fijos if configuracion else Decimal("26000.00")
    return Response({
        "periodo_desde": inicio_mes,
        "periodo_hasta": hoy,
        "ingresos_cobrados_mes": pagos,
        "gastos_registrados_pagados_mes": gastos_pagados,
        "costos_fijos_mensuales_configurados": fijos,
        "diferencia_ingresos_menos_gastos_pagados": pagos - gastos_pagados,
        "margen_despues_de_costos_fijos_estimado": pagos - gastos_pagados - fijos,
        "nota": "Resumen de caja simplificado; no equivale a utilidad contable ni incluye ingresos aún no cobrados."
    })
