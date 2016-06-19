from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_contacts.models import GenericContactField


class Association(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=80)
    description = models.TextField()
    logo = models.ImageField(upload_to='logos', blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    fields = GenericRelation(GenericContactField)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
