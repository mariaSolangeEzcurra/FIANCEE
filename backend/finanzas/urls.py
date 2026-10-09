from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (PagoViewSet, ConfiguracionFinancieraViewSet, GastoViewSet,
                    CostoProductoViewSet, resumen_financiero)
router = SimpleRouter()
router.register("pagos", PagoViewSet, basename="pago")
router.register("configuracion-financiera", ConfiguracionFinancieraViewSet, basename="configuracion-financiera")
router.register("gastos", GastoViewSet, basename="gasto")
router.register("costos-producto", CostoProductoViewSet, basename="costo-producto")
urlpatterns = router.urls + [path("finanzas/resumen/", resumen_financiero, name="resumen-financiero")]
