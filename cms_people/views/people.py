from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView

from cms_people.models import Person
from django.views.generic.detail import DetailView


class PeopleView(TemplateView):
    template_name = 'cms_people/people.html'


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
