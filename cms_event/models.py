from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from cms_association.models import Association, EVENT_TARGET
from cms_contact.models import AbstractContact
from cms_people.models import Person

BOOKING_OPTIONS = [
    ('OPTIONAL', _('Available')),
    ('REQUIRED', _('Required')),
    ('UNAVAILABLE', _('Free entry'))
]


ATTENDANCE_OPTIONS = [
    ('YES', _('Yes')),
    ('NO', _('No')),
    ('MAYBE', _('Maybe')),
]


class Event(AbstractContact):
    name = models.CharField(max_length=60, verbose_name=_('Name'))
    edition = models.PositiveSmallIntegerField(default=1, verbose_name=_('Edition'))
    slug = models.SlugField()
    target = models.CharField(max_length=18, choices=EVENT_TARGET, default='LOCAL')
    poster = models.ImageField(upload_to='posters', verbose_name=_('Poster'), blank=True, null=True)
    description = models.TextField(blank=True)
    association = models.ForeignKey(Association, on_delete=models.CASCADE, blank=True, null=True)
    start_datetime = models.DateTimeField(verbose_name=_('Start datetime'), blank=True, null=True)
    end_datetime = models.DateTimeField(verbose_name=_('End datetime'), blank=True, null=True)
    booking = models.CharField(max_length=18, choices=BOOKING_OPTIONS, default='OPTIONAL')
    total_seats = models.PositiveSmallIntegerField(verbose_name=_('Total seats'), blank=True, null=True)
    website_url = models.URLField(verbose_name=_('Website url'), blank=True, null=True)
    booking_url = models.URLField(verbose_name=_('Booking url'), blank=True, null=True)
    schedule_url = models.URLField(verbose_name=_('Schedule url'), blank=True, null=True)
    attendances = models.ManyToManyField(Person, verbose_name=_('Attendances'), through='Attendance')


class PriceEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, verbose_name=_('Name'))
    price = models.DecimalField(decimal_places=2, max_digits=8, verbose_name=_('Price'))
    description = models.CharField(verbose_name=_('Description'), max_length=150, blank=True)
    seats = models.PositiveSmallIntegerField(verbose_name=_('Seats'), blank=True, null=True)


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    attendance = models.CharField(max_length=12, verbose_name=_('You will go?'), choices=ATTENDANCE_OPTIONS)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    interests = TaggableManager(verbose_name=_('Interests'))
    speakers = models.ManyToManyField(Person, verbose_name=_('Speakers'))
    custom_speakers = models.CharField(max_length=150, blank=True, verbose_name=_('Speakers who are not in the db'))
    start_datetime = models.DateTimeField(blank=True, null=True, verbose_name=_('Start datetime'))
    duration = models.DurationField(blank=True, null=True, verbose_name=_('Duration'))
    location = models.CharField(blank=True, max_length=80, verbose_name=_('Location'),
                                help_text=_('Location within the building or buildings.'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
