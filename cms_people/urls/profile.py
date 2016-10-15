from django.conf.urls import url

from cms_people.views import ProfileAboutView
from ..views import ProfileAddressView

urlpatterns = [
    url('^$', ProfileAboutView.as_view(), name='profile_about'),
    url('^address$', ProfileAddressView.as_view(), name='profile_address'),
]
