from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms_association.models import Association
from cms_contact.models import AbstractContact


BOOKING_OPTIONS = [
    ('OPTIONAL', _('Available')),
    ('REQUIRED', _('Required')),
    ('UNAVAILABLE', _('Free entry'))
]


class Event(AbstractContact):
    name = models.CharField(max_length=60, label=_('Name'))
    edition = models.PositiveSmallIntegerField(default=1, verbose_name=_('Edition'))
    slug = models.SlugField()
    description = models.TextField(blank=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    booking = models.CharField(choices=BOOKING_OPTIONS, default='OPTIONAL')
    total_seats = models.PositiveSmallIntegerField(blank=True, null=True)


class PriceEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, label=_('Name'))
    price = models.DecimalField()
    description = models.CharField(max_length=150, blank=True)
