import json

import six
from cities.models import City
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.generic.edit import UpdateView
from cms_contact.forms import AddressForm
from cms_contact.models import Address


class AjaxView(View):
    safe = True

    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT']:
            kwargs.setdefault('data', request.POST or
                              json.loads(request.body if six.PY2 else request.body.decode('utf-8')))
        return JsonResponse(super(AjaxView, self).dispatch(request, *args, **kwargs) or {}, safe=self.safe)


class AddressView(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'cms_people/address.html'
    # fields = ('street', 'city')

    def get_object(self, queryset=None):
        return None


class AjaxPopulateAddress(AjaxView):
    safe = False

    def get(self, request):
        return {"foo": 3}

    def post(self, request, data):
        obj = get_object_or_404(City, pk=data['city'])
        return {getattr(obj, key).__class__.__name__: {x: getattr(getattr(obj, key), x) for x in ['id', 'name']}
                for key in ['subregion', 'region', 'region__country', 'country'] if hasattr(obj, key)}
