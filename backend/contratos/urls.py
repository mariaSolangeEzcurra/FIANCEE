from rest_framework.routers import SimpleRouter
from .views import ClienteViewSet, TiendaViewSet, ContratoViewSet, SolicitudComercialViewSet
router = SimpleRouter()
router.register("clientes", ClienteViewSet, basename="cliente")
router.register("tiendas", TiendaViewSet, basename="tienda")
router.register("contratos", ContratoViewSet, basename="contrato")
router.register("solicitudes-comerciales", SolicitudComercialViewSet, basename="solicitud-comercial")
urlpatterns = router.urls
