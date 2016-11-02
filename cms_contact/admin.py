from cities.models import City, Subregion, Region
from django.contrib import admin
from django.forms import CharField, ModelChoiceField, ModelForm

from cms_contact.forms import RegionWidget, SubregionWidget, CityWidget
from cms_contact.models import Address


class IncludeAddressForm(ModelForm):
    street = CharField()
    city = ModelChoiceField(City.objects.all(), widget=CityWidget(include_css=False))
    subregion = ModelChoiceField(Subregion.objects.all(), widget=SubregionWidget(include_css=False),required=False)
    region = ModelChoiceField(Region.objects.all(), widget=RegionWidget(include_css=False))


class IncludeAddressAdmin(admin.ModelAdmin):
    form = IncludeAddressForm


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
