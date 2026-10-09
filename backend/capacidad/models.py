from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class TemporadaDemanda(models.Model):
    nombre = models.CharField(max_length=120)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    factor_demanda = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("1.00"), validators=[MinValueValidator(Decimal("0.01"))])
    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["fecha_inicio"]

    def __str__(self):
        return self.nombre


class SimulacionContrato(models.Model):
    class Resultado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente de evaluar"
        FACTIBLE = "factible", "Factible"
        CONDICIONES = "condiciones", "Factible con condiciones"
        NO_FACTIBLE = "no_factible", "No factible"

    fecha_simulacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega_solicitada = models.DateField()
    importe_propuesto = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    dinero_recibido_proyectado = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0"), validators=[MinValueValidator(Decimal("0"))])
    resultado = models.CharField(max_length=20, choices=Resultado.choices, default=Resultado.PENDIENTE)
    horas_requeridas = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0"))
    resumen_resultado = models.TextField(blank=True)
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="simulaciones_creadas")

    def __str__(self):
        return f"Simulación #{self.pk}"


class ProductoSimulacion(models.Model):
    simulacion = models.ForeignKey(SimulacionContrato, on_delete=models.CASCADE, related_name="productos")
    nombre = models.CharField(max_length=150)
    tipo_producto = models.CharField(max_length=50)
    tipo_trabajo = models.CharField(max_length=50)
    origen_taller = models.CharField(max_length=30)
    fecha_entrega = models.DateField(null=True, blank=True)
    horas_estimadas = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0"), validators=[MinValueValidator(Decimal("0"))])
    observaciones = models.TextField(blank=True)


class OperacionSimulada(models.Model):
    producto_simulado = models.ForeignKey(ProductoSimulacion, on_delete=models.CASCADE, related_name="operaciones")
    tipo_operacion = models.ForeignKey("produccion.TipoOperacion", on_delete=models.PROTECT, related_name="operaciones_simuladas")
    centro_trabajo = models.ForeignKey("produccion.CentroTrabajo", on_delete=models.PROTECT, null=True, blank=True, related_name="operaciones_simuladas")
    orden = models.PositiveIntegerField()
    horas_estimadas = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    class Meta:
        ordering = ["producto_simulado", "orden"]
