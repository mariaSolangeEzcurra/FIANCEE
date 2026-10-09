from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import (Taller, CentroTrabajo, HabilidadTrabajadora, TipoOperacion, PlantillaTiempo,
                     OperacionPlantilla, OperacionProducto, ResponsableOperacion,
                     RegistroTiempoOperacion, PruebaProducto)
from .serializers import (TallerSerializer, CentroTrabajoSerializer, HabilidadTrabajadoraSerializer,
                          TipoOperacionSerializer, PlantillaTiempoSerializer, OperacionPlantillaSerializer,
                          OperacionProductoSerializer, ResponsableOperacionSerializer,
                          RegistroTiempoOperacionSerializer, PruebaProductoSerializer)

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.prefetch_related("centros", "plantillas_tiempo")
    serializer_class = TallerSerializer
    search_fields = ("nombre",)
    filterset_fields = ("tipo", "activo")

class CentroTrabajoViewSet(viewsets.ModelViewSet):
    queryset = CentroTrabajo.objects.select_related("taller").prefetch_related("habilidades_personal", "tipos_operacion")
    serializer_class = CentroTrabajoSerializer
    search_fields = ("codigo", "nombre", "taller__nombre")
    filterset_fields = ("taller", "activo")

class HabilidadTrabajadoraViewSet(viewsets.ModelViewSet):
    queryset = HabilidadTrabajadora.objects.select_related("trabajadora", "centro_trabajo")
    serializer_class = HabilidadTrabajadoraSerializer
    filterset_fields = ("trabajadora", "centro_trabajo", "activa")

class TipoOperacionViewSet(viewsets.ModelViewSet):
    queryset = TipoOperacion.objects.select_related("centro_trabajo")
    serializer_class = TipoOperacionSerializer
    search_fields = ("codigo", "nombre")
    filterset_fields = ("centro_trabajo", "requiere_bordado", "activa")

class PlantillaTiempoViewSet(viewsets.ModelViewSet):
    queryset = PlantillaTiempo.objects.select_related("taller").prefetch_related("operaciones")
    serializer_class = PlantillaTiempoSerializer
    search_fields = ("codigo", "nombre")
    filterset_fields = ("taller", "activa")

class OperacionPlantillaViewSet(viewsets.ModelViewSet):
    queryset = OperacionPlantilla.objects.select_related("plantilla", "tipo_operacion")
    serializer_class = OperacionPlantillaSerializer
    filterset_fields = ("plantilla", "tipo_operacion")
    ordering_fields = ("orden", "horas_estimadas")

class OperacionProductoViewSet(viewsets.ModelViewSet):
    queryset = OperacionProducto.objects.select_related("producto", "tipo_operacion", "depende_de").prefetch_related("responsables", "registros_tiempo", "pruebas")
    serializer_class = OperacionProductoSerializer
    filterset_fields = ("producto", "tipo_operacion", "estado", "agregada_durante_produccion")
    search_fields = ("producto__codigo", "producto__nombre", "nombre_personalizado", "tipo_operacion__nombre")
    ordering_fields = ("orden", "inicio_planificado", "fin_planificado", "estado")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creada_por=user)

    @action(detail=True, methods=["post"])
    def iniciar(self, request, pk=None):
        operacion = self.get_object()
        trabajadora_id = request.data.get("trabajadora")
        if not trabajadora_id:
            raise ValidationError({"trabajadora": "Este campo es obligatorio para iniciar el registro de tiempo."})
        if operacion.estado == OperacionProducto.Estado.TERMINADA:
            raise ValidationError("No se puede iniciar una operación terminada.")
        if operacion.registros_tiempo.filter(fin_real__isnull=True).exists():
            raise ValidationError("Esta operación ya tiene un registro de tiempo abierto.")
        registro = RegistroTiempoOperacion.objects.create(
            operacion=operacion,
            trabajadora_id=trabajadora_id,
            inicio_real=timezone.now(),
            registrado_por=request.user if request.user.is_authenticated else None,
        )
        if operacion.inicio_real is None:
            operacion.inicio_real = registro.inicio_real
        operacion.estado = OperacionProducto.Estado.EN_CURSO
        operacion.save(update_fields=["inicio_real", "estado", "actualizada_en"])
        return Response({"operacion": OperacionProductoSerializer(operacion, context={"request": request}).data,
                         "registro_tiempo": RegistroTiempoOperacionSerializer(registro).data}, status=status.HTTP_201_CREATED)

class ResponsableOperacionViewSet(viewsets.ModelViewSet):
    queryset = ResponsableOperacion.objects.select_related("operacion", "trabajadora", "asignada_por")
    serializer_class = ResponsableOperacionSerializer
    filterset_fields = ("operacion", "trabajadora", "activa")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(asignada_por=user)

class RegistroTiempoOperacionViewSet(viewsets.ModelViewSet):
    queryset = RegistroTiempoOperacion.objects.select_related("operacion", "trabajadora", "registrado_por")
    serializer_class = RegistroTiempoOperacionSerializer
    filterset_fields = ("operacion", "trabajadora")
    ordering_fields = ("inicio_real", "fin_real")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(registrado_por=user)

    @action(detail=True, methods=["post"])
    def finalizar(self, request, pk=None):
        registro = self.get_object()
        if registro.fin_real is not None:
            raise ValidationError("Este registro de tiempo ya está finalizado.")
        ahora = timezone.now()
        registro.fin_real = ahora
        registro.save(update_fields=["fin_real"])
        operacion = registro.operacion
        if not operacion.registros_tiempo.filter(fin_real__isnull=True).exists():
            operacion.fin_real = ahora
            operacion.estado = OperacionProducto.Estado.TERMINADA
            operacion.save(update_fields=["fin_real", "estado", "actualizada_en"])
        return Response({"registro_tiempo": self.get_serializer(registro).data,
                         "operacion": OperacionProductoSerializer(operacion, context={"request": request}).data})

class PruebaProductoViewSet(viewsets.ModelViewSet):
    queryset = PruebaProducto.objects.select_related("producto", "operacion")
    serializer_class = PruebaProductoSerializer
    filterset_fields = ("producto", "operacion", "estado")
    ordering_fields = ("numero", "fecha_planificada", "fecha_real")
