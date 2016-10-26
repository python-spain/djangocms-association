from itertools import chain

from cities.models import City, Subregion, Region, Country
from django.contrib.auth.models import User
from django.db.models import When, Value, Case, IntegerField
from django.forms import ModelForm, ChoiceField, CharField, ModelChoiceField
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import Input, Select
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
    width = '100%'
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

    def render_options(self, *args):
        """Render only selected options and set QuerySet from :class:`ModelChoicesIterator`."""
        try:
            selected_choices, = args
        except ValueError:
            choices, selected_choices = args
            choices = chain(self.choices, choices)
        else:
            choices = self.choices
        selected_choices = {force_text(v) for v in selected_choices}
        output = ['<option></option>' if not self.is_required and not self.allow_multiple_selected else '']
        if isinstance(self.choices, ModelChoiceIterator):
            # Mejora significativa de rendimiernto con esta condición
            if self.queryset is None:
                self.queryset = self.choices.queryset
            selected_choices = {c for c in selected_choices
                                if c not in self.choices.field.empty_values}
            choices = {(obj.pk, self.label_from_instance(obj))
                       for obj in self.choices.queryset.filter(pk__in=selected_choices)}
        else:
            choices = {(k, v) for k, v in choices if force_text(k) in selected_choices}
        for option_value, option_label in choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

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
    # queryset = City.objects.all()
    create_new = True


class SubregionWidget(AddressWidget):
    queryset = main_country_priority(Subregion.objects, 'region__country').all()
    # queryset = Subregion.objects.all()


class RegionWidget(AddressWidget):
    queryset = main_country_priority(Region.objects).all()
    # queryset = Region.objects.all()

    def label_from_instance(self, obj):
        return force_text(obj)


class CountryWidget(Select):
    def render(self, name, value, attrs=None, choices=()):
        self.choices = ()
        attrs['readonly'] = 'readonly'
        return super(CountryWidget, self).render(name, value, attrs, ())


class Select2ChoiceField(ModelChoiceField):
    def _get_queryset(self):
        return self._queryset

    def _set_queryset(self, queryset):
        self._queryset = queryset
        if self.initial:
            self.widget.choices = self.queryset.filter(pk=self.initial)

    queryset = property(_get_queryset, _set_queryset)



class AddressForm(ModelForm):
    # city = ModelChoiceField(queryset=User.objects.filter(id=1))
    # subregion = ModelChoiceField(queryset=User.objects.filter(id=1))
    # region = ModelChoiceField(queryset=Region.objects.all())

    # city = Select2ChoiceField(queryset=City.objects.all(), widget=CityWidget)
    # subregion = Select2ChoiceField(queryset=Subregion.objects.all(), widget=SubregionWidget)
    # region = Select2ChoiceField(queryset=Region.objects.all(), widget=RegionWidget)
    country = Select2ChoiceField(queryset=Country.objects.all(), widget=CountryWidget)

    class Meta:
        fields = ('street', 'city', 'subregion', 'region', 'country', 'custom_postal_code')
        model = Address
        widgets = {'city': CityWidget, 'subregion': SubregionWidget, 'region': RegionWidget}
