import json

import six
from django.http import JsonResponse
from django.views.generic import View
from django.views.generic.edit import UpdateView
from cms_contact.forms import AddressForm
from cms_contact.models import Address


class AjaxView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT']:
            kwargs.setdefault('data', request.POST or
                              json.loads(request.body if six.PY2 else request.body.decode('utf-8')))
        return JsonResponse(super(AjaxView, self).dispatch(request, *args, **kwargs) or {})


class AddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'cms_people/address.html'
    # fields = ('street', 'city')

    def get_object(self, queryset=None):
        return None


class AjaxPopulateAddress(AjaxView):
    def get(self, request):
        return {"foo": 3}

    def post(self, request, data):
        return {}
