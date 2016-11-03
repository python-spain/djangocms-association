from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from cms_contact.models import AbstractContact, ADDRESS_PRIVACY, delete_contact

REAL_NAME_PRIVACY = [
    ('HIDDEN', _('Hidden')),
    ('ONLYMEMBERS', _('Only Members')),
    ('VISIBLE', _('Always visible')),
]

BIO_PRIVACY = REAL_NAME_PRIVACY
EMAIL_PRIVACY = REAL_NAME_PRIVACY
TELEPHONES_PRIVACY = REAL_NAME_PRIVACY


def avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'avatars/{}.{}'.format(instance.user.id, ext)


def privacy_validation(privacy, request):
    if privacy == 'VISIBLE' or privacy == 'ONLYMEMBERS' and request.user.is_authenticated():
        return True
    return False


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
                                          default='HIDDEN')
    # Newsletters
    news = models.BooleanField(default=True, verbose_name=_('News'))
    nearby_new_members = models.BooleanField(default=True, verbose_name=_('Nearby new members'))
    nearby_new_associations = models.BooleanField(default=True, verbose_name=_('Nearby new associations'))
    nearby_new_jobs = models.BooleanField(default=False, verbose_name=_('Nearby new jobs'))
    nearby_new_events = models.BooleanField(default=True, verbose_name=_('Nearby new events'))

    def get_real_name_privacy(self, request):
        return privacy_validation(self.real_name_privacy, request)

    def get_bio_privacy(self, request):
        return privacy_validation(self.bio_privacy, request)

    def get_email_privacy(self, request):
        return privacy_validation(self.email_privacy, request)

    def get_telephones_privacy(self, request):
        return privacy_validation(self.telephones_privacy, request)

    def get_address_privacy(self):
        return self.address_privacy

    def save(self, **kwargs):
        if self.pk:
            person = Person.objects.get(pk=self.pk)
            if self.avatar != person.avatar:
                person.avatar.delete(save=False)
        super(Person, self).save(**kwargs)

    @cached_property
    def username(self):
        return self.user.username

    @cached_property
    def first_name(self):
        return self.user.first_name

    @cached_property
    def last_name(self):
        return self.user.last_name

    @cached_property
    def email(self):
        return self.user.email

    def __str__(self):
        return self.username


def delete_person(sender, **kwargs):
    if kwargs['instance'].avatar:
        kwargs['instance'].avatar.delete(save=False)


pre_delete.connect(delete_person, sender=Person)
pre_delete.connect(delete_contact, sender=Person)
