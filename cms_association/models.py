from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_contacts.models import GenericContactField
from cms_people.models import Person


class Association(models.Model):
    name = models.CharField(max_length=60, label=_('Name'))
    slug = models.SlugField(max_length=80, label=('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    logo = models.ImageField(upload_to='logos', label=_('Logo'), blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, label=_('Parent association'), null=True, on_delete=models.SET_NULL)
    fields = GenericRelation(GenericContactField, label=_('Fields'))
    members = models.ManyToManyField(Person, through='Membership')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


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
