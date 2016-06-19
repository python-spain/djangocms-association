from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_contacts.models import GenericContactField, Address
from taggit.managers import TaggableManager


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


class Person(models.Model):
    """A person corresponds to a Django user.
    It includes additional fields and privacy policies.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    bio = models.TextField(verbose_name=_('Bio'), blank=True, max_length=12000)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    address = models.OneToOneField(Address, blank=True, null=True, on_delete=models.SET_NULL)
    interests = TaggableManager()
    fields = GenericRelation(GenericContactField)
    # privacy policies
    real_name_privacy = models.CharField(max_length=20, choices=REAL_NAME_PRIVACY, default='VISIBLE')
    address_privacy = models.CharField(max_length=20, choices=ADDRESS_PRIVACY, default='ONLYCITY')
    bio_privacy = models.CharField(max_length=20, choices=BIO_PRIVACY, default='VISIBLE')
    email_privacy = models.CharField(max_length=20, choices=EMAIL_PRIVACY, default='ONLYMEMBERS')
    telephones_privacy = models.CharField(max_length=20, choices=TELEPHONES_PRIVACY, default='ONLYMEMBERS')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
