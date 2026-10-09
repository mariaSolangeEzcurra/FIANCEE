from django.conf import settings
from django.db import models


class Alerta(models.Model):
    class Tipo(models.TextChoices):
        PRIMERA_PRUEBA = "primera_prueba", "Seguimiento de primera prueba"
        INICIO_BORDADO = "inicio_bordado", "Inicio de bordado"
        ENTREGA_PROXIMA = "entrega_proxima", "Entrega próxima"
        SOBRECARGA = "sobrecarga", "Sobrecarga de capacidad"
        OPERACION_PENDIENTE = "operacion_pendiente", "Operación pendiente"
        OTRO = "otro", "Otra alerta"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ENVIADA = "enviada", "Enviada"
        ATENDIDA = "atendida", "Atendida"
        CANCELADA = "cancelada", "Cancelada"

    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    contrato = models.ForeignKey("contratos.Contrato", on_delete=models.CASCADE, null=True, blank=True, related_name="alertas")
    producto = models.ForeignKey("vestidos.ProductoTrabajo", on_delete=models.CASCADE, null=True, blank=True, related_name="alertas")
    operacion = models.ForeignKey("produccion.OperacionProducto", on_delete=models.CASCADE, null=True, blank=True, related_name="alertas")
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="alertas_recibidas")
    titulo = models.CharField(max_length=180)
    mensaje = models.TextField()
    fecha_programada = models.DateTimeField()
    fecha_atencion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha_programada"]
