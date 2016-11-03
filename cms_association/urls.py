from django.conf.urls import url

from cms_association.views import AssociationsView, AssociationMapResultView

urlpatterns = [
    url('^people_map_result$', AssociationMapResultView.as_view(), name='association_map_result'),
    # url('^(?P<association>.+)$', AssociationMapResultView.as_view(), name='association'),
    url('^$', AssociationsView.as_view(), name='associations'),
]