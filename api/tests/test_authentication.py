import email
from requests import request
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from api.models import Product, Catalogue
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from api.auth0 import Auth0
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings
from api.utils import jwt_decode_token, jwt_get_username_from_payload_handler

from rest_framework.exceptions import AuthenticationFailed

class TestAuthentication(APITestCase):

    list_url = reverse('products-list')

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient(enforce_csrf_checks=True)
        self.product = Product.objects.create()
        self.user = User.objects.create_user(username='cole', password='pass123', email='email@test.com')


    def test_should(self):
        request = self.client.get(self.list_url)

        #print(request)



    def test_should_check_get_request_with_jwt_passes(self):
        token = utils.jwt_create_payload(self.user)
        claim_set = utils.jwt_create_response_payload(token)
        #encoded = utils.jwt_decode_token(payload)
        #auth ='JWT {0}'.format(encoded)
        print(claim_set)

