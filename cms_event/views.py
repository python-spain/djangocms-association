from sched import Event

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView


class EventView(DetailView):
    template_name = 'cms_event/event.html'
    slug_url_kwarg = 'event'
    model = Event

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get(self.slug_url_kwarg))


class EventsView(ListView):
    model = Event
