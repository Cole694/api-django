import email
from email.mime import application
from urllib import response
from django.test import TestCase
from requests import request
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from api.models import Product, Catalogue
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from api.auth0 import Auth0
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings
from api.utils import jwt_decode_token, jwt_get_username_from_payload_handler
import jwt
from cryptography.hazmat.primitives import serialization
import requests

class TestUtils(APITestCase):

    list_url = list_url = reverse('products-list')

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test', 'test@test.com', 'abc123')

    def test_should_check_jwt_get_username_from_payload_handler(self):

        user = '12345'
        payload = {'sub':'12345', 'email':'test@test.com', 'is_staff':False}
        username = jwt_get_username_from_payload_handler(payload)
        self.assertEqual(username, user)

    def test_should_check_jwt_decode_token(self):# try include uuid with refactor
        pass

