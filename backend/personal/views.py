from rest_framework import viewsets
from .models import Trabajadora, HorarioTrabajadora, AusenciaTrabajadora
from .serializers import TrabajadoraSerializer, HorarioTrabajadoraSerializer, AusenciaTrabajadoraSerializer

class TrabajadoraViewSet(viewsets.ModelViewSet):
    queryset = Trabajadora.objects.select_related("usuario").prefetch_related("horarios", "ausencias", "habilidades")
    serializer_class = TrabajadoraSerializer
    search_fields = ("nombre", "iniciales", "cargo")
    filterset_fields = ("activa", "cargo")
    ordering_fields = ("nombre", "fecha_ingreso")

class HorarioTrabajadoraViewSet(viewsets.ModelViewSet):
    queryset = HorarioTrabajadora.objects.select_related("trabajadora")
    serializer_class = HorarioTrabajadoraSerializer
    filterset_fields = ("trabajadora", "dia_semana", "activo")
    ordering_fields = ("dia_semana", "hora_inicio")

class AusenciaTrabajadoraViewSet(viewsets.ModelViewSet):
    queryset = AusenciaTrabajadora.objects.select_related("trabajadora", "registrada_por")
    serializer_class = AusenciaTrabajadoraSerializer
    filterset_fields = ("trabajadora", "tipo", "estado")
    ordering_fields = ("inicio", "fin")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(registrada_por=user)
