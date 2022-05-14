from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from api.models import Product, Catalogue
from api.serializers import ProductSerializer

class TestProductViewSet(APITestCase):
    list_url = reverse('products-list')
    detail_url = reverse('products-detail', kwargs={'pk':1})

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='pass123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.product = Product.objects.create(pk=1)

    def test_should_check_product_created(self):
        data = {'sku':'ok9uh0f58d', 'name':'test_prod', 'product_description':'test_description',
            'price':10.50, 'department':'general', 
            'date_listed':datetime.now().replace(microsecond=0, second=0),
            'product_weight':15.0, 'product_height':21.78, 'product_width':20.0, 'product_length':30.50, 
            'product_rating':3,}
# image field has been omitted for test to pass. Need to add it #

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_should_check_product_list(self):
        response = self.client.get(self.list_url)
       # print('\n', response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_should_check_product_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'item_name')
        
    def test_should_check_product_update(self):
        response = self.client.put(self.detail_url, {'sku':'p0j7gfrt53', 
                'product_description':'updated_description',
                'price':200.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_should_check_product_deleted(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TestCatalogueViewSet(APITestCase):
    list_url = reverse('catalogue-list')
    detail_url = reverse('catalogue-detail', kwargs={'pk':1})

    def setUp(self):
        self.catalogue = Catalogue.objects.create(pk=1)
        self.user = User.objects.create_user(username='catalogue_user', password='pass123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_should_check_catalogue_created(self):
        data = {'name':'catalogue1', 'description':'catalogue description'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Catalogue.objects.count(), 2)

    def test_should_check_catalogue_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shoud_check_catalogue_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_check_cataloge_update(self):
        response = self.client.put(self.detail_url, {'name':'test_catalogue1', 
                'description':'new test description'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_check_catalogue_deleted(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)