from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaListCreateView(generics.ListCreateAPIView):
    """Lista todas las categorías (GET) o crea una nueva (POST) usando vistas genéricas."""
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer


class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene (GET), actualiza (PUT/PATCH) o elimina (DELETE) una categoría por PK."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoListCreateView(generics.ListCreateAPIView):
    """Lista todos los productos (GET) o registra un nuevo producto (POST) con vistas genéricas."""
    queryset = Producto.objects.select_related('categoria').all().order_by('id')
    serializer_class = ProductoSerializer


class ProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Obtiene (GET), actualiza (PUT/PATCH) o elimina (DELETE) un producto por PK."""
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer


class ProductoProtegidoListCreateView(generics.ListCreateAPIView):
    """Endpoint de Productos protegido con Autenticación Básica (BasicAuthentication)."""
    queryset = Producto.objects.select_related('categoria').all().order_by('id')
    serializer_class = ProductoSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class ProductoProtegidoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Detalle/Edición/Eliminación de Producto protegido con Autenticación Básica."""
    queryset = Producto.objects.select_related('categoria').all()
    serializer_class = ProductoSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class AuthCheckView(APIView):
    """Verifica credenciales enviadas por HTTP Basic Authentication."""
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'authenticated': True,
            'usuario': request.user.username,
            'es_admin': request.user.is_staff,
            'metodo_auth': 'BasicAuthentication',
            'mensaje': 'Acceso autorizado al servicio web protegido.',
        })
