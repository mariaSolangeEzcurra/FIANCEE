from rest_framework import serializers
from .models import TemporadaDemanda, SimulacionContrato, ProductoSimulacion, OperacionSimulada

class TemporadaDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporadaDemanda
        fields = "__all__"

    def validate(self, attrs):
        inicio = attrs.get("fecha_inicio", getattr(self.instance, "fecha_inicio", None))
        fin = attrs.get("fecha_fin", getattr(self.instance, "fecha_fin", None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({"fecha_fin": "La fecha fin no puede ser anterior al inicio."})
        return attrs

class SimulacionContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulacionContrato
        fields = "__all__"
        read_only_fields = ("fecha_simulacion", "creada_por")

class ProductoSimulacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoSimulacion
        fields = "__all__"

class OperacionSimuladaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperacionSimulada
        fields = "__all__"
