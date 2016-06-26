from cities.models import City
from django.forms import ModelForm, ChoiceField
from django_select2.forms import HeavySelect2Widget, ModelSelect2Widget

from cms_contact.models import Address


class CityWidget(ModelSelect2Widget):
    queryset = City.objects.all()
    width = '300px'
    search_fields = [
        'name__icontains'
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {'style': 'width: {};'.format(self.width)})
        super(CityWidget, self).__init__(*args, **kwargs)

    def build_attrs(self, extra_attrs=None, **kwargs):
        extra_attrs = extra_attrs or {}
        extra_attrs.setdefault('theme', 'bootstrap')
        return super(CityWidget, self).build_attrs(extra_attrs, **kwargs)


class AddressForm(ModelForm):
    city = ChoiceField(widget=CityWidget)

    class Meta:
        fields = ('street', 'city')
        model = Address
