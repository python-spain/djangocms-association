from django.conf.urls import url

from cms_event.views import EventView, EventsView

urlpatterns = [
    url('^(?P<event>.+)$', EventView.as_view(), name='event'),
    url('^$', EventsView.as_view(), name='events'),
]
