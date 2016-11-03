from collections import defaultdict

from django.conf import settings
from django.views.generic import ListView
from django.views.generic import TemplateView


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


class MapView(TemplateView):
    model = None

    def get_elements(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['MAP_COORDS'] = settings.MAP_COORDS
        context['MAP_ZOOM'] = settings.MAP_ZOOM
        context['elements'] = dict(group_by_coord(self.get_elements(), lambda x: x.pk,
                                                  lambda x: ','.join(map(str, reversed(x)))))
        return context


class MapResultView(ListView):
    def get_queryset(self):
        pks = self.request.GET.get('pks', [])
        return self.queryset.filter(pk__in=pks.split(','))
