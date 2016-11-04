import json

import six
from cities.models import City, PostalCode, Subregion, Region
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View


class AjaxView(View):
    safe = True

    def dispatch(self, request, *args, **kwargs):
        if request.method in ['POST', 'PUT']:
            kwargs.setdefault('data', request.POST or
                              json.loads(request.body if six.PY2 else request.body.decode('utf-8')))
        return JsonResponse(super(AjaxView, self).dispatch(request, *args, **kwargs) or {}, safe=self.safe)


class AjaxPopulateAddress(AjaxView):
    safe = False

    def get(self, request):
        return {"foo": 3}

    def post(self, request, data):
        if not data.get('name'):
            return HttpResponseServerError("Name name is required.")
        model = {'city': City, 'subregion': Subregion, 'region': Region}.get(data.get('model'))
        if not model:
            return HttpResponseServerError("Invalid model: {}".format(data.get('model')))
        obj = get_object_or_404(model, pk=data['name'])
        data = {getattr(obj, key).__class__.__name__: {x: getattr(getattr(obj, key), x) for x in ['id', 'name']}
                for key in ['subregion', 'region', 'region__country', 'country'] if hasattr(obj, key)}
        # TODO: en la web de Django cities se muestra cómo obtener el código postal en función a la distancia.
        # No obstante, es bastante lento. Mientras lo  hago por el nombre, aunque habría que encontrar una
        # forma más fiable de hacer esto.
        postal_codes = PostalCode.objects.filter(name=obj.name)
        data['postal_code'] = postal_codes.first().code if postal_codes.count() else None
        return data
