from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from cms_contact.views.map import MapView, MapResultView
from cms_people.models import Person


class PeopleView(MapView):
    template_name = 'cms_people/people.html'
    model = Person


class PeopleMapResultView(MapResultView):
    queryset = Person.objects.all()
    template_name = 'cms_people/people_map_results.html'


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
