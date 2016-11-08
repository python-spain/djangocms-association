from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from cms_association.models import Association
from cms_contact.views.map import MapView, MapResultView


class AssociationsView(MapView):
    template_name = 'cms_association/associations.html'
    model = Association


class AssociationMapResultView(MapResultView):
    queryset = Association.objects.all()
    template_name = 'cms_association/association_map_results.html'


class AssociationView(DetailView):
    template_name = 'cms_association/association.html'
    model = Association
    slug_url_kwarg = 'association'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get(self.slug_url_kwarg))
