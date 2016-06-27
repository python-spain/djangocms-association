from itertools import chain

from cities.models import City, Subregion, Region
from django.forms import ModelForm, ChoiceField
from django.utils.encoding import force_text
from django_select2.forms import  ModelSelect2Widget

from cms_contact.models import Address


class AddressWidget(ModelSelect2Widget):
    width = '300px'
    create_new = False

    search_fields = [
        'name__icontains'
    ]

    def build_attrs(self, extra_attrs=None, **kwargs):
        extra_attrs = extra_attrs or {}
        extra_attrs.setdefault('class', '')
        extra_attrs.setdefault('style', 'width: {}'.format(self.width))
        extra_attrs.setdefault('data-theme', 'bootstrap')
        if self.create_new:
            extra_attrs.setdefault('data-tags', 'true')
            extra_attrs['class'] += ' django-select2-create-tag'
            extra_attrs['class'] += ' django-select2-template-result'
        return super(AddressWidget, self).build_attrs(extra_attrs, **kwargs)

    def _get_media(self):
        media = super(AddressWidget, self)._get_media()
        media._js.remove('django_select2/django_select2.js')
        media.add_js(['cms_contact/src/js/django_select2.js'])
        return media

    media = property(_get_media)

    def label_from_instance(self, obj):
        return '{} ({})'.format(obj.name, obj.region)


class CityWidget(AddressWidget):
    queryset = City.objects.all()
    create_new = True


class SubregionWidget(AddressWidget):
    queryset = Subregion.objects.all()


class RegionWidget(AddressWidget):
    queryset = Region.objects.all()

    def label_from_instance(self, obj):
        return force_text(obj)


class AddressForm(ModelForm):
    city = ChoiceField(widget=CityWidget)
    subregion = ChoiceField(widget=SubregionWidget)
    region = ChoiceField(widget=RegionWidget)

    class Meta:
        fields = ('street', 'city', 'subregion', 'region')
        model = Address
