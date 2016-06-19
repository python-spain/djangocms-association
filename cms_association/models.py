from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from cms_contact.models import GenericContactField, Address, AbstractContact
from cms_people.models import Person


EVENT_TARGET = [
    ('LOCAL', _('Local')),
    ('REGION', _('Region')),
    ('COUNTRY', _('Country')),
    ('INTERNATIONAL', _('International')),
]


class Association(AbstractContact):
    name = models.CharField(max_length=60, label=_('Name'))
    slug = models.SlugField(max_length=80, label=('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    logo = models.ImageField(upload_to='logos', label=_('Logo'), blank=True, null=True)
    target = models.CharField(max_length=18, choices=EVENT_TARGET, default='LOCAL')
    parent = models.ForeignKey('self', blank=True, label=_('Parent association'), null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(Person, through='Membership')
    foundation_date = models.DateField(auto_now_add=True)
    death_date = models.DateField(blank=True, null=True)


class Membership(models.Model):
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    member = models.ForeignKey(Person, on_delete=models.CASCADE)
    active = models.BooleanField(label=_('Active'), default=False)
    position = models.CharField(max_length=30, blank=True)
    executive_board = models.BooleanField(default=False)
    since = models.DateTimeField(label=_('Since'), blank=True, null=True,
                                 help_text=_('If a user has never been as active, this will be null.'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
