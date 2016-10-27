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


def avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'avatars/{}.{}'.format(instance.user.id, ext)


class Person(AbstractContact):
    """A person corresponds to a Django user.
    It includes additional fields and privacy policies.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='person')
    bio = models.TextField(verbose_name=_('Biography'), blank=True, max_length=12000)
    avatar = models.ImageField(verbose_name=_('Avatar'), upload_to=avatar_path, blank=True, null=True)
    # privacy policies
    real_name_privacy = models.CharField(max_length=20, verbose_name=_('Real name privacy'), choices=REAL_NAME_PRIVACY,
                                         default='VISIBLE')
    address_privacy = models.CharField(max_length=20, verbose_name=_('Address privacy'), choices=ADDRESS_PRIVACY,
                                       default='ONLYCITY')
    bio_privacy = models.CharField(max_length=20, verbose_name=_('Bio privacy'), choices=BIO_PRIVACY, default='VISIBLE')
    email_privacy = models.CharField(max_length=20, verbose_name=_('Email privacy'), choices=EMAIL_PRIVACY,
                                     default='ONLYMEMBERS')
    telephones_privacy = models.CharField(max_length=20, verbose_name=_('Telephones privacy'),
                                          choices=TELEPHONES_PRIVACY,
                                          default='ONLYMEMBERS')
    # Newsletters
    news = models.BooleanField(default=True, verbose_name=_('News'))
    nearby_new_members = models.BooleanField(default=True, verbose_name=_('Nearby new members'))
    nearby_new_associations = models.BooleanField(default=True, verbose_name=_('Nearby new associations'))
    nearby_new_jobs = models.BooleanField(default=False, verbose_name=_('Nearby new jobs'))
    nearby_new_events = models.BooleanField(default=True, verbose_name=_('Nearby new events'))

    def save(self, **kwargs):
        if self.pk:
            person = Person.objects.get(pk=self.pk)
            if self.avatar != person.avatar:
                person.avatar.delete(save=False)
        super(Person, self).save(**kwargs)
