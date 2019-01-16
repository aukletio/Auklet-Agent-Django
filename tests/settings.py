SECRET_KEY = 123

AUKLET_CONFIG = {
    "api_key": "123",
    "application": "123",
    "organization": "123",
    "monitor": "123"
}

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'apm',
        'USER': 'apm',
        'PASSWORD': 'apm',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}

INSTALLED_APPS = (
    'auklet',
    'django.contrib.gis',
    'tests'
)
