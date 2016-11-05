import getpass


DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': 'localhost',
        'NAME': 'pywebes_test',
        'PASSWORD': '',
        'PORT': '',
        'USER': getpass.getuser(),
    }
}

ROOT_URLCONF = 'cms_contact.urls'

INSTALLED_APPS = [
    'cities',
]
