# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from rest_framework import ISO_8601

import os

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '192.168.2.69']

PROJECT_NAME = 'FPT Camera'

# TIMEZONE
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_TZ = True

REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.StaticHTMLRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_THROTTLE_CLASSES': (),
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': None,

    # Generic view behavior
    'DEFAULT_PAGINATION_CLASS': None,
    'DEFAULT_FILTER_BACKENDS': (),

    # Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',

    # Throttling
    'DEFAULT_THROTTLE_RATES': {
        'user': None,
        'anon': None,
    },
    'NUM_PROXIES': None,

    # Pagination
    'PAGE_SIZE': None,

    # Filtering
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',

    # Versioning
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',

    # Authentication
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    'UNAUTHENTICATED_TOKEN': None,

    # View configuration
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',

    # Exception handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',

    # Testing
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',

    # Hyperlink settings
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',

    # Input and output formats
    'DATE_FORMAT': ISO_8601,
    'DATE_INPUT_FORMATS': (ISO_8601,),

    'DATETIME_FORMAT': ISO_8601,
    'DATETIME_INPUT_FORMATS': (ISO_8601,),

    'TIME_FORMAT': ISO_8601,
    'TIME_INPUT_FORMATS': (ISO_8601,),

    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,

    # Browseable API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",

    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}

# DJANGO PROMETHEUS
# settings.INSTALLED_APPS += ['django_prometheus']
# PROMETHEUS_BEGIN = ['django_prometheus.middleware.PrometheusBeforeMiddleware']
# PROMETHEUS_END = ['django_prometheus.middleware.PrometheusAfterMiddleware']
# settings.MIDDLEWARE = PROMETHEUS_BEGIN + settings.MIDDLEWARE + PROMETHEUS_END

# Config SSL
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Time Retry Server
REQUEST_RETRY = 120000
AUTH_CODE_RETRY = 120000
RE_AUTH_CODE_SERVER = 'https://prod-management.iotc.vn'
CONFIG_SERVER = '192.168.2.69:8000'

# Libraries embedded
LIB_IPC_HMAC_PATH = os.path.join('libraries/libFPTHmac.so')

# Image file formats
IMAGE_FILE_FORMAT = ['png', 'gif', 'jpeg', 'jpg', 'svg', 'icon']
PATH_IMAGE_BRAND = 'images/brand/'

# Stream Config
STREAM_PROTOCOL = ['rtmp']

# SMS Gateway
SENDSMS_BACKEND = 'sendsms.backends.console.SmsBackend'
SENDSMS_FROM_NUMBER = ''

# JSON Format
JSON_SCHEMA_FORM = {}

# ACCESS POINT
ACCESS_POINT_PASSWORD = '123456'
ACCESS_POINT_SECRET_KEY = ''

# Camera account
CAMERA_ACCOUNT_SECRET_KEY = '2A=n2eWM%=sZkc7#'
CAMERA_ACCOUNT_USERNAME = 'admin'
CAMERA_ACCOUNT_PASSWORD = ''

# TOKEN SECRET
TOKEN_SECRET_KEY_ALGORITHM = 'sha256'
TOKEN_SECRET_KEY_MAX_LENGTH = 8
TOKEN_SECRET_KEY_CIRCLE = 4
TOKEN_SECRET_KEY_POSITION = 1
TOKEN_SECRET_KEY_DEFAULT = 'P9$1w@ev'
TOKEN_SECRET_KEY_SPECIAL_CHARACTER = '*'
TOKEN_IV = '4e5Wa71fYoT7MFEX'

# FTP System
API_FTP_PROTOCOL = 'http'
API_FTP_HOST = 'prod-ftp.iotc.vn'
FTP_SECRET_KEY = '@9wJq+%K+qZ*t3&='

# QUEUE SYSTEM
API_QUEUE_PROTOCOL = 'https'
API_QUEUE_SERVER = 'prod-queue.iotc.vn'
API_QUEUE_GIS = 'b7a5b38faa5049cd9ff979bddf5b88ea'
API_QUEUE_TLS_VERSION = ['tlsv1', 'tlsv1.1', 'tlsv1.2']
API_QUEUE_IS_MQTT = True
API_QUEUE_ENABLE = True
API_QUEUE_CA_PATH = os.path.join('certificate/mqtt/')
API_QUEUE_CA_FILE = 'ca.crt'

WOWZA_SERVER = '192.168.2.53'
WOWZA_PORT = [8088, 1935]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(settings.MEDIA_ROOT, 'logs', 'api.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}

ADMIN_REORDER = (
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ipc_management',
                'USER': 'root',
                'PASSWORD': 'root123',
                'HOST': '127.0.0.1',
                'PORT': '7777',
                'ATOMIC_REQUEST': True,
                'OPTIONS': {
                        'charset': 'utf8mb4',
                        'use_unicode': True
                },
        'TEST': {
                    'CHARSET': 'utf8mb4',
                    'COLLATION': 'utf8mb4_0900_as_ci',
                }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'qr-code': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'qr-code-cache',
        'TIMEOUT': 3600
    }
}

LOGIN_URL = 'http://192.168.2.69:8000/login/?next=/'
LOGOUT_URL = 'http://192.168.2.69:8000/logout'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'GIS': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'gis'
        }
    },
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': LOGIN_URL,
    'LOGOUT_URL': LOGOUT_URL,
	'EXCLUDED_MEDIA_TYPES': [
		# 'html',
        # 'json',
	],
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'options',
        'head',
        'path',
        'trace'
    ],
    'REFETCH_SCHEMA_WITH_AUTH': True,  # Default: False
    'REFETCH_SCHEMA_ON_LOGOUT': True,  # Default: False
    'FETCH_SCHEMA_WITH_QUERY': True,  # Default: False
    'OPERATIONS_SORTER': 'method',  # None, alpha, method
    'DOC_EXPANSION': 'list',  # none, list, full
    'NATIVE_SCROLLBARS': True,  # Default: False
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': True,
    'EXPAND_RESPONSES': True
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

if DEBUG and os.environ.get('RUN_MAIN', None) != 'true':
    LOGGING = {}
