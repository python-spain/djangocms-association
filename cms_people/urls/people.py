from django.conf.urls import url

from cms_people.views.people import PersonView, PeopleView

urlpatterns = [
    url('^(?P<username>.+)$', PersonView.as_view(), name='person'),
    url('^$', PeopleView.as_view(), name='people'),
]