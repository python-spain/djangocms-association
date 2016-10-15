from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView

from cms_contact.forms import AddressForm
from cms_contact.models import Address
from cms_people.models import Person


class ProfileView(UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class ProfileAboutView(ProfileView):
    model = Person
    template_name = 'cms_people/about.html'
    fields = ('bio',)

    def get_object(self, queryset=None):
        # return getattr(self.request.user, 'person', None)
        return None


class ProfileSecurityView(ProfileView):
    model = get_user_model()
    template_name = 'cms_people/security.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileAddressView(ProfileView):
    model = Address
    form_class = AddressForm
    template_name = 'cms_people/address.html'
    # fields = ('street', 'city')

    def get_object(self, queryset=None):
        return None