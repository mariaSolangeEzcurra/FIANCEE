from rest_framework import serializers
from .models import Cliente, Tienda, Contrato, SolicitudComercial

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
        read_only_fields = ("creado_en",)

class TiendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tienda
        fields = "__all__"

class ContratoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombres", read_only=True)
    cliente_apellidos = serializers.CharField(source="cliente.apellidos", read_only=True)
    tienda_nombre = serializers.CharField(source="tienda.nombre", read_only=True, default=None)
    class Meta:
        model = Contrato
        fields = "__all__"
        read_only_fields = ("creado_por", "creado_en", "actualizado_en")

class SolicitudComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudComercial
        fields = "__all__"
        read_only_fields = ("creada_por", "creada_en")
