from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_association.models import Address
from taggit.managers import TaggableManager


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    bio = models.TextField(_('Bio'), blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    address = models.OneToOneField(Address, blank=True, null=True, on_delete=models.SET_NULL)
    interests = TaggableManager()
