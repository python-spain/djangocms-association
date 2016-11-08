from django.conf.urls import url

from cms_event.views import EventView

urlpatterns = [
    url('^(?P<event>.+)$', EventView.as_view(), name='event'),
    url('^$', AssociationsView.as_view(), name='events'),
]