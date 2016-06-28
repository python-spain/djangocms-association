from itertools import chain

from cities.models import City, Subregion, Region, Country
from django.db.models import When, Value, Case, IntegerField
from django.forms import ModelForm, ChoiceField
from django.utils.encoding import force_text
from django_select2.forms import  ModelSelect2Widget

from cms_contact.models import Address


MAIN_COUNTRY = 'ES'


def main_country_priority(queryset, country_field='country'):
    return queryset.annotate(main_country=Case(
        When(**{country_field: Country.objects.get(code=MAIN_COUNTRY), 'then': Value('1')}),
        default=Value('0'),
        output_field=IntegerField()
    )).order_by('-main_country', 'name')


class AddressWidget(ModelSelect2Widget):
    width = '300px'
    create_new = False

    search_fields = [
        # Sort by:
        # - First spain
        # - Second Starts with term
        # - Third population
        # - Last alphanum.
        'name__istartswith',
        # 'name__icontains',
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
    queryset = main_country_priority(City.objects).all()
    create_new = True


class SubregionWidget(AddressWidget):
    queryset = main_country_priority(Subregion.objects, 'region__country').all()


class RegionWidget(AddressWidget):
    queryset = main_country_priority(Region.objects).all()

    def label_from_instance(self, obj):
        return force_text(obj)


class AddressForm(ModelForm):
    city = ChoiceField(widget=CityWidget)
    subregion = ChoiceField(widget=SubregionWidget)
    region = ChoiceField(widget=RegionWidget)

    class Meta:
        fields = ('street', 'city', 'subregion', 'region')
        model = Address
