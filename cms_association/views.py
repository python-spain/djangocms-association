from cms_association.models import Association
from cms_contact.views.map import MapView, MapResultView


class AssociationsView(MapView):
    template_name = 'cms_association/associations.html'
    model = Association


class AssociationMapResultView(MapResultView):
    queryset = Association.objects.all()
    template_name = 'cms_association/association_map_results.html'
