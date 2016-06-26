from cities.models import City
from django.forms import ModelForm, ChoiceField
from django_select2.forms import HeavySelect2Widget, ModelSelect2Widget

from cms_contact.models import Address


class CityWidget(ModelSelect2Widget):
    queryset = City.objects.all()
    search_fields = [
        'name__icontains'
    ]


class AddressForm(ModelForm):
    city = ChoiceField(widget=CityWidget)

    class Meta:
        fields = ('street', 'city')
        model = Address
