from rest_framework.routers import SimpleRouter
from .views import (VestidoStockViewSet, OrdenTrabajoInternaViewSet, ProductoTrabajoViewSet,
                    NotaProductoViewSet, EvidenciaProductoViewSet, ModificacionProductoViewSet)
router = SimpleRouter()
router.register("vestidos-stock", VestidoStockViewSet, basename="vestido-stock")
router.register("ordenes-internas", OrdenTrabajoInternaViewSet, basename="orden-interna")
router.register("productos", ProductoTrabajoViewSet, basename="producto-trabajo")
router.register("notas-producto", NotaProductoViewSet, basename="nota-producto")
router.register("evidencias-producto", EvidenciaProductoViewSet, basename="evidencia-producto")
router.register("modificaciones-producto", ModificacionProductoViewSet, basename="modificacion-producto")
urlpatterns = router.urls
