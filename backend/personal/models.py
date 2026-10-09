from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Trabajadora(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="perfil_trabajadora")
    nombre = models.CharField(max_length=120)
    iniciales = models.CharField(max_length=8, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class HorarioTrabajadora(models.Model):
    DIAS = [(0, "Lunes"), (1, "Martes"), (2, "Miércoles"), (3, "Jueves"), (4, "Viernes"), (5, "Sábado"), (6, "Domingo")]
    trabajadora = models.ForeignKey(Trabajadora, on_delete=models.CASCADE, related_name="horarios")
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS, validators=[MinValueValidator(0), MaxValueValidator(6)])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    minutos_pausa = models.PositiveIntegerField(default=0)
    vigente_desde = models.DateField()
    vigente_hasta = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["trabajadora", "dia_semana", "hora_inicio"]


class AusenciaTrabajadora(models.Model):
    class Tipo(models.TextChoices):
        VACACIONES = "vacaciones", "Vacaciones"
        DESCANSO = "descanso", "Descanso"
        ENFERMEDAD = "enfermedad", "Enfermedad"
        PERMISO = "permiso", "Permiso"
        OTRO = "otro", "Otro"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        APROBADA = "aprobada", "Aprobada"
        RECHAZADA = "rechazada", "Rechazada"

    trabajadora = models.ForeignKey(Trabajadora, on_delete=models.CASCADE, related_name="ausencias")
    inicio = models.DateTimeField()
    fin = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    observaciones = models.TextField(blank=True)
    registrada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="ausencias_registradas")

    class Meta:
        ordering = ["inicio"]
