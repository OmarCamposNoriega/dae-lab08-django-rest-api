from datetime import date
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Serie


class SerieAPITests(APITestCase):
    def setUp(self):
        self.s1 = Serie.objects.create(
            name='Breaking Bad',
            release_date=date(2008, 1, 20),
            rating=5,
            category=Serie.DRAMA,
        )

    def test_index_endpoint(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'mensaje': 'servidor activo'})

    def test_series_crud_flow(self):
        # GET lista
        res_list = self.client.get('/serie')
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        # POST crear Lost
        payload = {
            'name': 'Lost',
            'release_date': '2014-09-22',
            'rating': 4,
            'category': 'comedy',
        }
        res_post = self.client.post('/serie', payload, format='json')
        self.assertEqual(res_post.status_code, status.HTTP_201_CREATED)
        lost_id = res_post.data['id']

        # GET detalle
        res_get = self.client.get(f'/serie/{lost_id}')
        self.assertEqual(res_get.status_code, status.HTTP_200_OK)
        self.assertEqual(res_get.data['name'], 'Lost')

        # PUT actualizar Lost
        update_payload = {
            'name': 'Lost',
            'release_date': '2014-09-22',
            'rating': 5,
            'category': 'drama',
        }
        res_put = self.client.put(f'/serie/{lost_id}', update_payload, format='json')
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)
        self.assertEqual(res_put.data['rating'], 5)
        self.assertEqual(res_put.data['category'], 'drama')

        # DELETE
        res_del = self.client.delete(f'/serie/{lost_id}')
        self.assertEqual(res_del.status_code, status.HTTP_200_OK)
        self.assertFalse(Serie.objects.filter(pk=lost_id).exists())
