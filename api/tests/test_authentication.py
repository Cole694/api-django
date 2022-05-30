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
        jwt_sub = 'test.jwt.subject'
        payload = utils.jwt_create_payload(self.user)
        payload['sub'] = 'test|jwt|subject'
        util_function = jwt_get_username_from_payload_handler(payload)
        self.assertEqual(util_function, jwt_sub)
        

    def test_should_check_jwt_decode_token(self):# try include uuid with refactor

        headers = {"typ": "JWT", "alg": "RS256", "kid":"JhutschiIutrvjGrgx"}
        payload = {"sub": "127853487354", "name": "test"}

        private_key = open('.ssh/id_rsa', 'r').read()
        
        key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

        token = jwt.encode(payload=payload, key=key, algorithm='RS256', headers=headers)
        #print(token, '\n')
        util_func = jwt_decode_token(token)
        

class TestAuth0(APITestCase):

    list_url = list_url = reverse('products-list')

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test', 'test@test.com', 'abc123')

    def test_should_check_authorization_url(self):
        pass

    def test_should_check_access_token_url(self):
        pass

    def test_should_check_get_user_id(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url)
        details = {'username':'test_user', 'email':'test@test.com', 'user_id':'111'}
        auth_function = Auth0.get_user_id(self, details, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(auth_function, '111')

    def test_should_check_get_user_details(self):
        pass

