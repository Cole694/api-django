from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings
from api.utils import jwt_decode_token, jwt_get_username_from_payload_handler
import jwt
from cryptography.hazmat.primitives import serialization

class TestUtils(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test', 'test@test.com', 'abc123')

    def test_should_check_jwt_get_username_from_payload_handler(self):
        user = '12345'
        payload = {'sub':'12345', 'email':'test@test.com', 'is_staff':False}
        username = jwt_get_username_from_payload_handler(payload)
        self.assertEqual(username, user)
"""
    def test_should_check_jwt_decode_token(self):# try include uuid with refactor
        headers = {"typ": "JWT", "alg": "RS256", "kid":"JhutschiIutrvjGrgx"}
        payload = {"sub": "127853487354", "name": "test"}

        private_key = open('.ssh/id_rsa', 'r').read()
        
        key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

        token = jwt.encode(payload=payload, key=key, algorithm='RS256', headers=headers)
        #print(token, '\n')
        util_func = jwt_decode_token(token)

"""