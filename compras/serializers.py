from rest_framework import serializers
from .models import Proveedor, OrdenCompra, DetalleOrden, Categoria, Insumo

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        fields = ['id', 'proveedor', 'insumo', 'insumo_fk', 'unidad_medida', 'cantidad', 'precio_unitario', 'subtotal']

class OrdenCompraSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrdenCompra
        fields = '__all__'
