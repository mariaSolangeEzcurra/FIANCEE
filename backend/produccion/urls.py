from rest_framework.routers import SimpleRouter
from .views import (TallerViewSet, CentroTrabajoViewSet, HabilidadTrabajadoraViewSet, TipoOperacionViewSet,
                    PlantillaTiempoViewSet, OperacionPlantillaViewSet, OperacionProductoViewSet,
                    ResponsableOperacionViewSet, RegistroTiempoOperacionViewSet, PruebaProductoViewSet)
router = SimpleRouter()
router.register("talleres", TallerViewSet, basename="taller")
router.register("centros-trabajo", CentroTrabajoViewSet, basename="centro-trabajo")
router.register("habilidades-trabajadoras", HabilidadTrabajadoraViewSet, basename="habilidad-trabajadora")
router.register("tipos-operacion", TipoOperacionViewSet, basename="tipo-operacion")
router.register("plantillas-tiempo", PlantillaTiempoViewSet, basename="plantilla-tiempo")
router.register("operaciones-plantilla", OperacionPlantillaViewSet, basename="operacion-plantilla")
router.register("operaciones", OperacionProductoViewSet, basename="operacion-producto")
router.register("responsables-operacion", ResponsableOperacionViewSet, basename="responsable-operacion")
router.register("registros-tiempo", RegistroTiempoOperacionViewSet, basename="registro-tiempo")
router.register("pruebas", PruebaProductoViewSet, basename="prueba-producto")
urlpatterns = router.urls
