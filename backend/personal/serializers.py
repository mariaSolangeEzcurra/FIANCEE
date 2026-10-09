from rest_framework import serializers
from .models import Trabajadora, HorarioTrabajadora, AusenciaTrabajadora

class TrabajadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajadora
        fields = "__all__"

class HorarioTrabajadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioTrabajadora
        fields = "__all__"

    def validate(self, attrs):
        inicio = attrs.get("hora_inicio", getattr(self.instance, "hora_inicio", None))
        fin = attrs.get("hora_fin", getattr(self.instance, "hora_fin", None))
        if inicio and fin and fin <= inicio:
            raise serializers.ValidationError({"hora_fin": "La hora de fin debe ser posterior a la hora de inicio."})
        return attrs

class AusenciaTrabajadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AusenciaTrabajadora
        fields = "__all__"
        read_only_fields = ("registrada_por",)

    def validate(self, attrs):
        inicio = attrs.get("inicio", getattr(self.instance, "inicio", None))
        fin = attrs.get("fin", getattr(self.instance, "fin", None))
        if inicio and fin and fin <= inicio:
            raise serializers.ValidationError({"fin": "La fecha/hora de fin debe ser posterior al inicio."})
        return attrs
