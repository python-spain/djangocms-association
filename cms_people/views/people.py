from collections import defaultdict

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from cms_people.models import Person
from django.views.generic.detail import DetailView


def get_coords(element, privacy=False):
    place = None
    if privacy and element.address_privacy == 'ONLYREGION':
        place = element.address.region
    elif element.address:
        place = element.address.city or element.address.region
    if not place or (privacy and element.address_privacy == 'HIDDEN'):
        return
    return place.location.coords


def group_by_coord(elements, value_fn=lambda x: x, key_fn=lambda x: x):
    data = defaultdict(list)
    for element in elements:
        coords = get_coords(element)
        if not coords:
            continue
        coords = key_fn(coords)
        data[coords].append(value_fn(element))
    return data


class PeopleView(TemplateView):
    template_name = 'cms_people/people.html'

    def get_elements(self):
        return Person.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        context['MAP_COORDS'] = settings.MAP_COORDS
        context['MAP_ZOOM'] = settings.MAP_ZOOM
        context['elements'] = dict(group_by_coord(self.get_elements(), lambda x: x.pk,
                                                  lambda x: ','.join(map(str, reversed(x)))))
        return context


class PeopleMapResultView(ListView):
    queryset = Person.objects.all()
    template_name = 'cms_people/people_map_result.html'

    def get_queryset(self):
        pks = self.request.GET.get('pks', [])
        return self.queryset.filter(pk__in=pks.split(','))


class PersonView(DetailView):
    template_name = 'cms_people/person.html'
    model = Person
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)
        context['real_name_privacy'] = self.object.get_real_name_privacy(self.request)
        context['bio_privacy'] = self.object.get_bio_privacy(self.request)
        context['email_privacy'] = self.object.get_email_privacy(self.request)
        context['telephones_privacy'] = self.object.get_telephones_privacy(self.request)
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, user__username=self.kwargs.get(self.slug_url_kwarg))
