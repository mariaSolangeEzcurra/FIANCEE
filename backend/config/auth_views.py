from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Nombres de grupos en Django y sus identificadores para el frontend.
ROLES_PERMITIDOS = {
    "Comercial": "comercial",
    "Jefa de taller": "jefa_taller",
    "Taller": "taller",
    "Gerencia": "gerencia",
}

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def login_por_rol(request):
    """Autentica solo con usuario y contraseña; el perfil sale de los grupos asignados."""
    username = str(request.data.get("username", "")).strip()
    password = request.data.get("password", "")

    if not username or not password:
        return Response(
            {"detail": "Debes ingresar usuario y contraseña."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request=request, username=username, password=password)
    if user is None or not user.is_active:
        return Response(
            {"detail": "Usuario o contraseña incorrectos."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    grupos_usuario = list(user.groups.values_list("name", flat=True))
    roles = [
        role_id for nombre, role_id in ROLES_PERMITIDOS.items()
        if nombre in grupos_usuario
    ]

    # El superusuario debe poder entrar para administrar usuarios y asignar permisos.
    if user.is_superuser and not roles:
        roles = ["gerencia", "comercial", "jefa_taller", "taller"]

    if not roles:
        return Response(
            {"detail": "Tu cuenta todavía no tiene un área asignada. Solicita a Gerencia o al superadministrador que te asigne un rol."},
            status=status.HTTP_403_FORBIDDEN,
        )

    token, _ = Token.objects.get_or_create(user=user)
    perfil = getattr(user, "perfil_trabajadora", None)
    nombre = perfil.nombre if perfil else user.get_full_name() or user.get_username()

    return Response({
        "token": token.key,
        "username": user.get_username(),
        "nombre": nombre,
        "roles": roles,
        "rol": roles[0],
        "es_superusuario": user.is_superuser,
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_usuario(request):
    if request.auth:
        request.auth.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def usuario_actual(request):
    user = request.user
    perfil = getattr(user, "perfil_trabajadora", None)
    grupos = list(user.groups.values_list("name", flat=True))
    roles = [
        role_id for nombre, role_id in ROLES_PERMITIDOS.items()
        if nombre in grupos
    ]
    if user.is_superuser and not roles:
        roles = ["gerencia", "comercial", "jefa_taller", "taller"]
    return Response({
        "username": user.get_username(),
        "nombre": perfil.nombre if perfil else user.get_full_name() or user.get_username(),
        "roles": roles,
        "es_superusuario": user.is_superuser,
    })
