from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Taller(models.Model):
    class Tipo(models.TextChoices):
        INTERNO = "interno", "Interno"
        EXTERNO = "externo", "Externo"

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.INTERNO)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CentroTrabajo(models.Model):
    taller = models.ForeignKey(Taller, on_delete=models.PROTECT, related_name="centros")
    codigo = models.CharField(max_length=40)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["taller", "codigo"], name="centro_codigo_unico_por_taller")]
        ordering = ["taller", "nombre"]

    def __str__(self):
        return f"{self.taller.nombre} - {self.nombre}"


class HabilidadTrabajadora(models.Model):
    trabajadora = models.ForeignKey("personal.Trabajadora", on_delete=models.CASCADE, related_name="habilidades")
    centro_trabajo = models.ForeignKey(CentroTrabajo, on_delete=models.PROTECT, related_name="habilidades_personal")
    nivel = models.CharField(max_length=50, blank=True)
    horas_maximas_dia = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(Decimal("0.01"))])
    activa = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["trabajadora", "centro_trabajo"], name="habilidad_unica_por_centro")]


class TipoOperacion(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    centro_trabajo = models.ForeignKey(CentroTrabajo, on_delete=models.PROTECT, null=True, blank=True, related_name="tipos_operacion")
    requiere_bordado = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class PlantillaTiempo(models.Model):
    codigo = models.CharField(max_length=80, unique=True)
    nombre = models.CharField(max_length=120)
    taller = models.ForeignKey(Taller, on_delete=models.PROTECT, related_name="plantillas_tiempo")
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class OperacionPlantilla(models.Model):
    plantilla = models.ForeignKey(PlantillaTiempo, on_delete=models.CASCADE, related_name="operaciones")
    tipo_operacion = models.ForeignKey(TipoOperacion, on_delete=models.PROTECT, related_name="operaciones_plantilla")
    orden = models.PositiveIntegerField()
    horas_estimadas = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    class Meta:
        ordering = ["plantilla", "orden"]
        constraints = [models.UniqueConstraint(fields=["plantilla", "orden"], name="orden_unico_por_plantilla")]


class OperacionProducto(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_CURSO = "en_curso", "En curso"
        PAUSADA = "pausada", "Pausada"
        TERMINADA = "terminada", "Terminada"
        CANCELADA = "cancelada", "Cancelada"

    producto = models.ForeignKey("vestidos.ProductoTrabajo", on_delete=models.PROTECT, related_name="operaciones")
    tipo_operacion = models.ForeignKey(TipoOperacion, on_delete=models.PROTECT, related_name="operaciones_producto")
    nombre_personalizado = models.CharField(max_length=150, blank=True)
    orden = models.PositiveIntegerField()
    horas_estimadas = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    inicio_planificado = models.DateTimeField(null=True, blank=True)
    fin_planificado = models.DateTimeField(null=True, blank=True)
    inicio_real = models.DateTimeField(null=True, blank=True)
    fin_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    depende_de = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="operaciones_dependientes")
    agregada_durante_produccion = models.BooleanField(default=False)
    motivo_cambio = models.TextField(blank=True)
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="operaciones_creadas")
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["producto", "orden", "id"]
        constraints = [models.UniqueConstraint(fields=["producto", "orden"], name="orden_unico_por_producto")]

    def __str__(self):
        return self.nombre_personalizado or f"{self.tipo_operacion.nombre} - {self.producto.codigo}"


class ResponsableOperacion(models.Model):
    operacion = models.ForeignKey(OperacionProducto, on_delete=models.CASCADE, related_name="responsables")
    trabajadora = models.ForeignKey("personal.Trabajadora", on_delete=models.PROTECT, related_name="asignaciones_operacion")
    asignada_en = models.DateTimeField(auto_now_add=True)
    asignada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="asignaciones_realizadas")
    activa = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["operacion", "trabajadora"], name="responsable_unico_por_operacion")]


class RegistroTiempoOperacion(models.Model):
    operacion = models.ForeignKey(OperacionProducto, on_delete=models.PROTECT, related_name="registros_tiempo")
    trabajadora = models.ForeignKey("personal.Trabajadora", on_delete=models.PROTECT, related_name="registros_tiempo")
    inicio_real = models.DateTimeField()
    fin_real = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="tiempos_registrados")

    class Meta:
        ordering = ["inicio_real"]

    @property
    def minutos_registrados(self):
        if self.fin_real is None or self.fin_real < self.inicio_real:
            return None
        return int((self.fin_real - self.inicio_real).total_seconds() // 60)


class PruebaProducto(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        REALIZADA = "realizada", "Realizada"
        REPROGRAMADA = "reprogramada", "Reprogramada"
        CANCELADA = "cancelada", "Cancelada"

    producto = models.ForeignKey("vestidos.ProductoTrabajo", on_delete=models.PROTECT, related_name="pruebas")
    operacion = models.ForeignKey(OperacionProducto, on_delete=models.SET_NULL, null=True, blank=True, related_name="pruebas")
    numero = models.PositiveIntegerField()
    fecha_planificada = models.DateTimeField(null=True, blank=True)
    fecha_real = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["producto", "numero"]
        constraints = [models.UniqueConstraint(fields=["producto", "numero"], name="numero_prueba_unico_por_producto")]
