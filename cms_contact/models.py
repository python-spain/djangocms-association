from cities.models import District, City, Subregion, Region
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, EmailValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.validators import validate_international_phonenumber
from taggit.managers import TaggableManager

CONTACT_FIELD_TYPES = [
    (
        _('VCS'),
        (
            ('GITHUB', _('Github')),
            ('BITBUCKET', _('Bitbucket')),
            ('GITLAB', _('Gitlab')),
        ),
    ),
    (
        _('Social'),
        (
            ('TWITTER', _('Twitter')),
            ('FACEBOOK', _('Facebook')),
            ('GOOGLE-PLUS', _('Google+')),
            ('LINKEDIN', _('LinkedIn')),
            ('PINTEREST', _('Pinterest')),
            ('TUMBLR', _('Tumblr')),
            ('WEBSITE', _('Website'), {'validator': URLValidator}),
        ),
    ),
    (
        _('Communication'),
        (
            ('TELEPHONE', 'Telephone', {'validator': validate_international_phonenumber}),
            ('MOBILE', 'Mobile', {'validator': validate_international_phonenumber}),
            ('WHATSAPP', 'WhatsApp', {'validator': validate_international_phonenumber}),
            ('TELEGRAM', 'Telegram'),
            ('SKYPE', 'Skype'),
            ('FMESSENGER', 'Facebook Messenger'),
            ('LINE', 'Line'),
            ('IRC', 'IRC'),
            ('JABBER', 'Jabber/XMPP', {'validator': EmailValidator}),
        ),
    ),
]


def remove_social_options(sections):
    """Remove additional options in SOCIAL_TYPES
    """
    for section in sections:
        yield section[0], [choice[:2] for choice in section[1]]


class AbstractAddress(models.Model):
    """A abstract address model for addresses.

    The text of street is free. If the city does not exist can be entered manually.
    """
    street = models.CharField(max_length=120, label=_('Street and number'))
    poiny = PointField(blank=True, null=True)
    district = models.ForeignKey(District, blank=True, null=True, on_delete=models.SET_NULL, label=_('District'))
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL, label=_('City'))
    custom_city = models.CharField(max_length=40, blank=True)
    custom_postal_code = models.CharField(max_length=15, blank=True, label=_('Postal code'))
    subregion = models.ForeignKey(Subregion, blank=True, null=True, label=_('Subregion'), on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, label=_('Region'), on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.city and not self.custom_city:
            raise ValidationError(_('You must provide a city or a custom city'))
        elif self.city and self.custom_city:
            raise ValidationError(_('You can not provide custom city if you provided a city'))
        elif not self.custom_postal_code and self.custom_city:
            raise ValidationError(_('You must provide a postal code if you use a custom city'))

    class Meta:
        abstract = True


class AbstractContactField(models.Model):
    """A model to have social media key-value pairs. For example, twitter, Facebook, etc.
    """
    type = models.CharField(choices=remove_social_options(CONTACT_FIELD_TYPES), label=_('Type'))
    value = models.CharField(label=_('Value'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class GenericContactField(AbstractContactField):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Address(AbstractAddress):
    pass


class AbstractContact(models.Model):
    address = models.OneToOneField(Address, label=_('Address'), blank=True, null=True, on_delete=models.SET_NULL)
    interests = TaggableManager(label=_('Interests'))
    fields = GenericRelation(GenericContactField, label=_('Fields'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
