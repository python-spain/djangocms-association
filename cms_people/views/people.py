from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from cms_contact.views.map import group_by_coord
from cms_people.models import Person


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
