
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_root(request):
    base = request.build_absolute_uri("/api/")

    endpoints = [
        "clientes/",
        "tiendas/",
        "contratos/",
        "solicitudes-comerciales/",
        "trabajadoras/",
        "horarios-trabajadoras/",
        "ausencias/",
        "vestidos-stock/",
        "ordenes-internas/",
        "productos/",
        "notas-producto/",
        "evidencias-producto/",
        "modificaciones-producto/",
        "talleres/",
        "centros-trabajo/",
        "habilidades-trabajadoras/",
        "tipos-operacion/",
        "plantillas-tiempo/",
        "operaciones-plantilla/",
        "operaciones/",
        "responsables-operacion/",
        "registros-tiempo/",
        "pruebas/",
        "pagos/",
        "configuracion-financiera/",
        "gastos/",
        "costos-producto/",
        "finanzas/resumen/",
        "temporadas-demanda/",
        "simulaciones/",
        "productos-simulacion/",
        "operaciones-simuladas/",
        "capacidad/resumen/",
        "notificaciones/",
    ]

    return Response({
        "api": "Fiancée API",
        "version": "1.0",
        "endpoints": {
            endpoint.rstrip("/").replace("/", "_"): base + endpoint
            for endpoint in endpoints
        },
    })
