from django.conf.urls import url

from cms_contact.views import AjaxPopulateAddress

urlpatterns = [
    url('^populate_address$', AjaxPopulateAddress.as_view(), name='dataType')
]
