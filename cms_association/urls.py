from django.conf.urls import url

from cms_association.views import AssociationsView

urlpatterns = [
    # url('^people_map_result$', PeopleMapResultView.as_view(), name='people_map_result'),
    # url('^(?P<username>.+)$', PersonView.as_view(), name='person'),
    url('^$', AssociationsView.as_view(), name='associations'),
]