from django.conf import settings
from django.views.generic import TemplateView

from cms_association.models import Association
from cms_contact.views.map import group_by_coord


class AssociationView(TemplateView):
    template_name = 'cms_people/people.html'

    def get_elements(self):
        return Association.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AssociationView, self).get_context_data(**kwargs)
        context['MAP_COORDS'] = settings.MAP_COORDS
        context['MAP_ZOOM'] = settings.MAP_ZOOM
        context['elements'] = dict(group_by_coord(self.get_elements(), lambda x: x.pk,
                                                  lambda x: ','.join(map(str, reversed(x)))))
        return context
