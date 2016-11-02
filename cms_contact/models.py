from cities.models import District, City, Subregion, Region
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models import PointField
from django.db.models.signals import pre_delete
from django.utils.functional import cached_property
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from cms_contact.contact_social import CONTACT_FIELD_TYPES, remove_social_options, SOCIAL


ADDRESS_PRIVACY = [
    ('HIDDEN', _('Hidden')),
    ('ONLYREGION', _('Show only region')),
    ('ONLYCITY', _('Show only city')),
    ('COMPLETE', _('Show full address')),
]


ADDRESS_PRIVACY_FIELDS = {
    'HIDDEN': [],
    'ONLYREGION': ['subregion', 'region', 'country'],
    'ONLYCITY': ['city_name', 'subregion', 'region', 'custom_postal_code', 'country'],
    'COMPLETE': ['street', 'city_name', 'subregion', 'region', 'custom_postal_code', 'country'],
}


class AbstractAddress(models.Model):
    """A abstract address model for addresses.

    The text of street is free. If the city does not exist can be entered manually.
    """
    street = models.CharField(max_length=120, verbose_name=_('Street and number'))
    # TODO: change to point
    poiny = PointField(blank=True, null=True)
    district = models.ForeignKey(District, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('District'))
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('City'))
    custom_city = models.CharField(max_length=40, blank=True)
    custom_postal_code = models.CharField(max_length=15, blank=True, verbose_name=_('Postal code'))
    subregion = models.ForeignKey(Subregion, blank=True, null=True, verbose_name=_('Subregion'),
                                  on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_country(self):
        for item in [self.city, self.subregion, self.region if self.region_id else None]:
            if not item:
                continue
            if hasattr(item, 'region'):
                return item.region.country
            return item.country

    @cached_property
    def country(self):
        return self.get_country()

    def full_address(self, privacy='COMPLETE', exclude=()):
        fields = [x for x in ADDRESS_PRIVACY_FIELDS[privacy] if x not in exclude]
        fields = map(lambda x: str(getattr(self, x, None)), fields)
        fields = list(filter(lambda x: x, fields))
        return ' '.join(fields)

    @cached_property
    def city_name(self):
        return self.custom_city or (self.city.name if self.city else None)

    def clean(self):
        if not self.city and not self.custom_city:
            raise ValidationError(_('You must provide a city or a custom city'))
        elif self.city and self.custom_city:
            raise ValidationError(_('You can not provide custom city if you provided a city'))
        elif not self.custom_postal_code and self.custom_city:
            raise ValidationError(_('You must provide a postal code if you use a custom city'))

    def __str__(self):
        return self.full_address()

    class Meta:
        abstract = True


class AbstractContactField(models.Model):
    """A model to have social media key-value pairs. For example, twitter, Facebook, etc.
    """
    type = models.CharField(max_length=25, choices=remove_social_options(CONTACT_FIELD_TYPES), verbose_name=_('Type'))
    value = models.CharField(max_length=150, verbose_name=_('Value'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_html(self):
        fn = SOCIAL[self.type].get('to_html', lambda x: mark_safe('<span>{}</span>'.format(escape(x))))
        return fn(self.value)

    def icon_path(self):
        return static('cms_contact/src/img/{}.png'.format(self.type.lower()))

    def is_telephone(self):
        return SOCIAL[self.type].get('is_telephone', False)

    class Meta:
        abstract = True


class GenericContactField(AbstractContactField):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Address(AbstractAddress):
    pass


class AbstractContact(models.Model):
    address = models.OneToOneField(Address, verbose_name=_('Address'), blank=True, null=True, on_delete=models.SET_NULL)
    interests = TaggableManager(verbose_name=_('Interests'), blank=True)
    fields = GenericRelation(GenericContactField, verbose_name=_('Fields'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def delete_contact(sender, **kwargs):
    if kwargs['instance'].address:
        kwargs['instance'].address.delete()
    kwargs['instance'].fields.delete()
