from cities.models import City, Subregion, Region
from django.contrib import admin
from django.forms import CharField, ModelChoiceField, ModelForm

from cms_contact.forms import RegionWidget, SubregionWidget, CityWidget
from cms_contact.models import Address


class IncludeAddressForm(ModelForm):
    street = CharField(required=False)
    city = ModelChoiceField(City.objects.all(), widget=CityWidget(include_css=False))
    subregion = ModelChoiceField(Subregion.objects.all(), widget=SubregionWidget(include_css=False),required=False)
    region = ModelChoiceField(Region.objects.all(), widget=RegionWidget(include_css=False))

    def __init__(self, *args, **kwargs):
        super(IncludeAddressForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.address:
            self.initial['street'] = self.instance.address.street
            self.initial['city'] = self.instance.address.city
            self.initial['subregion'] = self.instance.address.subregion
            self.initial['region'] = self.instance.address.region

    class Meta:
        exclude = ('address',)


class IncludeAddressAdmin(admin.ModelAdmin):
    form = IncludeAddressForm

    def get_changelist_form(self, request, **kwargs):
        super(IncludeAddressAdmin, self).get_changelist_form(request, **kwargs)

    def save_model(self, request, obj, form, change):
        super(IncludeAddressAdmin, self).save_model(request, obj, form, change)
        address = obj.address or Address()
        address.street = form.cleaned_data.get('street', '')
        address.city = form.cleaned_data.get('city')
        address.subregion = form.cleaned_data.get('subregion')
        address.region = form.cleaned_data['region']
        is_new = not address.pk
        address.save()
        if is_new:
            obj.address = address
            obj.save()


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
