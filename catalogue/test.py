from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "sdfghjktrewsxcvhjk"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 
        'api.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'api.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': 'https://test_api/api',
    'JWT_ISSUER': 'https://dev-ec7a9tlw.us.auth0.com/',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}


