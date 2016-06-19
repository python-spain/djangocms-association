from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_association.models import Association
from cms_contact.models import AbstractContact


BOOKING_OPTIONS = [
    ('OPTIONAL', _('Available')),
    ('REQUIRED', _('Required')),
    ('UNAVAILABLE', _('Free entry'))
]


EVENT_TARGET = [
    ('LOCAL', _('Local')),
    ('REGION', _('Region')),
    ('COUNTRY', _('Country')),
    ('INTERNATIONAL', _('International')),
]


class Event(AbstractContact):
    name = models.CharField(max_length=60, label=_('Name'))
    edition = models.PositiveSmallIntegerField(default=1, verbose_name=_('Edition'))
    slug = models.SlugField()
    target = models.CharField(max_length=18, choices=EVENT_TARGET, default='LOCAL')
    description = models.TextField(blank=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    booking = models.CharField(choices=BOOKING_OPTIONS, default='OPTIONAL')
    total_seats = models.PositiveSmallIntegerField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    booking_url = models.URLField(blank=True, null=True)
    schedule_url = models.URLField(blank=True, null=True)


class PriceEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, label=_('Name'))
    price = models.DecimalField()
    description = models.CharField(max_length=150, blank=True)
    seats = models.PositiveSmallIntegerField(blank=True, null=True)
