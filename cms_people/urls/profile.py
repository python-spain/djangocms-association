from django.conf.urls import url
from ..views import AddressView

urlpatterns = [
    url('^address$', AddressView.as_view(), name='Profile_address'),
]
