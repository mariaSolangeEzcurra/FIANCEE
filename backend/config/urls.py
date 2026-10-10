from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import api_root
from .auth_views import login_por_rol, logout_usuario, usuario_actual
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    path("api/auth/token/", obtain_auth_token, name="api-token-auth"),
    path("api/auth/login/", login_por_rol, name="api-login"),
    path("api/auth/logout/", logout_usuario, name="api-logout"),
    path("api/auth/me/", usuario_actual, name="api-current-user"),
    path("api/", include("contratos.urls")),
    path("api/", include("personal.urls")),
    path("api/", include("vestidos.urls")),
    path("api/", include("produccion.urls")),
    path("api/", include("finanzas.urls")),
    path("api/", include("capacidad.urls")),
    path("api/", include("notificaciones.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
