from rest_framework import serializers
from .models import Pago, ConfiguracionFinanciera, Gasto, CostoProducto

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = "__all__"
        read_only_fields = ("registrado_por",)

    def validate(self, attrs):
        contrato = attrs.get("contrato", getattr(self.instance, "contrato", None))
        orden = attrs.get("orden_interna", getattr(self.instance, "orden_interna", None))
        if (contrato is None) == (orden is None):
            raise serializers.ValidationError("El pago debe estar vinculado a un contrato o a una orden interna, pero no a ambos.")
        return attrs

class ConfiguracionFinancieraSerializer(serializers.ModelSerializer):
    total_costos_fijos = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = ConfiguracionFinanciera
        fields = "__all__"

    def validate(self, attrs):
        inicio = attrs.get("vigente_desde", getattr(self.instance, "vigente_desde", None))
        fin = attrs.get("vigente_hasta", getattr(self.instance, "vigente_hasta", None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({"vigente_hasta": "La vigencia final no puede ser anterior a la inicial."})
        return attrs

class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = "__all__"

    def validate(self, attrs):
        pagado = attrs.get("pagado", getattr(self.instance, "pagado", False))
        fecha_pago = attrs.get("fecha_pago", getattr(self.instance, "fecha_pago", None))
        if pagado and not fecha_pago:
            raise serializers.ValidationError({"fecha_pago": "Indica la fecha de pago cuando el gasto figura como pagado."})
        return attrs

class CostoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostoProducto
        fields = "__all__"
