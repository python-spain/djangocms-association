from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView

from cms_contact.forms import AddressForm, GenericContactFieldFormSet
from cms_contact.models import Address
from cms_people.forms import SecurityForm, AboutForm, PrivacyForm
from cms_people.models import Person

from django.utils.translation import ugettext as _


TABS = [
    {'tab': 'about', 'name': _('About'), 'url_name': 'profile_about'},
    {'tab': 'security', 'name': _('Email and password'), 'url_name': 'profile_security'},
    {'tab': 'address', 'name': _('Address'), 'url_name': 'profile_address'},
    {'tab': 'privacy', 'name': _('Privacy'), 'url_name': 'profile_privacy'},
]


class ProfileView(UpdateView):
    profile_tab = ''

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile_tab'] = self.profile_tab
        context['tabs'] = TABS
        return context

    def get_success_url(self):
        return reverse('profile_{}'.format(self.profile_tab))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class PersonView(ProfileView):
    def get_object(self, queryset=None):
        person, exists = Person.objects.get_or_create(user=self.request.user)
        return person


class ProfileAboutView(PersonView):
    profile_tab = 'about'
    model = Person
    template_name = 'cms_people/about.html'
    form_class = AboutForm

    def get_context_data(self, **kwargs):
        context = super(ProfileAboutView, self).get_context_data(**kwargs)
        context['formset'] = GenericContactFieldFormSet()
        return context

    def get_initial(self):
        initial = super(ProfileAboutView, self).get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        response = super(ProfileAboutView, self).form_valid(form)
        self.object.user.first_name = form.cleaned_data['first_name']
        self.object.user.last_name = form.cleaned_data['last_name']
        self.object.user.save()
        return response


class ProfileSecurityView(ProfileView):
    profile_tab = 'security'
    model = get_user_model()
    template_name = 'cms_people/security.html'
    form_class = SecurityForm

    def get_object(self, queryset=None):
        return self.request.user


class ProfileAddressView(ProfileView):
    profile_tab = 'address'
    model = Address
    form_class = AddressForm
    template_name = 'cms_people/address.html'
    # fields = ('street', 'city')

    def get_form_kwargs(self):
        kwargs = super(ProfileAddressView, self).get_form_kwargs()
        kwargs.pop('request', None)
        return kwargs

    def get_object(self, queryset=None):
        user = self.request.user
        person = getattr(user, 'person', None)
        if person and person.address:
            return person.address
        else:
            return Address()

    def form_valid(self, form):
        person, exists = Person.objects.get_or_create(user=self.request.user)
        response = super(ProfileAddressView, self).form_valid(form)
        person.address = self.object
        person.save()
        return response


class ProfilePrivacyView(PersonView):
    profile_tab = 'privacy'
    model = Person
    template_name = 'cms_people/privacy.html'
    form_class = PrivacyForm
