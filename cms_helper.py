import getpass

HELPER_SETTINGS = dict(
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
    },
    ROOT_URLCONF = 'cms_contact.urls',
    INSTALLED_APPS=[
        'cities',
    ],
)


def run():
    from djangocms_helper import runner
    runner.cms('cms_contact')


def setup():
    import sys
    from djangocms_helper import runner
    runner.setup('cms_contact', sys.modules[__name__], use_cms=True)


if __name__ == '__main__':
    run()
