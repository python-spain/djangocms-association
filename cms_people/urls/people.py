from django.conf.urls import url

from cms_people.views.people import PersonView, PeopleView, PeopleMapResultView

urlpatterns = [
    url('^people_map_result$', PeopleMapResultView.as_view(), name='people_map_result'),
    url('^(?P<username>.+)$', PersonView.as_view(), name='person'),
    url('^$', PeopleView.as_view(), name='people'),
]