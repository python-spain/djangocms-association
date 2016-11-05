from django.conf.urls import include, url

urlpatterns = [
    url(r'^contact/', include('cms_contact.urls')),
]