from rest_framework.routers import SimpleRouter
from .views import TrabajadoraViewSet, HorarioTrabajadoraViewSet, AusenciaTrabajadoraViewSet
router = SimpleRouter()
router.register("trabajadoras", TrabajadoraViewSet, basename="trabajadora")
router.register("horarios-trabajadoras", HorarioTrabajadoraViewSet, basename="horario-trabajadora")
router.register("ausencias", AusenciaTrabajadoraViewSet, basename="ausencia")
urlpatterns = router.urls
