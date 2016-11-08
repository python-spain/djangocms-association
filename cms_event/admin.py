from django.forms import ModelForm
from django.contrib import admin

from cms_contact.admin import IncludeAddressAdmin, IncludeAddressForm
from cms_event.models import Event, PriceEvent, Schedule
from django.utils.translation import ugettext_lazy as _


class EventForm(IncludeAddressForm):
    class Meta:
        model = Event
        exclude = ()


class PriceEventInline(admin.TabularInline):
    verbose_name_plural = _('prices')
    verbose_name = _('price')
    model = PriceEvent
    extra = 2


class ScheduleInline(admin.StackedInline):
    model = Schedule
    extra = 2
    fields = ('name', 'description', 'start_datetime', ('duration', 'location'),
              'speakers', 'custom_speakers', 'interests')


@admin.register(Event)
class EventAdmin(IncludeAddressAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = EventForm
    inlines = [
        PriceEventInline, ScheduleInline
    ]

    fieldsets = (
        (None, {
            'fields': ('name', 'edition', 'slug', 'description', 'poster', 'association',
                       'start_datetime', 'end_datetime', 'booking', 'total_seats', 'interests'),
        }),
        ('urls', {
            'fields': ('website_url', 'booking_url', 'schedule_url')
        }),
        ('Street', {
            'fields': (('street', 'city'), ('subregion', 'region')),
        })
    )

    class Media:
        js = ('cms_contact/src/js/jquery-admin-init.js',)
