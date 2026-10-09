from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Cliente(models.Model):
    nombres = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=120, blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["apellidos", "nombres"]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}".strip()


class Tienda(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Contrato(models.Model):
    class Estado(models.TextChoices):
        COTIZACION = "cotizacion", "Cotización"
        CONFIRMADO = "confirmado", "Confirmado"
        EN_PRODUCCION = "en_produccion", "En producción"
        ENTREGADO = "entregado", "Entregado"
        CANCELADO = "cancelado", "Cancelado"

    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="contratos")
    tienda = models.ForeignKey(Tienda, on_delete=models.PROTECT, related_name="contratos", null=True, blank=True)
    fecha_contrato = models.DateField()
    fecha_entrega = models.DateField()
    importe_original = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.COTIZACION)
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="contratos_creados")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha_entrega", "numero"]

    def __str__(self):
        return self.numero


class SolicitudComercial(models.Model):
    """Solicitud previa a la aceptación del contrato; no consume capacidad confirmada."""
    class Estado(models.TextChoices):
        NUEVA = "nueva", "Nueva"
        CONTACTADA = "contactada", "Contactada"
        SIMULADA = "simulada", "Simulada"
        CONVERTIDA = "convertida", "Convertida en contrato"
        DESCARTADA = "descartada", "Descartada"

    client_name = models.CharField(max_length=180)
    city = models.CharField(max_length=100, blank=True)
    summary = models.TextField(blank=True)
    dress_type = models.CharField(max_length=40, blank=True)
    event_date = models.DateField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    channel = models.CharField(max_length=80, blank=True)
    template_code = models.CharField(max_length=80, blank=True)
    complexity = models.CharField(max_length=30, blank=True)
    collection = models.CharField(max_length=80, blank=True)
    quoted_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    embroidery_level = models.CharField(max_length=30, blank=True)
    features = models.JSONField(default=list, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NUEVA)
    contrato_creado = models.ForeignKey(Contrato, on_delete=models.SET_NULL, null=True, blank=True, related_name="solicitudes_origen")
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="solicitudes_comerciales")
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada_en"]

    def __str__(self):
        return f"Solicitud: {self.client_name}"
