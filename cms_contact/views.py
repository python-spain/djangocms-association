from django.views.generic.edit import UpdateView
from cms_contact.models import Address


class AddressView(UpdateView):
    model = Address
    template_name = 'cms_people/address.html'
    fields = ('street', 'district', 'city')

    def get_object(self, queryset=None):
        return None