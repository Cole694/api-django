from datetime import datetime
from itertools import product
from django.core.exceptions import ValidationError
from django.forms import ImageField
from django.test import TestCase
from api.models import Product, Catalogue
from django.db.models.fields.files import ImageFieldFile

class TestProduct(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_prod = Product.objects.create(pk=1)
        cls.test_prod2 = Product.objects.create(pk=2)
        cls.test_catalogue = Catalogue.objects.create()

    def test_should_check_product_fields(self):
        self.assertIsInstance(self.test_prod.sku, str)
        self.assertIsInstance(self.test_prod.name, str)
        self.assertIsInstance(self.test_prod.product_description, str)
        self.assertIsInstance(self.test_prod.price, float)
        self.assertIsInstance(self.test_prod.department, str)
        self.assertIsInstance(self.test_prod.date_listed, datetime)
        self.assertIsInstance(self.test_prod.product_weight, float)
        self.assertIsInstance(self.test_prod.product_height, float)
        self.assertIsInstance(self.test_prod.product_width, float)
        self.assertIsInstance(self.test_prod.product_length, float)
        self.assertIsInstance(self.test_prod.product_image, ImageFieldFile)
        self.assertIsInstance(self.test_prod.product_rating, int)

    def test_should_check_num_products_in_catalogue(self):
        self.test_catalogue.product.set([self.test_prod.pk, self.test_prod2.pk])
        self.assertEqual(self.test_catalogue.product.count(), 2)

    def test_sould_check_sku_length(self):
        self.assertEqual(len(self.test_prod.sku), 10)

    def test_should_check_if_sku_is_unique(self):
        self.assertNotEqual(self.test_prod.sku, self.test_prod2.sku)

    def test_should_check_if_sku_is_unique_within_catalogue(self):
        self.test_catalogue.product.set([self.test_prod.pk, self.test_prod2.pk])
        self.assertNotEqual(self.test_catalogue.product.get(pk=1).sku, 
                            self.test_catalogue.product.get(pk=2).sku)

    def test_should_check_default_field_values_match_generated_field_values_when_crating_object(self):
        test_prod = Product.objects.create(name='item_name', product_description='description', 
            price=10.50, department='general', date_listed=datetime.now().replace(microsecond=0, second=0, minute=0), 
            product_weight=0.1, product_height=1 ,product_width=1 ,product_length=1 ,
            product_image='image/default.jpg', product_rating=1)
        test_prod2 = Product.objects.create()
# try search for testing objects (maybe validating them) against eachother
        self.assertEqual(test_prod.name, test_prod2.name)
        self.assertEqual(test_prod.product_description, test_prod2.product_description)
        self.assertEqual(test_prod.price, test_prod2.price)
        self.assertEqual(test_prod.department, test_prod2.department)
        self.assertEqual(test_prod.date_listed, test_prod2.date_listed)
        self.assertEqual(test_prod.product_weight, test_prod2.product_weight)
        self.assertEqual(test_prod.product_height, test_prod2.product_height)
        self.assertEqual(test_prod.product_width, test_prod2.product_width)
        self.assertEqual(test_prod.product_length, test_prod2.product_length)
        self.assertEqual(test_prod.product_image, test_prod2.product_image)
        self.assertEqual(test_prod.product_rating, test_prod2.product_rating)

    def test_should_check_field_validation_err_raises(self):
        with self.assertRaises(ValidationError):
            test_prod = Product(name='item_name', product_description='description', 
                price=0.05, department='general', date_listed=datetime.now().replace(microsecond=0, second=0), 
                product_weight=0, product_height=-1 ,product_width=-1 ,product_length=-1 ,
                product_rating=-1)
            test_prod.full_clean()

    def test_should_check_validation(self):
        #with self.assertRaises(ValidationError): # this line checks for a validation error being raised
            test_prod = Product( 
                price=10, 
                product_weight=16, product_height=14 ,product_width=15 ,product_length=21 ,
                product_rating=3)
            test_prod.full_clean()

class TestCatalogue(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_catalogue = Catalogue.objects.create(name='tet_cat1', description='description')
        
    def test_should_check_catalogue_fields(self):
        self.assertIsInstance(self.test_catalogue.name, str)
        self.assertIsInstance(self.test_catalogue.description, str)

    def test_should_check_catalogue_has_product(self):
        products = [Product.objects.create() for _ in range(3)]
        for item in products:
            item.catalogue.add(self.test_catalogue)
        
        self.assertEquals(len(products), self.test_catalogue.product.count())
        self.assertTrue(True, self.test_catalogue.product.exists())
            

    