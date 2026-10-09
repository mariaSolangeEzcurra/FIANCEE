from rest_framework.routers import SimpleRouter
from .views import AlertaViewSet
router = SimpleRouter()
router.register("notificaciones", AlertaViewSet, basename="notificacion")
urlpatterns = router.urls
