from base64 import decode
from email import header
from wsgiref import headers
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_jwt import utils
from rest_framework_jwt.settings import api_settings
from api.utils import jwt_decode_token, jwt_get_username_from_payload_handler
import jwt
from cryptography.hazmat.primitives import serialization
import http.client
import json
import responses
import requests

class TestUtils(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test', 'test@test.com', 'abc123')

    def test_should_check_jwt_get_username_from_payload_handler(self):
        user = '12345'
        payload = {'sub':'12345', 'email':'test@test.com', 'is_staff':False}
        username = jwt_get_username_from_payload_handler(payload)
        self.assertEqual(username, user)

    @responses.activate
    def test_should_check_jwt_decode_token(self):
        
        claim = {'iss': 'https://dev-ec7a9tlw.us.auth0.com/', 'sub': 'KWwVnoYEFoAQkrYmNDvdu7eXUEJ0h2Ub@clients', 'aud': 'https://test_api/api', 'iat': 1654511304, 'exp': 1654597704, 'azp': 'KWwVnoYEFoAQkrYmNDvdu7eXUEJ0h2Ub', 'gty': 'client-credentials'}
        token_details = '{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ilk5UUpFWFhuMWpoeDZ2cXl5WTZIMyJ9.eyJpc3MiOiJodHRwczovL2Rldi1lYzdhOXRsdy51cy5hdXRoMC5jb20vIiwic3ViIjoiS1d3Vm5vWUVGb0FRa3JZbU5EdmR1N2VYVUVKMGgyVWJAY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vdGVzdF9hcGkvYXBpIiwiaWF0IjoxNjU0NTExMzA0LCJleHAiOjE2NTQ1OTc3MDQsImF6cCI6IktXd1Zub1lFRm9BUWtyWW1ORHZkdTdlWFVFSjBoMlViIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.Xod5ZdVvqkX1DeJa044R_ABiF769JYW_pxzyE82arqJCrxdFoxuxb3Mfin1ceAFuhQtd1dyqAjNpP0c5xrAH4CT0IoYSX9wz7PKjHcYxYsQPyh7ljahLyfVqDexLpiCYNScCUAGv-UYo56B8D4TySQE9WCT1EobbeyU7Cpr-ReqQd9qoe3E4lCDEgy4mscdCeHF1coMjavE6mTd4si4eEjvXuial8nGySpwL4Pcczk_sBzbu_K07d-qX8FwzBB5nRx0s9DR0kU2I-nbHNx5q4RWF-x0Lj0kweh29adLzVJTZov7LR-lq_FQYcAChOSRgIYUFyv5dP0olDp0s9hKlPA","expires_in":"86400","token_type":"Bearer"}'

        responses.add(
            responses.GET, 
            'https://dev-ec7a9tlw.us.auth0.com/.well-known/jwks.json',
            body = '{"keys":[{"alg":"RS256","kty":"RSA","use":"sig","n":"xSOwAp5P0DL7jGM6UiMJi2Y-MZRYyigVjUJmIXeagiTDTlBnFA9OLkrcKDM8_f5GAM7CXNawAi4RTf3YyU2KQ1zS-rW4D1f5ko6JzNK-tBrPio-VyL9vNkBNp5bvL4lRsIzDrPeZ6Q2HBQqUrbJs7l3tLDoDDo0PtnjuG77fiAHRcKXb4y4tt0q1puli8zw8RaDfEDYrMTYgfYa-BghF6kajguHW-E7lzNGNA3DrqMz-ANRqe2qvNmQgH8Sm9Z7HEahS-FjWKorWn1TepfAVRXkHoiDZW9Fx35oRUbw4YC_pWNNRbtBb4bhTG-ioCFrn9UW6LLae6pvw5CXscG4Shw","e":"AQAB","kid":"Y9QJEXXn1jhx6vqyyY6H3","x5t":"JTU3JT3qSX7oV3Oaf_koZ11YArg","x5c":["MIIDDTCCAfWgAwIBAgIJNYSz318BcvtcMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi1lYzdhOXRsdy51cy5hdXRoMC5jb20wHhcNMjIwMzE2MTM0NjI3WhcNMzUxMTIzMTM0NjI3WjAkMSIwIAYDVQQDExlkZXYtZWM3YTl0bHcudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxSOwAp5P0DL7jGM6UiMJi2Y+MZRYyigVjUJmIXeagiTDTlBnFA9OLkrcKDM8/f5GAM7CXNawAi4RTf3YyU2KQ1zS+rW4D1f5ko6JzNK+tBrPio+VyL9vNkBNp5bvL4lRsIzDrPeZ6Q2HBQqUrbJs7l3tLDoDDo0PtnjuG77fiAHRcKXb4y4tt0q1puli8zw8RaDfEDYrMTYgfYa+BghF6kajguHW+E7lzNGNA3DrqMz+ANRqe2qvNmQgH8Sm9Z7HEahS+FjWKorWn1TepfAVRXkHoiDZW9Fx35oRUbw4YC/pWNNRbtBb4bhTG+ioCFrn9UW6LLae6pvw5CXscG4ShwIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRrVil4o6nDEC5o437gKymktH7+ezAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBADlTeL3n9QtVV8Jr+356fssI+Cm6wAgRCqjXrQxK3m+8ML25XNFZfxUcrOHLB3o2cGIYiYfrf0uv6rBDN/Gl7FeXENOvOq6b58hy90KdCVdNi/JWJnI7fthP+6/VOpx4TRuNt0DDdgHWtP3/2O+xq/gD7LZnasotYr5DAHLLCMCAdWxr9whSL0+KJdG+UugxlYFaduOUuuRAjxx9mGTrXLydrFT1VjGUrGctcrkAffWqRwkeGa/W9vZVwWq2uH/9TDLrLdMmaJjG0DirW43G/RDRQbOVwxkjPQQP9IQixVST9rYlziaPS+78CoKrNGVxVgyNh+veWOEf0KkK2D/WS6k="]},{"alg":"RS256","kty":"RSA","use":"sig","n":"ouK-o3H7yw2QBp6AqfnfmhlHvvmmojHk0F9VK8-U6RAcpomhBkDUeuchixoX879PVldroL0qHUCHpLz3qUZWfvtS5sQRH_o58zwYwTBoWx0DXdXmdIbLmX32xKnvNMY4g7XcAeqVXyDB6YEMECbk5Eqgqr-DEyrhK7te4UWwVPLImUpzyDyrPL0U8kpHMG2DEzoPqrF7uGsTNV0floRh-6wbvOFiZOlA7cCAielXZg2RGS7jQTqCgOv1fCpWSpYP8JGfq28ppcP3SaZms-YL3mTuNpX1-D1HlFNCQGhbRiloRcuIRi7HeAjJVlq4tmfuDVrQp346PYfssjAEInOMyw","e":"AQAB","kid":"-XiyMr0iRD1YMLsfDbEq4","x5t":"mSo3_bmFDs3h20ePISQPT07jiF4","x5c":["MIIDDTCCAfWgAwIBAgIJeQkY0Qse1lqCMA0GCSqGSIb3DQEBCwUAMCQxIjAgBgNVBAMTGWRldi1lYzdhOXRsdy51cy5hdXRoMC5jb20wHhcNMjIwMzE2MTM0NjI4WhcNMzUxMTIzMTM0NjI4WjAkMSIwIAYDVQQDExlkZXYtZWM3YTl0bHcudXMuYXV0aDAuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAouK+o3H7yw2QBp6AqfnfmhlHvvmmojHk0F9VK8+U6RAcpomhBkDUeuchixoX879PVldroL0qHUCHpLz3qUZWfvtS5sQRH/o58zwYwTBoWx0DXdXmdIbLmX32xKnvNMY4g7XcAeqVXyDB6YEMECbk5Eqgqr+DEyrhK7te4UWwVPLImUpzyDyrPL0U8kpHMG2DEzoPqrF7uGsTNV0floRh+6wbvOFiZOlA7cCAielXZg2RGS7jQTqCgOv1fCpWSpYP8JGfq28ppcP3SaZms+YL3mTuNpX1+D1HlFNCQGhbRiloRcuIRi7HeAjJVlq4tmfuDVrQp346PYfssjAEInOMywIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBT3wkUz+pa9+shZU75sLZsAgD3F6DAOBgNVHQ8BAf8EBAMCAoQwDQYJKoZIhvcNAQELBQADggEBAHtQ0ikgq/s47i8P2A3x4diMXmqVNlhFLqky4p4L6TsDL3AVtSXU5XILa5tJG+xDKmvsJf/QVcavEohu4zAL/ZQtaXeKKQwXAeteF8+FE+bOMPjtJNf13Ceuso+wUGgFCqKzCeTZpil5oCAQqAE6wDzh8AF+lAm2GYv1F60UEpZ+yAMPQ2QclNzaUfPYFDsEbmEXShvB1tusvdXwMraWa+vi7ptxXTV1agpRgNKysiLp8y8+w6RaP0ARNTr2Ti6awurt0VZHit35JZn7zdJntVfK+eVo5RZlyJFlPfa5yOHBp4fXLV9kyBDDYdGCU1zhpVp4e+XgAkH6Cl+ZnoIHHHE="]}]}',
            status = 200,
            content_type = 'application/json'
            )
        
        token_dict = json.loads(token_details)
        token = token_dict['access_token']

        func = jwt_decode_token(token)
        self.assertEqual(func, claim) 