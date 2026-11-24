import base64
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Categoria, Producto


class TiendaAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='Tecsup2023')
        self.cat = Categoria.objects.create(nombre='Gaseosas')
        self.prod = Producto.objects.create(
            categoria=self.cat,
            nombre='Coca Cola 500ml',
            precio='2.50',
            stock=10,
            descripcion='Bebida gasificada 500ml',
        )

    def test_categorias_and_productos_generic_views(self):
        res_cats = self.client.get('/tienda/categorias/')
        self.assertEqual(res_cats.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_cats.data), 1)

        res_post_prod = self.client.post(
            '/tienda/productos/',
            {
                'categoria': self.cat.id,
                'nombre': 'Inca Kola 500ml',
                'precio': '2.50',
                'stock': 15,
                'descripcion': 'Sabor nacional del Perú',
            },
            format='json',
        )
        self.assertEqual(res_post_prod.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_post_prod.data['categoria_nombre'], 'Gaseosas')

    def test_basic_authentication_endpoint(self):
        # Sin credenciales -> 401 Unauthorized
        res_unauth = self.client.get('/tienda/auth/productos/')
        self.assertEqual(res_unauth.status_code, status.HTTP_401_UNAUTHORIZED)

        # Con credenciales Basic Auth -> 200 OK
        token = base64.b64encode(b'admin:Tecsup2023').decode('utf-8')
        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {token}')
        res_auth = self.client.get('/tienda/auth/productos/')
        self.assertEqual(res_auth.status_code, status.HTTP_200_OK)

        res_status = self.client.get('/tienda/auth/status/')
        self.assertEqual(res_status.status_code, status.HTTP_200_OK)
        self.assertEqual(res_status.data['usuario'], 'admin')
