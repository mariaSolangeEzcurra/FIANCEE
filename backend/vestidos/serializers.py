from rest_framework import serializers
from .models import VestidoStock, OrdenTrabajoInterna, ProductoTrabajo, NotaProducto, EvidenciaProducto, ModificacionProducto

class VestidoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VestidoStock
        fields = "__all__"
        read_only_fields = ("creado_en",)

class OrdenTrabajoInternaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenTrabajoInterna
        fields = "__all__"
        read_only_fields = ("creado_por", "creado_en")

class ProductoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoTrabajo
        fields = "__all__"
        read_only_fields = ("creado_en", "actualizado_en")

    def validate(self, attrs):
        contrato = attrs.get("contrato", getattr(self.instance, "contrato", None))
        orden = attrs.get("orden_interna", getattr(self.instance, "orden_interna", None))
        if (contrato is None) == (orden is None):
            raise serializers.ValidationError("El producto debe pertenecer a un contrato o a una orden interna, pero no a ambos.")
        return attrs

class NotaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaProducto
        fields = "__all__"
        read_only_fields = ("autor", "fecha")

class EvidenciaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenciaProducto
        fields = "__all__"
        read_only_fields = ("subido_por", "fecha_carga")

class ModificacionProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModificacionProducto
        fields = "__all__"
        read_only_fields = ("solicitada_en", "aprobada_por", "fecha_aprobacion")
