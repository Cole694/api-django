from math import prod
from unicodedata import name
from django.test import TestCase
from api.models import Product, Catalogue

class TestProduct(TestCase):
    def test_fields(self):
        product = Product()
        product.name = 'test_product'
        product.save()

        record = Product.objects.get(pk=1)
        self.assertEqual(product, record)
