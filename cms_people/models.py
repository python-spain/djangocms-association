from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_contact.models import AbstractContact


REAL_NAME_PRIVACY = [
    ('HIDDEN', _('Hidden')),
    ('ONLYMEMBERS', _('Only Members')),
    ('VISIBLE', _('Always visible')),
]


ADDRESS_PRIVACY = [
    ('HIDDEN', _('Hidden')),
    ('ONLYREGION', _('Show only region')),
    ('ONLYCITY', _('Show only city')),
    ('COMPLETE', _('Show full address')),
]


BIO_PRIVACY = REAL_NAME_PRIVACY
EMAIL_PRIVACY = REAL_NAME_PRIVACY
TELEPHONES_PRIVACY = REAL_NAME_PRIVACY


class Person(AbstractContact):
    """A person corresponds to a Django user.
    It includes additional fields and privacy policies.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, label=_('User'), verbose_name=_('User'))
    bio = models.TextField(verbose_name=_('Biography'), blank=True, max_length=12000)
    avatar = models.ImageField(label=_('Avatar'), upload_to='avatars', blank=True, null=True)
    # privacy policies
    real_name_privacy = models.CharField(max_length=20, label=_('Real name privacy'), choices=REAL_NAME_PRIVACY,
                                         default='VISIBLE')
    address_privacy = models.CharField(max_length=20, label=_('Address privacy'), choices=ADDRESS_PRIVACY,
                                       default='ONLYCITY')
    bio_privacy = models.CharField(max_length=20, label=_('Bio privacy'), choices=BIO_PRIVACY, default='VISIBLE')
    email_privacy = models.CharField(max_length=20, label=('Email privacy'), choices=EMAIL_PRIVACY,
                                     default='ONLYMEMBERS')
    telephones_privacy = models.CharField(max_length=20, label=_('Telephones privacy'), choices=TELEPHONES_PRIVACY,
                                          default='ONLYMEMBERS')
