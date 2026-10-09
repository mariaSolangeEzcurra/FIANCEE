from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class VestidoStock(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=80, blank=True)
    observaciones = models.TextField(blank=True)
    disponible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class OrdenTrabajoInterna(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROCESO = "en_proceso", "En proceso"
        TERMINADA = "terminada", "Terminada"
        CANCELADA = "cancelada", "Cancelada"

    numero = models.CharField(max_length=50, unique=True)
    vestido_stock = models.ForeignKey(VestidoStock, on_delete=models.PROTECT, related_name="ordenes")
    fecha_ingreso = models.DateField()
    fecha_objetivo = models.DateField(null=True, blank=True)
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="ordenes_internas_creadas")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero


class ProductoTrabajo(models.Model):
    """Unidad de producción: producto de contrato o trabajo interno de stock, nunca ambos."""
    class TipoProducto(models.TextChoices):
        NOVIA = "Novia", "Novia"
        QUINCEANERA = "Quinceañera", "Quinceañera"
        VESTIDO_CAMBIO = "Vestido de cambio", "Vestido de cambio"
        DESMONTABLE = "Desmontable", "Desmontable"
        VELO = "Velo", "Velo"
        MINI_ME = "Mini me", "Mini me"
        ACCESORIO = "Accesorio", "Accesorio"
        OTRO = "Otro", "Otro"

    class Complejidad(models.TextChoices):
        BAJA = "Baja", "Baja"
        MEDIA = "Media", "Media"
        ALTA = "Alta", "Alta"
        MUY_ALTA = "Muy alta", "Muy alta"

    class Taller(models.TextChoices):
        A = "Taller A", "Taller A"
        C = "Taller C", "Taller C"
        OTRO = "Otro", "Otro"

    class Estado(models.TextChoices):
        EN_COLA = "En cola", "En cola"
        EN_PRODUCCION = "En producción", "En producción"
        TERMINADO = "Terminado", "Terminado"
        ENTREGADO = "Entregado", "Entregado"
        CANCELADO = "Cancelado", "Cancelado"

    class Prioridad(models.TextChoices):
        ALTA = "Alta", "Alta"
        MEDIA = "Media", "Media"
        NORMAL = "Normal", "Normal"

    contrato = models.ForeignKey("contratos.Contrato", on_delete=models.PROTECT, null=True, blank=True, related_name="productos")
    orden_interna = models.ForeignKey(OrdenTrabajoInterna, on_delete=models.PROTECT, null=True, blank=True, related_name="productos")
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150, blank=True)
    tipo = models.CharField(max_length=40, choices=TipoProducto.choices, default=TipoProducto.OTRO)
    corte_id = models.CharField(max_length=80, blank=True, help_text="Código de plantilla, por ejemplo princesa-volumen o taller-c")
    coleccion = models.CharField(max_length=80, blank=True)
    complejidad = models.CharField(max_length=20, choices=Complejidad.choices, default=Complejidad.MEDIA)
    taller = models.CharField(max_length=20, choices=Taller.choices, default=Taller.A)
    evento_fecha = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.EN_COLA)
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.NORMAL)
    caracteristicas = models.JSONField(default=list, blank=True)
    recibido_desde_taller_c = models.JSONField(default=list, blank=True)
    es_nuevo = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=(Q(contrato__isnull=False, orden_interna__isnull=True) | Q(contrato__isnull=True, orden_interna__isnull=False)), name="producto_tiene_un_solo_origen")]
        ordering = ["fecha_entrega", "codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre or self.get_tipo_display()}"


class NotaProducto(models.Model):
    class Tipo(models.TextChoices):
        OBSERVACION = "observacion", "Observación"
        INCIDENCIA = "incidencia", "Incidencia"

    producto = models.ForeignKey(ProductoTrabajo, on_delete=models.CASCADE, related_name="notas")
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="notas_producto")
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.OBSERVACION)

    class Meta:
        ordering = ["-fecha"]


class EvidenciaProducto(models.Model):
    producto = models.ForeignKey(ProductoTrabajo, on_delete=models.CASCADE, related_name="evidencias")
    archivo = models.ImageField(upload_to="vestidos/evidencias/")
    observacion = models.TextField(blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="evidencias_producto_subidas")

    class Meta:
        ordering = ["-fecha_carga"]


class ModificacionProducto(models.Model):
    class Estado(models.TextChoices):
        SOLICITADA = "solicitada", "Solicitada"
        APROBADA = "aprobada", "Aprobada"
        EN_PROCESO = "en_proceso", "En proceso"
        COMPLETADA = "completada", "Completada"
        RECHAZADA = "rechazada", "Rechazada"

    producto = models.ForeignKey(ProductoTrabajo, on_delete=models.PROTECT, related_name="modificaciones")
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.SOLICITADA)
    importe_adicional_propuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    importe_adicional_aprobado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    costo_adicional = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    solicitada_en = models.DateTimeField(auto_now_add=True)
    aprobada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="modificaciones_aprobadas")
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-solicitada_en"]
