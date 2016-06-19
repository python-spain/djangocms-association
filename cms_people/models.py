from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    bio = models.TextField(_('Bio'), blank=True)
    avatar = models.ImageField()
