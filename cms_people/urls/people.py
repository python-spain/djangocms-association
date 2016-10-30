from django.conf.urls import url

from cms_people.views.people import PersonView

urlpatterns = [
    url('^(?P<username>.+)$', PersonView.as_view(), name='person'),
]