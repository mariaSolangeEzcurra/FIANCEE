from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


class Pago(models.Model):
    class Metodo(models.TextChoices):
        EFECTIVO = "efectivo", "Efectivo"
        TARJETA = "tarjeta", "Tarjeta"
        TRANSFERENCIA = "transferencia", "Transferencia"
        OTRO = "otro", "Otro"

    contrato = models.ForeignKey("contratos.Contrato", on_delete=models.PROTECT, null=True, blank=True, related_name="pagos")
    orden_interna = models.ForeignKey("vestidos.OrdenTrabajoInterna", on_delete=models.PROTECT, null=True, blank=True, related_name="pagos")
    fecha_pago = models.DateTimeField()
    importe = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    metodo = models.CharField(max_length=20, choices=Metodo.choices)
    referencia = models.CharField(max_length=120, blank=True)
    anulado = models.BooleanField(default=False)
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="pagos_registrados")
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_pago"]
        constraints = [models.CheckConstraint(condition=(Q(contrato__isnull=False, orden_interna__isnull=True) | Q(contrato__isnull=True, orden_interna__isnull=False)), name="pago_tiene_un_solo_destino")]

    def __str__(self):
        destino = self.contrato or self.orden_interna
        return f"Pago S/ {self.importe} - {destino}"


class ConfiguracionFinanciera(models.Model):
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    planilla = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("22000"), validators=[MinValueValidator(0)])
    servicios = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("1500"), validators=[MinValueValidator(0)])
    alquiler = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("2500"), validators=[MinValueValidator(0)])
    meta_mensual = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("40000"), validators=[MinValueValidator(0)])
    margen_objetivo = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal("0.35"), validators=[MinValueValidator(0), MaxValueValidator(1)])
    tasa_materiales = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal("0.22"), validators=[MinValueValidator(0), MaxValueValidator(1)])

    class Meta:
        ordering = ["-vigente_desde"]

    @property
    def total_costos_fijos(self):
        return self.planilla + self.servicios + self.alquiler


class Gasto(models.Model):
    concepto = models.CharField(max_length=180)
    fecha_vencimiento = models.DateField()
    importe = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["fecha_vencimiento"]


class CostoProducto(models.Model):
    producto = models.ForeignKey("vestidos.ProductoTrabajo", on_delete=models.PROTECT, related_name="costos")
    tipo = models.CharField(max_length=80)
    concepto = models.CharField(max_length=180, blank=True)
    importe = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    fecha = models.DateField()

    class Meta:
        ordering = ["-fecha"]
