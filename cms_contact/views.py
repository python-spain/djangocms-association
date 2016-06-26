from django.views.generic.edit import UpdateView

from cms_contact.forms import AddressForm
from cms_contact.models import Address


class AddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'cms_people/address.html'
    # fields = ('street', 'city')

    def get_object(self, queryset=None):
        return None