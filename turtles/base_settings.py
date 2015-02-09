import os

TURTLES_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(TURTLES_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

DEBUG = False
TEMPLATE_DEBUG = False

HOST = "turtles.wildside.org.il"
ALLOWED_HOSTS = [HOST]


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.gis',

    'django_extensions',
    'floppyforms_bootstrap3',
    'floppyforms',
    'bootstrap3',
    'leaflet',
    'google_leaflet',

    'obs',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'turtles.urls'

WSGI_APPLICATION = 'turtles.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'turtles',
        'USER': 'turtles',
    }
}

# Internationalization
LANGUAGE_CODE = 'he'
TIME_ZONE = 'Asia/Jerusalem'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TURTLE_SMTP_DOMAIN = HOST
TURTLE_MAIL_PREFIX = "turtle."
TURTLES_SMTP_PORT = 4467
TURTLES_SMTP_HOST = '127.0.0.1'

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = (
    os.path.join(TURTLES_DIR, "static"),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collected-static')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

ITM_SRID = 2039

DEFAULT_FILE_STORAGE = "turtles.storages.RandomFilenameStorage"

LEAFLET_CONFIG = {
    'SPATIAL_EXTENT': (30, 29, 36, 33.5),
    # 'DEFAULT_CENTER': (31.5, 35.0),
    # 'DEFAULT_ZOOM': 8,

    'TILES': [

        ('OVI Satellite',
         'http://maptile.maps.svc.ovi.com/maptiler/maptile/newest/satellite.day/{z}/{x}/{y}/256/png8',
         'OVI maps'),

        ('OpenStreet map',
         'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
         'OpenStreet Map'),

        ('MapQuest Open Aerial',
         'http://otile1.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg',
         'MapQuest Open Aerial'),

    ],

    'ATTRIBUTION_PREFIX': 'Timi',

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },

    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
        },
        'inbox': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

if os.name == 'nt':
    OSGEO4W = r"C:\OSGeo4W"
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

