from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (TemporadaDemandaViewSet, SimulacionContratoViewSet, ProductoSimulacionViewSet,
                    OperacionSimuladaViewSet, resumen_capacidad)
router = SimpleRouter()
router.register("temporadas-demanda", TemporadaDemandaViewSet, basename="temporada-demanda")
router.register("simulaciones", SimulacionContratoViewSet, basename="simulacion-contrato")
router.register("productos-simulacion", ProductoSimulacionViewSet, basename="producto-simulacion")
router.register("operaciones-simuladas", OperacionSimuladaViewSet, basename="operacion-simulada")
urlpatterns = router.urls + [path("capacidad/resumen/", resumen_capacidad, name="resumen-capacidad")]
