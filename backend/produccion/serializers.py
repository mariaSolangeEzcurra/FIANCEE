from rest_framework import serializers
from .models import (Taller, CentroTrabajo, HabilidadTrabajadora, TipoOperacion, PlantillaTiempo,
                     OperacionPlantilla, OperacionProducto, ResponsableOperacion,
                     RegistroTiempoOperacion, PruebaProducto)

class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = "__all__"

class CentroTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroTrabajo
        fields = "__all__"

class HabilidadTrabajadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabilidadTrabajadora
        fields = "__all__"

class TipoOperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoOperacion
        fields = "__all__"

class PlantillaTiempoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantillaTiempo
        fields = "__all__"

class OperacionPlantillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperacionPlantilla
        fields = "__all__"

class OperacionProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperacionProducto
        fields = "__all__"
        read_only_fields = ("creada_por", "creada_en", "actualizada_en")

    def validate(self, attrs):
        inicio = attrs.get("inicio_planificado", getattr(self.instance, "inicio_planificado", None))
        fin = attrs.get("fin_planificado", getattr(self.instance, "fin_planificado", None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({"fin_planificado": "El fin planificado no puede ser anterior al inicio."})
        return attrs

class ResponsableOperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableOperacion
        fields = "__all__"
        read_only_fields = ("asignada_en", "asignada_por")

class RegistroTiempoOperacionSerializer(serializers.ModelSerializer):
    minutos_registrados = serializers.IntegerField(read_only=True)
    class Meta:
        model = RegistroTiempoOperacion
        fields = "__all__"
        read_only_fields = ("registrado_por",)

    def validate(self, attrs):
        inicio = attrs.get("inicio_real", getattr(self.instance, "inicio_real", None))
        fin = attrs.get("fin_real", getattr(self.instance, "fin_real", None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({"fin_real": "El fin no puede ser anterior al inicio."})
        return attrs

class PruebaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PruebaProducto
        fields = "__all__"
