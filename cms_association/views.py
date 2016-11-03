from cms_association.models import Association
from cms_contact.views.map import MapView


class AssociationsView(MapView):
    template_name = 'cms_association/associations.html'
    model = Association
