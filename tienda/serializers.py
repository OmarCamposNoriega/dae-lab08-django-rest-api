from rest_framework import serializers
from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    total_productos = serializers.IntegerField(source='productos.count', read_only=True)

    class Meta:
        model = Categoria
        fields = ('id', 'nombre', 'imagen', 'pub_date', 'total_productos')


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = (
            'id',
            'categoria',
            'categoria_nombre',
            'nombre',
            'precio',
            'stock',
            'imagen',
            'descripcion',
            'pub_date',
        )
