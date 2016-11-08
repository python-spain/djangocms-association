from django.forms import ModelForm
from django.contrib import admin

from cms_contact.admin import IncludeAddressAdmin, IncludeAddressForm
from cms_event.models import Event


class EventForm(IncludeAddressForm):
    class Meta:
        model = Event
        exclude = ()


@admin.register(Event)
class EventAdmin(IncludeAddressAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = EventForm

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
